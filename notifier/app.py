import json
import os
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

TABLE_NAME = os.environ.get('JOBS_TABLE', 'genai-job-agent-listings')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'chrisadams27@gmail.com')

ALERT_THRESHOLD = 75
DIGEST_THRESHOLD = 40

table = dynamodb.Table(TABLE_NAME)


def get_active_profiles():
    """Get all active profiles with email addresses."""
    response = table.scan(
        FilterExpression='SK = :sk AND active = :a',
        ExpressionAttributeValues={':sk': 'CONFIG', ':a': True}
    )
    return response['Items']


def get_scored_listings():
    """Get all scored listings waiting for notification."""
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression='GSI1PK = :status',
        ExpressionAttributeValues={':status': 'STATUS#scored'}
    )
    return response['Items']


def get_listings_for_profile(listings, profile_name):
    """Filter listings that belong to a specific profile."""
    return [l for l in listings if l.get('profile') == profile_name]


def format_apply_links(listing):
    """Format apply links for display in email."""
    apply_url = listing.get('apply_url', '')
    apply_source = listing.get('apply_source', '')
    apply_options = listing.get('apply_options', [])

    lines = []

    if apply_url:
        label = f"Apply on {apply_source}" if apply_source else "Apply"
        lines.append(f"    ➤ {label}: {apply_url}")

        if len(apply_options) > 1:
            lines.append(f"    Also on:")
            for opt in apply_options[1:]:
                source = opt.get('source', 'Unknown')
                url = opt.get('url', '')
                if url:
                    lines.append(f"      • {source}: {url}")
    else:
        url = listing.get('url', '')
        if url:
            lines.append(f"    ➤ View: {url}")

    return "\n".join(lines)


def format_listing(listing):
    """Format a single listing for the digest email."""
    score = listing.get('bedrock_score', 0)
    title = listing.get('title', 'Unknown')
    company = listing.get('company', 'Unknown')
    location = listing.get('location', 'Unknown')
    summary = listing.get('summary', 'No summary available.')
    details = listing.get('score_details', {})

    lines = [
        f"{'⭐ ' if score >= ALERT_THRESHOLD else ''}[{score}/100] {title}",
        f"    Company:   {company}",
        f"    Location:  {location}",
    ]

    if details:
        lines.append(f"    Scores:    role={details.get('role_fit','-')}  genai={details.get('genai_relevance','-')}  seniority={details.get('seniority_match','-')}  industry={details.get('industry_match','-')}  geo={details.get('geographic_match','-')}")

    lines.append(f"    Summary:   {summary}")

    apply_links = format_apply_links(listing)
    if apply_links:
        lines.append(apply_links)

    lines.append("")
    lines.append("─" * 60)
    lines.append("")
    return "\n".join(lines)


def send_email(to_email, subject, body):
    """Send an email via SES."""
    try:
        ses.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {'Text': {'Data': body, 'Charset': 'UTF-8'}}
            }
        )
        print(f"  Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        print(f"  ERROR sending to {to_email}: {e}")
        return False


def send_digest(profile_name, to_email, listings):
    """Send a digest email for a specific profile."""
    if not listings:
        print(f"  [{profile_name}] No listings to digest")
        return False

    sorted_listings = sorted(listings, key=lambda x: x.get('bedrock_score', 0), reverse=True)
    above_threshold = [l for l in sorted_listings if l.get('bedrock_score', 0) >= DIGEST_THRESHOLD]

    if not above_threshold:
        print(f"  [{profile_name}] No listings above digest threshold ({DIGEST_THRESHOLD})")
        return False

    now = datetime.now().strftime('%B %d, %Y')
    header = f"Job Agent - Weekly Digest for {profile_name.title()}\n{now}\n{'=' * 50}\n\n"
    header += f"Total scored: {len(listings)} | Above threshold ({DIGEST_THRESHOLD}+): {len(above_threshold)}\n"

    high = [l for l in above_threshold if l.get('bedrock_score', 0) >= ALERT_THRESHOLD]
    if high:
        header += f"🔥 High-priority matches ({ALERT_THRESHOLD}+): {len(high)}\n"

    header += "\n" + "-" * 50 + "\n\n"

    body = header
    for listing in above_threshold:
        body += format_listing(listing)

    body += "-" * 50 + "\n"
    body += "GenAI Job Search Agent | github.com/falcon9heavy/genai-job-agent\n"

    subject = f"Job Agent Digest ({profile_name.title()}): {len(above_threshold)} matches ({len(high)} hot)"
    return send_email(to_email, subject, body)


def send_alerts(profile_name, to_email, listings):
    """Send individual hot-match alert emails for a specific profile."""
    high = [l for l in listings if l.get('bedrock_score', 0) >= ALERT_THRESHOLD]

    if not high:
        print(f"  [{profile_name}] No high-priority listings (threshold: {ALERT_THRESHOLD})")
        return 0

    sorted_high = sorted(high, key=lambda x: x.get('bedrock_score', 0), reverse=True)
    count = 0

    for listing in sorted_high:
        score = listing.get('bedrock_score', 0)
        title = listing.get('title', 'Unknown')
        company = listing.get('company', 'Unknown')
        location = listing.get('location', '')
        apply_url = listing.get('apply_url', listing.get('url', ''))
        apply_source = listing.get('apply_source', '')

        message = f"🔥 HOT MATCH ({score}/100): {title} at {company}"
        if location:
            message += f" [{location}]"
        message += "\n"

        if apply_url:
            label = f"Apply on {apply_source}" if apply_source else "Apply"
            message += f"\n➤ {label}: {apply_url}"

            apply_options = listing.get('apply_options', [])
            if len(apply_options) > 1:
                message += "\n\nAlso available on:"
                for opt in apply_options[1:]:
                    source = opt.get('source', 'Unknown')
                    url = opt.get('url', '')
                    if url:
                        message += f"\n  • {source}: {url}"

        summary = listing.get('summary', '')
        if summary:
            message += f"\n\nSummary: {summary}"

        subject = f"🔥 Job Alert ({profile_name.title()}): {title} ({score}/100)"
        if send_email(to_email, subject, message):
            count += 1

    print(f"  [{profile_name}] Alerts sent: {count}")
    return count


def update_notified(listings):
    """Mark listings as notified."""
    for listing in listings:
        table.update_item(
            Key={'PK': listing['PK'], 'SK': listing['SK']},
            UpdateExpression='SET GSI1PK = :status, notified_at = :ts',
            ExpressionAttributeValues={
                ':status': 'STATUS#notified',
                ':ts': datetime.now().isoformat()
            }
        )


def lambda_handler(event, context):
    profiles = get_active_profiles()
    listings = get_scored_listings()

    stats = {
        'total_listings': len(listings),
        'profiles_processed': 0,
        'profile_stats': {}
    }

    if not listings:
        print("No scored listings to notify")
        return {'statusCode': 200, 'body': json.dumps(stats)}

    if not profiles:
        print("No active profiles found")
        return {'statusCode': 200, 'body': json.dumps(stats)}

    for profile in profiles:
        name = profile.get('name', 'unknown')
        email = profile.get('email', '')

        if not email:
            print(f"[{name}] No email configured, skipping notifications")
            continue

        profile_listings = get_listings_for_profile(listings, name)
        print(f"\n=== Profile: {name} ({email}) - {len(profile_listings)} listings ===")

        p_stats = {
            'email': email,
            'total': len(profile_listings),
            'digest_sent': False,
            'alerts': 0
        }

        if profile_listings:
            p_stats['digest_sent'] = send_digest(name, email, profile_listings)
            p_stats['alerts'] = send_alerts(name, email, profile_listings)

        stats['profile_stats'][name] = p_stats
        stats['profiles_processed'] += 1

    # Mark all listings as notified
    update_notified(listings)

    print(f"\nResults: {json.dumps(stats, indent=2)}")
    return {'statusCode': 200, 'body': json.dumps(stats)}

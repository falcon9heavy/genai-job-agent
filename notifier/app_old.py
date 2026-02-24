import json
import os
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

TABLE_NAME = os.environ.get('JOBS_TABLE', 'genai-job-agent-listings')
DIGEST_TOPIC = os.environ.get('DIGEST_TOPIC', '')
ALERT_TOPIC = os.environ.get('ALERT_TOPIC', '')

ALERT_THRESHOLD = 75
DIGEST_THRESHOLD = 40

table = dynamodb.Table(TABLE_NAME)


def get_scored_listings():
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression='GSI1PK = :status',
        ExpressionAttributeValues={':status': 'STATUS#scored'}
    )
    return response['Items']


def format_listing(listing):
    score = listing.get('bedrock_score', 0)
    title = listing.get('title', 'Unknown')
    company = listing.get('company', 'Unknown')
    location = listing.get('location', 'Unknown')
    summary = listing.get('summary', 'No summary available.')
    url = listing.get('url', '')
    details = listing.get('score_details', {})

    lines = [
        f"{'⭐ ' if score >= ALERT_THRESHOLD else ''}[{score}/100] {title}",
        f"    Company:   {company}",
        f"    Location:  {location}",
    ]

    if details:
        lines.append(f"    Scores:    role={details.get('role_fit','-')}  genai={details.get('genai_relevance','-')}  seniority={details.get('seniority_match','-')}  industry={details.get('industry_match','-')}  geo={details.get('geographic_match','-')}")

    lines.append(f"    Summary:   {summary}")

    if url:
        lines.append(f"    Link:      {url}")

    lines.append("")
    lines.append("─" * 60)
    lines.append("")
    return "\n".join(lines)


def send_digest(listings):
    if not listings:
        print("No listings above digest threshold")
        return False

    sorted_listings = sorted(listings, key=lambda x: x.get('bedrock_score', 0), reverse=True)
    above_threshold = [l for l in sorted_listings if l.get('bedrock_score', 0) >= DIGEST_THRESHOLD]

    if not above_threshold:
        print(f"No listings above digest threshold ({DIGEST_THRESHOLD})")
        return False

    now = datetime.now().strftime('%B %d, %Y')
    header = f"GenAI Job Agent - Weekly Digest\n{now}\n{'=' * 50}\n\n"
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

    sns.publish(
        TopicArn=DIGEST_TOPIC,
        Subject=f"Job Agent Digest: {len(above_threshold)} matches ({len(high)} hot)",
        Message=body
    )
    print(f"Digest sent: {len(above_threshold)} listings")
    return True


def send_alerts(listings):
    high = [l for l in listings if l.get('bedrock_score', 0) >= ALERT_THRESHOLD]

    if not high:
        print(f"No high-priority listings (threshold: {ALERT_THRESHOLD})")
        return 0

    sorted_high = sorted(high, key=lambda x: x.get('bedrock_score', 0), reverse=True)
    count = 0

    for listing in sorted_high:
        score = listing.get('bedrock_score', 0)
        title = listing.get('title', 'Unknown')
        company = listing.get('company', 'Unknown')
        location = listing.get('location', '')

        message = f"🔥 HOT MATCH ({score}/100): {title} at {company}"
        if location:
            message += f" [{location}]"

        sns.publish(
            TopicArn=ALERT_TOPIC,
            Subject=f"🔥 Job Alert: {title} ({score}/100)",
            Message=message
        )
        count += 1

    print(f"Alerts sent: {count}")
    return count


def update_notified(listings):
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
    listings = get_scored_listings()
    stats = {'total': len(listings), 'digest_sent': False, 'alerts': 0}

    if not listings:
        print("No scored listings to notify")
        return {'statusCode': 200, 'body': json.dumps(stats)}

    stats['digest_sent'] = send_digest(listings)
    stats['alerts'] = send_alerts(listings)

    update_notified(listings)

    print(f"\nResults: {stats}")
    return {'statusCode': 200, 'body': json.dumps(stats)}
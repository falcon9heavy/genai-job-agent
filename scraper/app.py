import json
import os
import hashlib
import boto3
from datetime import datetime, timedelta
from serpapi import GoogleSearch

# Clients
dynamodb = boto3.resource('dynamodb')
secrets = boto3.client('secretsmanager')

TABLE_NAME = os.environ.get('JOBS_TABLE', 'genai-job-agent-listings')
table = dynamodb.Table(TABLE_NAME)


def get_serpapi_key():
    response = secrets.get_secret_value(SecretId='genai-job-agent/serpapi-key')
    return response['SecretString']


def get_active_profiles():
    response = table.scan(
        FilterExpression='SK = :sk AND active = :a',
        ExpressionAttributeValues={':sk': 'CONFIG', ':a': True}
    )
    return response['Items']


def search_jobs(api_key, query, location):
    params = {
        'engine': 'google_jobs',
        'q': query,
        'location': location,
        'api_key': api_key
    }
    search = GoogleSearch(params)
    return search.get_dict().get('jobs_results', [])


def make_job_id(profile_name, job):
    raw = f"{profile_name}-{job.get('title','')}-{job.get('company_name','')}-{job.get('location','')}".lower()
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def job_exists(source, job_id):
    response = table.get_item(Key={'PK': f'SOURCE#{source}', 'SK': f'JOB#{job_id}'})
    return 'Item' in response


def write_job(source, job_id, job_data, profile_name, raw_score, matched_keywords):
    now = datetime.now()
    item = {
        'PK': f'SOURCE#{source}',
        'SK': f'JOB#{job_id}',
        'GSI1PK': 'STATUS#new',
        'GSI1SK': f'DATE#{now.strftime("%Y-%m-%d")}',
        'profile': profile_name,
        'title': job_data.get('title', ''),
        'company': job_data.get('company_name', ''),
        'location': job_data.get('location', ''),
        'description': job_data.get('description', '')[:5000],
        'url': job_data.get('related_links', [{}])[0].get('link', ''),
        'raw_score': raw_score,
        'keywords_matched': matched_keywords,
        'first_seen': now.isoformat(),
        'last_seen': now.isoformat(),
        'ttl': int((now + timedelta(days=90)).timestamp())
    }
    table.put_item(Item=item)
    return item


def score_listing(job_data, profile):
    text = f"{job_data.get('title', '')} {job_data.get('description', '')} {job_data.get('location', '')}".lower()

    # Check exclusions
    for exc in profile.get('exclusions', []):
        if exc.lower() in text:
            return None

    matched = []
    tier1_count = 0
    tier2_count = 0
    geo_match = False

    for kw in profile.get('tier1_keywords', []):
        if kw.lower() in text:
            tier1_count += 1
            matched.append(kw)

    for kw in profile.get('tier2_keywords', []):
        if kw.lower() in text:
            tier2_count += 1
            matched.append(kw)

    for kw in profile.get('geo_keywords', []):
        if kw.lower() in text:
            geo_match = True
            matched.append(kw)

    tier1_min = int(profile.get('tier1_minimum', 2))
    if tier1_count < tier1_min:
        return None

    raw_score = (tier1_count * 10) + (tier2_count * 5) + (15 if geo_match else 0)
    return raw_score, matched


def lambda_handler(event, context):
    api_key = get_serpapi_key()
    profiles = get_active_profiles()

    if not profiles:
        print("No active profiles found!")
        return {'statusCode': 200, 'body': json.dumps({'error': 'no active profiles'})}

    all_stats = {}

    for profile in profiles:
        name = profile['name']
        print(f"\n=== Profile: {name} ===")
        stats = {'searched': 0, 'new': 0, 'skipped': 0, 'filtered': 0}

        for query in profile.get('search_queries', []):
            for location in profile.get('search_locations', []):
                print(f"  Searching: '{query}' in '{location}'")
                stats['searched'] += 1

                try:
                    results = search_jobs(api_key, query, location)
                except Exception as e:
                    print(f"    Error: {e}")
                    continue

                for job in results:
                    job_id = make_job_id(name, job)

                    if job_exists('google_jobs', job_id):
                        stats['skipped'] += 1
                        continue

                    result = score_listing(job, profile)
                    if result is None:
                        stats['filtered'] += 1
                        print(f"    FILTERED: {job.get('title')}")
                        continue

                    raw_score, matched = result
                    write_job('google_jobs', job_id, job, name, raw_score, matched)
                    stats['new'] += 1
                    print(f"    NEW ({raw_score}pts): {job.get('title')} at {job.get('company_name')} | {matched}")

        all_stats[name] = stats
        print(f"  Stats: {stats}")

    print(f"\nAll stats: {all_stats}")
    return {'statusCode': 200, 'body': json.dumps(all_stats)}
import json
import os
import boto3
import time
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

TABLE_NAME = os.environ.get('JOBS_TABLE', 'genai-job-agent-listings')
table = dynamodb.Table(TABLE_NAME)

MODEL_ID = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
MAX_SCORES_PER_RUN = 100


def get_new_listings():
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression='GSI1PK = :status',
        ExpressionAttributeValues={':status': 'STATUS#new'}
    )
    return response['Items']


def get_profile(profile_name):
    response = table.get_item(
        Key={'PK': f'PROFILE#{profile_name}', 'SK': 'CONFIG'}
    )
    return response.get('Item')


def score_with_bedrock(listing, profile):
    prompt = f"""Analyze this job listing for relevance to the following candidate profile.

CANDIDATE PROFILE:
- Name: {profile.get('name', 'Unknown')}
- Target keywords (must match): {', '.join(profile.get('tier1_keywords', []))}
- Preferred keywords (nice to have): {', '.join(profile.get('tier2_keywords', []))}
- Target locations: {', '.join(profile.get('geo_keywords', []))}

JOB LISTING:
- Title: {listing.get('title', '')}
- Company: {listing.get('company', '')}
- Location: {listing.get('location', '')}
- Description: {listing.get('description', '')[:3000]}

Score this listing 1-100 on each dimension:
- role_fit: How well does the title/responsibilities match the candidate?
- seniority_match: Is the seniority level appropriate?
- genai_relevance: How central is GenAI/AI/ML to the role?
- geographic_match: Does the location match target areas?
- industry_match: Is this in the right industry?

Also provide:
- overall_score: Weighted average (role_fit 30%, genai_relevance 25%, seniority_match 20%, industry_match 15%, geographic_match 10%)
- summary: One paragraph explaining why this is or isn't a good match.

Return ONLY valid JSON, no markdown, no backticks:
{{"role_fit": 0, "seniority_match": 0, "genai_relevance": 0, "geographic_match": 0, "industry_match": 0, "overall_score": 0, "summary": ""}}"""

    body = json.dumps({
        'anthropic_version': 'bedrock-2023-05-31',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 500,
        'temperature': 0
    })

    response = bedrock.invoke_model(modelId=MODEL_ID, body=body, contentType='application/json')
    result = json.loads(response['body'].read())
    text = result['content'][0]['text']

    return json.loads(text)


def update_listing_score(listing, scores):
    table.update_item(
        Key={'PK': listing['PK'], 'SK': listing['SK']},
        UpdateExpression='SET GSI1PK = :status, bedrock_score = :score, score_details = :details, summary = :summary, scored_at = :ts',
        ExpressionAttributeValues={
            ':status': 'STATUS#scored',
            ':score': int(scores['overall_score']),
            ':details': {
                'role_fit': int(scores['role_fit']),
                'seniority_match': int(scores['seniority_match']),
                'genai_relevance': int(scores['genai_relevance']),
                'geographic_match': int(scores['geographic_match']),
                'industry_match': int(scores['industry_match']),
            },
            ':summary': scores['summary'],
            ':ts': datetime.now().isoformat()
        }
    )


def lambda_handler(event, context):
    listings = get_new_listings()
    stats = {'total': len(listings), 'scored': 0, 'errors': 0}

    for listing in listings[:MAX_SCORES_PER_RUN]:
        profile = get_profile(listing.get('profile', 'chris'))
        if not profile:
            print(f"  No profile found for {listing.get('profile')}")
            stats['errors'] += 1
            continue

        try:
            print(f"Scoring: {listing['title']} at {listing['company']}")
            scores = score_with_bedrock(listing, profile)
            update_listing_score(listing, scores)
            stats['scored'] += 1
            print(f"  Score: {scores['overall_score']} - {scores['summary'][:80]}...")
        except KeyError as e:
            print(f"  Bad response format: {e}")
            stats['errors'] += 1
        except Exception as e:
            print(f"  Error scoring: {e}")
            stats['errors'] += 1

        time.sleep(2)  # avoid throttling

    print(f"\nResults: {stats}")
    return {'statusCode': 200, 'body': json.dumps(stats)}
import boto3
from datetime import datetime, timedelta
import time

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')

# --- WRITE sample listings ---

sample_jobs = [
    {
        'PK': 'SOURCE#indeed',
        'SK': 'JOB#ind-001',
        'GSI1PK': 'STATUS#new',
        'GSI1SK': f'DATE#{datetime.now().strftime("%Y-%m-%d")}',
        'title': 'Senior Security Architect - GenAI',
        'company': 'JPMorgan Chase',
        'location': 'Miami, FL',
        'url': 'https://indeed.com/jobs/ind-001',
        'description': 'Lead security architecture for generative AI applications in our digital banking division...',
        'keywords_matched': ['genai', 'security', 'architect'],
        'first_seen': datetime.now().isoformat(),
        'last_seen': datetime.now().isoformat(),
        'ttl': int((datetime.now() + timedelta(days=90)).timestamp())
    },
    {
        'PK': 'SOURCE#linkedin',
        'SK': 'JOB#lin-001',
        'GSI1PK': 'STATUS#new',
        'GSI1SK': f'DATE#{datetime.now().strftime("%Y-%m-%d")}',
        'title': 'Cloud Security Engineer',
        'company': 'Fidelity Investments',
        'location': 'Jacksonville, FL',
        'url': 'https://linkedin.com/jobs/lin-001',
        'description': 'Design and implement cloud security controls for AWS workloads...',
        'keywords_matched': ['cloud', 'security', 'aws'],
        'first_seen': datetime.now().isoformat(),
        'last_seen': datetime.now().isoformat(),
        'ttl': int((datetime.now() + timedelta(days=90)).timestamp())
    },
    {
        'PK': 'SOURCE#indeed',
        'SK': 'JOB#ind-002',
        'GSI1PK': 'STATUS#scored',
        'GSI1SK': f'DATE#{datetime.now().strftime("%Y-%m-%d")}',
        'title': 'VP, AI Security Operations',
        'company': 'Citizens Financial',
        'location': 'Melbourne, FL',
        'url': 'https://indeed.com/jobs/ind-002',
        'description': 'Oversee security for AI/ML initiatives across the enterprise...',
        'score': 92,
        'keywords_matched': ['ai', 'security', 'vp', 'financial'],
        'first_seen': datetime.now().isoformat(),
        'last_seen': datetime.now().isoformat(),
        'ttl': int((datetime.now() + timedelta(days=90)).timestamp())
    }
]

print("--- Writing sample listings ---")
for job in sample_jobs:
    table.put_item(Item=job)
    print(f"  Wrote: {job['title']} ({job['PK']} / {job['SK']})")

# --- READ by source (primary key) ---

print("\n--- Query: All Indeed listings ---")
response = table.query(
    KeyConditionExpression='PK = :pk',
    ExpressionAttributeValues={':pk': 'SOURCE#indeed'}
)
for item in response['Items']:
    print(f"  {item['title']} at {item['company']}")

# --- READ by status via GSI ---

print("\n--- Query: All NEW listings (via GSI1) ---")
response = table.query(
    IndexName='GSI1',
    KeyConditionExpression='GSI1PK = :status',
    ExpressionAttributeValues={':status': 'STATUS#new'}
)
for item in response['Items']:
    print(f"  {item['title']} at {item['company']} - {item['location']}")

# --- READ by status = scored via GSI ---

print("\n--- Query: All SCORED listings (via GSI1) ---")
response = table.query(
    IndexName='GSI1',
    KeyConditionExpression='GSI1PK = :status',
    ExpressionAttributeValues={':status': 'STATUS#scored'}
)
for item in response['Items']:
    print(f"  {item['title']} - Score: {item.get('score', 'N/A')}")

# --- DEDUP check (direct GetItem) ---

print("\n--- Dedup check: Does JOB#ind-001 exist? ---")
response = table.get_item(
    Key={'PK': 'SOURCE#indeed', 'SK': 'JOB#ind-001'}
)
exists = 'Item' in response
print(f"  Exists: {exists}")
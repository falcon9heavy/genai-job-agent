# tests/count_status.py
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')

for status in ['new', 'scored', 'notified']:
    r = table.query(
        IndexName='GSI1',
        KeyConditionExpression='GSI1PK = :s',
        ExpressionAttributeValues={':s': f'STATUS#{status}'}
    )
    print(f"STATUS#{status}: {len(r['Items'])}")
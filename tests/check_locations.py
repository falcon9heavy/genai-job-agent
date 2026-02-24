# tests/check_locations.py
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')

r = table.query(
    IndexName='GSI1',
    KeyConditionExpression='GSI1PK = :s',
    ExpressionAttributeValues={':s': 'STATUS#new'}
)

for item in sorted(r['Items'], key=lambda x: x.get('title', '')):
    print(f"{item.get('location', 'N/A'):40} | {item.get('title', '')}")
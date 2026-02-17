import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')

response = table.query(
    IndexName='GSI1',
    KeyConditionExpression='GSI1PK = :status',
    ExpressionAttributeValues={':status': 'STATUS#new'}
)

print(f"Found {len(response['Items'])} items still with STATUS#new")
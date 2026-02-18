import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')

response = table.query(
    IndexName='GSI1',
    KeyConditionExpression='GSI1PK = :status',
    ExpressionAttributeValues={':status': 'STATUS#scored'}
)

count = 0
for item in response['Items']:
    table.update_item(
        Key={'PK': item['PK'], 'SK': item['SK']},
        UpdateExpression='SET GSI1PK = :status REMOVE bedrock_score, score_details, summary, scored_at',
        ExpressionAttributeValues={':status': 'STATUS#new'}
    )
    count += 1

print(f"Reset {count} listings to STATUS#new")
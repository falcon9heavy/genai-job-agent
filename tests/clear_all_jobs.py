import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')

for status in ['new', 'scored', 'notified']:
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression='GSI1PK = :s',
        ExpressionAttributeValues={':s': f'STATUS#{status}'}
    )
    for item in response['Items']:
        table.delete_item(Key={'PK': item['PK'], 'SK': item['SK']})
        print(f"Deleted: {item.get('title', 'unknown')}")

print("Done")
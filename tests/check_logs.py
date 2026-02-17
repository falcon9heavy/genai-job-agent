import boto3

logs = boto3.client('logs', region_name='us-east-1')

streams = logs.describe_log_streams(
    logGroupName='/aws/lambda/genai-job-agent-ScorerFunction-LwO21hg82tdE',
    orderBy='LastEventTime',
    descending=True,
    limit=1
)

stream_name = streams['logStreams'][0]['logStreamName']
print(f"Stream: {stream_name}")

events = logs.get_log_events(
    logGroupName='/aws/lambda/genai-job-agent-ScorerFunction-LwO21hg82tdE',
    logStreamName=stream_name,
    limit=30
)

for event in events['events']:
    print(event['message'])
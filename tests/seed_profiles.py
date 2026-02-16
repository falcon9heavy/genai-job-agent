import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')

profiles = [
    {
        'PK': 'PROFILE#chris',
        'SK': 'CONFIG',
        'name': 'chris',
        'active': True,
        'search_queries': [
            'generative AI security architect',
            'GenAI application security financial services',
            'AI security architect AWS',
            'LLM security engineer',
        ],
        'search_locations': [
            'Miami, FL',
            'Fort Lauderdale, FL',
            'Melbourne, FL',
            'Remote',
        ],
        'tier1_keywords': [
            'generative ai', 'genai', 'gen ai', 'llm', 'large language model',
            'ai security', 'ml security', 'bedrock', 'ai governance',
        ],
        'tier2_keywords': [
            'financial services', 'banking', 'fintech', 'production approval',
            'security architect', 'principal', 'vanguard', 'fidelity',
            'jpmorgan', 'citi', 'wells fargo',
        ],
        'geo_keywords': [
            'miami', 'fort lauderdale', 'broward', 'palm beach',
            'melbourne', 'brevard', 'cocoa beach', 'space coast',
            'remote', 'hybrid',
        ],
        'exclusions': [
            'junior', 'entry-level', 'entry level', 'intern',
            'contract', 'temporary', 'temp ',
        ],
        'tier1_minimum': 2,
    },
]

for profile in profiles:
    table.put_item(Item=profile)
    print(f"Seeded profile: {profile['name']}")
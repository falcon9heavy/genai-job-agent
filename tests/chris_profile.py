import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')

profiles = [
    {
        'PK': 'PROFILE#chris',
        'SK': 'CONFIG',
        'name': 'chris',
        'require_geo_match': True,
        'active': True,
        'search_queries': [
            'security architect',
            'cyber security engineer',
            'GenAI application security engineer',
            'AI security architect AWS',
            'LLM security engineer',
        ],
        'target_companies': [
            # Financial Services / Investment
            'JPMorgan', 'Citi', 'Bank of America', 'Wells Fargo',
            'Goldman Sachs', 'Morgan Stanley', 'Fidelity',
            'Charles Schwab', 'Raymond James', 'BlackRock',
            'State Street', 'BNY Mellon', 'Capital One',
            'American Express', 'Visa', 'Mastercard',
            'Regions Financial', 'TD Bank', 'PNC',
            'Citadel', 'Two Sigma', 'Renaissance Technologies',
            # Wall Street South - Hedge Funds & Private Equity
            'Elliott Management', 'Point72', 'Apollo Global',
            'D1 Capital', 'Thoma Bravo', 'Millennium Management',
            'Balyasny', 'Schonfeld', 'ExodusPoint',
            'Aurelius Capital', 'Starwood Capital', 'Icahn Enterprises',
            'Bessemer Trust', 'Baron Funds', 'Paulson Capital',
            'Blackstone', 'CI Financial', 'Virtu Financial',
            'Ark Invest', 'DoubleLine Capital',
            # Aerospace & Defense
            'L3Harris', 'Lockheed Martin', 'Northrop Grumman',
            'Raytheon', 'Boeing', 'General Dynamics',
            'BAE Systems', 'Leidos', 'SAIC', 'Booz Allen',
            # Space Coast Aerospace
            'SpaceX', 'Blue Origin', 'United Launch Alliance',
            'Sierra Space', 'Firefly Aerospace', 'Relativity Space',
            'Stoke Space', 'Leonardo DRS', 'Embraer',
            'Collins Aerospace', 'Rocket Lab', 'Jacobs Engineering',
            'Extant Aerospace',
            # Cybersecurity
            'CrowdStrike', 'Palo Alto Networks', 'Fortinet',
            'SentinelOne', 'Zscaler', 'Rapid7', 'Tenable',
            'Mandiant', 'Trellix', 'Arctic Wolf', 'Varonis',
            'Okta', 'CyberArk', 'Proofpoint', 'Palantir',
            'Elastic', 'Splunk', 'Cloudflare',
            # Big Tech (GenAI heavy)
            'Amazon', 'Microsoft', 'Google', 'Meta', 'Apple',
            'Anthropic', 'OpenAI', 'Nvidia',
        ],
        'search_locations': [
            'Fort Lauderdale, FL',
            'Melbourne, FL',
            'Boca Raton, FL',
            'Miami, FL',
            'West Palm Beach, FL',
            'Remote',
        ],
        'tier1_keywords': [
            'architect', 'genai', 'gen ai', 'security', 'large language model',
            'ai security', 'engineer', 'bedrock', 'cyber', 'cybersecurity', 'data security',
        ],
        'tier2_keywords': [
            'generative ai', 'genai', 'llm', 'ai security',
            'bedrock', 'ai governance', 'machine learning',
            'financial services', 'banking', 'principal',
            'cloud security', 'aws', 'azure', 'gcp', 'google cloud',
        ],
        'geo_keywords': [
            # South Florida - Miami / Brickell / Wall Street South
            'miami', 'coral gables', 'doral', 'brickell', 'hialeah',
            'miami-dade', 'miami dade', 'coconut grove', 'key biscayne',
            'wynwood', 'downtown miami',
            'fort lauderdale', 'broward', 'hollywood, fl',
            'boca raton', 'delray beach', 'boynton beach',
            'palm beach', 'west palm beach', 'jupiter',
            'palm beach gardens',
            # Treasure Coast
            'port st. lucie', 'port saint lucie', 'stuart', 'vero beach',
            # Space Coast
            'melbourne', 'brevard', 'cocoa beach', 'cocoa, fl',
            'cape canaveral', 'titusville', 'merritt island',
            'space coast', 'palm bay', 'rockledge',
            # General
            'south florida', 'southeast florida',
            'florida', ', fl',
            # Remote
            'remote', 'hybrid', 'anywhere', 'work from home',
        ],
        'exclusions': [
            'junior', 'entry-level', 'entry level', 'intern',
            'contract', 'temporary', 'temp ',
        ],
        'tier1_minimum': 1,
        # Scraper should capture and store these fields per listing
        'capture_fields': [
            'title', 'company', 'location', 'description',
            'source_url', 'apply_url', 'date_posted',
        ],
    },
]

# Upload profiles to DynamoDB
for profile in profiles:
    table.put_item(Item=profile)
    print(f"Uploaded profile: {profile['name']}")

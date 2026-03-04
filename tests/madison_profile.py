import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')

profiles = [
    {
        'PK': 'PROFILE#madison',
        'SK': 'CONFIG',
        'name': 'madison',
        'require_geo_match': False,  # Wide geo net - Philly, NYC, FL, remote
        'active': True,
        'search_queries': [
            'iOS developer Swift',
            'mobile software engineer',
            'SwiftUI developer',
            'AI ML engineer iOS',
        ],
        'target_companies': [
            # Big Tech
            'Apple', 'Google', 'Meta', 'Amazon', 'Microsoft',
            'Netflix', 'Spotify', 'Uber', 'Lyft', 'Airbnb',
            # Finance (Philly / NYC / FL)
            'JPMorgan', 'Goldman Sachs', 'Citi', 'Capital One',
            'Bloomberg', 'Fidelity', 'Vanguard', 'BlackRock',
            'Robinhood', 'Coinbase', 'Block', 'Stripe',
            # Health Tech / Med Tech
            'Comcast', 'Johnson & Johnson', 'Merck',
            'CVS Health', 'Independence Blue Cross',
            # iOS-heavy companies
            'Peloton', 'DoorDash', 'Instacart', 'Pinterest',
            'Snap', 'Reddit', 'Discord', 'Slack',
            'Duolingo', 'Calm', 'Headspace',
            # Defense / Aerospace (familiar from Dad)
            'Lockheed Martin', 'L3Harris', 'Northrop Grumman',
            'Raytheon', 'Leidos', 'Booz Allen',
            # Consulting / Enterprise
            'Accenture', 'Deloitte', 'IBM',
            'SAP', 'Salesforce', 'Oracle',
            # Philly-area tech
            'Comcast NBCUniversal', 'Susquehanna International Group',
            'Vertex Inc', 'SEI Investments', 'Bentley Systems',
            'InvisALERT Solutions',
        ],
        'search_locations': [
            'New York, NY',
            'Jersey City, NJ',
            'Philadelphia, PA',
            'Remote',
        ],
        'tier1_keywords': [
            'ios', 'swift', 'swiftui', 'uikit', 'mobile',
            'iphone', 'ipad', 'xcode', 'apple',
            'software engineer', 'software developer',
            'ai', 'machine learning', 'ml engineer',
        ],
        'tier2_keywords': [
            'mvvm', 'core data', 'combine', 'async await',
            'rest api', 'figma', 'agile', 'scrum',
            'python', 'tensorflow', 'pytorch', 'nlp',
            'computer vision', 'deep learning',
            'react native', 'flutter', 'cross-platform',
        ],
        'geo_keywords': [
            # New York City
            'new york', 'nyc', 'manhattan', 'brooklyn',
            'queens', 'bronx', 'staten island',
            # North Jersey
            'jersey city', 'hoboken', 'newark, nj',
            'weehawken', 'edgewater', 'fort lee',
            'morristown', 'parsippany', 'florham park',
            'summit', 'short hills', 'montclair',
            # Philadelphia metro
            'philadelphia', 'philly', 'west chester', 'king of prussia',
            'conshohocken', 'blue bell', 'malvern',
            'chester county', 'montgomery county',
            # Remote
            'remote', 'hybrid', 'anywhere', 'work from home',
        ],
        'exclusions': [
            'intern', 'internship',
            'contract', 'temporary', 'temp ',
            'principal', 'staff engineer', 'director',
            'vp ', 'vice president',
        ],
        'tier1_minimum': 1,
    },
]

for profile in profiles:
    table.put_item(Item=profile)
    print(f"Seeded profile: {profile['name']}")
    print(f"  Queries: {len(profile['search_queries'])}")
    print(f"  Locations: {len(profile['search_locations'])}")
    print(f"  Searches per run: {len(profile['search_queries']) * len(profile['search_locations'])}")

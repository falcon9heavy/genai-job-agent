import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('genai-job-agent-listings')
profiles = [
    {
        'PK': 'PROFILE#madison',
        'SK': 'CONFIG',
        'name': 'madison',
        'email': 'madison.k.adams@gmail.com',
        'require_geo_match': False,
        'active': True,
        'search_queries': [
            # iOS / Mobile
            'iOS developer Swift',
            'mobile software engineer',
            'SwiftUI developer',
            # AI/ML
            'AI ML engineer iOS',
            'machine learning engineer Python',
            # Full-stack (new from her profile)
            'full stack developer Python JavaScript',
            # São Paulo - Portuguese queries
            'desenvolvedor iOS Swift São Paulo',
            'engenheiro machine learning São Paulo',
        ],
        'target_companies': [
            # Big Tech
            'Apple', 'Google', 'Meta', 'Amazon', 'Microsoft',
            'Netflix', 'Spotify', 'Uber', 'Lyft', 'Airbnb',
            'Nvidia', 'Anthropic', 'OpenAI',
            # Finance / FinTech
            'JPMorgan', 'Goldman Sachs', 'Citi', 'Capital One',
            'Bloomberg', 'Fidelity', 'Vanguard', 'BlackRock',
            'Robinhood', 'Coinbase', 'Block', 'Stripe',
            'Plaid', 'Ramp', 'Betterment', 'Kalshi', 'Bilt',
            'Two Sigma', 'Citadel', 'DE Shaw',
            'Morgan Stanley', 'BNY Mellon', 'Deutsche Bank',
            # Health Tech
            'Johnson & Johnson', 'Merck', 'Pfizer',
            'CVS Health', 'Independence Blue Cross',
            'Tempus', 'Flatiron Health', 'Oscar Health',
            # iOS-heavy / Consumer
            'Peloton', 'DoorDash', 'Instacart', 'Pinterest',
            'Snap', 'Reddit', 'Discord', 'Slack',
            'Duolingo', 'Calm', 'Headspace',
            'Squarespace', 'Etsy',
            # Mid-size / Growth Startups
            'Datadog', 'MongoDB', 'Atlassian',
            'Figma', 'Notion', 'Linear', 'Vercel',
            # Consulting (she's talking to Accenture already)
            'Accenture', 'Deloitte', 'IBM',
            'SAP', 'Salesforce', 'Oracle',
            # Media
            'NBCUniversal', 'New York Times', 'Conde Nast',
            # Philly-area
            'Comcast', 'Susquehanna International Group',
            'Vertex Inc', 'SEI Investments', 'Bentley Systems',
            'InvisALERT Solutions',
            # Miami / South FL
            'Magic Leap', 'Chewy', 'Citrix',
            'World Fuel Services', 'Kaseya',
            # São Paulo / Brazil
            'Nubank', 'iFood', 'PagSeguro', 'Stone',
            'Mercado Libre', 'VTEX', 'Loft',
            'C6 Bank', 'Inter', 'Creditas',
        ],
        'search_locations': [
            'New York, NY',
            'Philadelphia, PA',
            'Miami, FL',
            'São Paulo, Brazil',
            'Remote',
        ],
        'tier1_keywords': [
            'ios', 'swift', 'swiftui', 'uikit', 'mobile',
            'iphone', 'ipad', 'xcode', 'apple',
            'software engineer', 'software developer',
            'full stack', 'fullstack',
            'ai', 'machine learning', 'ml engineer',
            'deep learning',
        ],
        'tier2_keywords': [
            'mvvm', 'core data', 'combine', 'async await',
            'rest api', 'figma', 'agile', 'scrum',
            'python', 'tensorflow', 'pytorch', 'nlp',
            'computer vision', 'deep learning',
            'react native', 'flutter', 'cross-platform',
            'backend', 'java', 'devops', 'ci/cd',
            'jenkins', 'docker', 'kubernetes',
        ],
        'geo_keywords': [
            # New York City
            'new york', 'nyc', 'manhattan', 'brooklyn',
            'queens', 'bronx', 'staten island',
            # Philadelphia metro
            'philadelphia', 'philly', 'west chester', 'king of prussia',
            'conshohocken', 'blue bell', 'malvern',
            'chester county', 'montgomery county',
            # Miami / South Florida
            'miami', 'fort lauderdale', 'boca raton',
            'west palm beach', 'doral', 'coral gables',
            'south florida',
            # São Paulo
            'são paulo', 'sao paulo', 'sp', 'brasil', 'brazil',
            'faria lima', 'pinheiros', 'vila olímpia',
            # Remote
            'remote', 'hybrid', 'anywhere', 'work from home',
        ],
        'exclusions': [
            # Level filters
            'intern', 'internship',
            'contract', 'temporary', 'temp ',
            'principal', 'staff engineer', 'director',
            'vp ', 'vice president', 'senior staff',
            # Dealbreakers from Madison
            'defense', 'defence', 'military', 'dod ', 'department of defense',
            'security clearance', 'ts/sci', 'secret clearance',
            'drug test', 'drug screen', 'pre-employment screening',
            'lockheed', 'northrop', 'raytheon', 'l3harris',
            'leidos', 'booz allen', 'bae systems',
        ],
        'salary_range': {
            'min': 95000,
            'target': 115000,
            'max': 130000,
        },
        'tier1_minimum': 1,
    },
]
for profile in profiles:
    table.put_item(Item=profile)
    print(f"Seeded profile: {profile['name']}")
    print(f"  Queries: {len(profile['search_queries'])}")
    print(f"  Locations: {len(profile['search_locations'])}")
    print(f"  Searches per run: {len(profile['search_queries']) * len(profile['search_locations'])}")

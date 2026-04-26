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
            # iOS / Mobile (can be senior)
            'iOS developer Swift',
            'mobile software engineer',
            'SwiftUI developer',
            'senior iOS developer SwiftUI',
            # AI/ML (junior/mid focus)
            'junior AI engineer',
            'junior machine learning engineer',
            'AI ML engineer Python',
            'machine learning engineer entry level',
            'deep learning engineer PyTorch',
            'AI engineer LLM',
            # Full-stack
            'full stack developer Python JavaScript',
            # Finance specific
            'software engineer fintech',
            'software developer hedge fund',
            # São Paulo - Portuguese queries
            'desenvolvedor iOS Swift São Paulo',
            'engenheiro machine learning São Paulo',
            'engenheiro inteligencia artificial junior São Paulo',
        ],
        'target_companies': [
            # Big Tech
            'Apple', 'Google', 'Meta', 'Amazon', 'Microsoft',
            'Netflix', 'Spotify', 'Uber', 'Lyft', 'Airbnb',
            'Nvidia', 'Anthropic', 'OpenAI',
            # AI / ML Companies
            'DeepMind', 'Cohere', 'Mistral AI', 'Hugging Face',
            'Scale AI', 'Runway', 'Stability AI', 'Weights & Biases',
            'Cerebras', 'Inflection AI', 'Adept AI',
            'Character AI', 'Perplexity', 'Jasper AI',
            'DataRobot', 'H2O.ai', 'Lightning AI',
            'Replicate', 'Modal', 'Anyscale',
            # Finance / FinTech
            'JPMorgan', 'Goldman Sachs', 'Citi', 'Capital One',
            'Bloomberg', 'Fidelity', 'Vanguard', 'BlackRock',
            'Robinhood', 'Coinbase', 'Block', 'Stripe',
            'Plaid', 'Ramp', 'Betterment', 'Kalshi', 'Bilt',
            'Morgan Stanley', 'BNY Mellon', 'Deutsche Bank',
            # Wall Street North / NYC Hedge Funds & Investment
            'Two Sigma', 'Citadel', 'DE Shaw',
            'Bridgewater Associates', 'Renaissance Technologies',
            'Jane Street', 'Hudson River Trading',
            'Susquehanna International Group', 'Tower Research',
            'Jump Trading', 'Virtu Financial',
            'AQR Capital', 'Man Group', 'PDT Partners',
            'WorldQuant', 'Trexquant', 'Squarepoint Capital',
            'Marshall Wace', 'Brevan Howard',
            'Anchorage Digital', 'Paxos',
            # NYC Investment Banks & Asset Managers
            'Lazard', 'Jefferies', 'Evercore',
            'KKR', 'Apollo Global', 'Ares Management',
            'Carlyle Group', 'Warburg Pincus',
            'Tiger Global', 'Coatue Management',
            'Interactive Brokers', 'Tradeweb',
            # NYC FinTech
            'Brex', 'Adyen', 'Marqeta', 'Toast',
            'Chime', 'SoFi', 'Lemonade', 'Oscar Health',
            'Paxos', 'Fireblocks', 'Figure',
            # Health Tech
            'Johnson & Johnson', 'Merck', 'Pfizer',
            'CVS Health', 'Independence Blue Cross',
            'Tempus', 'Flatiron Health', 'Oscar Health',
            # iOS-heavy / Consumer
            'Peloton', 'DoorDash', 'Instacart', 'Pinterest',
            'Snap', 'Reddit', 'Discord', 'Slack',
            'Duolingo', 'Calm', 'Headspace',
            'Squarespace', 'Etsy',
            # Mid-size / Growth Tech
            'Datadog', 'MongoDB', 'Atlassian',
            'Figma', 'Notion', 'Linear', 'Vercel',
            'Palantir', 'Snowflake', 'Databricks',
            'Cloudflare', 'HashiCorp', 'Cockroach Labs',
            'Cockroach Labs', 'JFrog', 'Grafana Labs',
            # NYC Tech
            'Etsy', 'Squarespace', 'Shutterstock',
            'Vimeo', 'ZocDoc', 'Oscar Health',
            'Compass', 'Justworks', 'Spring Health',
            'Ro', 'Hims & Hers', 'K Health',
            # Consulting (she's talking to Accenture already)
            'Accenture', 'Deloitte', 'IBM',
            'SAP', 'Salesforce', 'Oracle',
            # Media
            'NBCUniversal', 'New York Times', 'Conde Nast',
            # Wall Street South / Miami Hedge Funds & Finance
            'Citadel Securities', 'Point72', 'Millennium',
            'Schonfeld', 'Balyasny', 'ExodusPoint',
            'Verition', 'Walleye', 'Thoma Bravo',
            'Starwood Capital', 'CI Financial',
            'Blackstone', 'Elliott Management',
            # South FL Tech / FinTech / Consumer
            'Magic Leap', 'Chewy', 'Citrix',
            'World Fuel Services', 'Kaseya',
            'aXpire', 'Mastercard Miami',
            'Watsco', 'NextEra Energy',
            'Royal Caribbean', 'Carnival Corporation',
            'Ultimate Software', 'Perk',
            # Florida FinTech / Tech
            'AgileEngine', 'Canoe Intelligence', 'Narmi',
            'Flywire', 'AppZen', 'Alloy',
            'Robosoft Technologies', 'CEX.IO',
            'Grifin', 'AIO Logic', 'Sentora',
            'Bookit', 'Network Capital',
            'MetLife Florida', 'New York Life Florida',
            'Coupa', 'Inspira Financial',
            # Tampa / Orlando Tech
            'ConnectWise', 'ReliaQuest', 'KnowBe4',
            'Citigroup Tampa', 'USAA Tampa', 'JPMorgan Tampa',
            # São Paulo / Brazil
            'Nubank', 'iFood', 'PagSeguro', 'Stone',
            'Mercado Libre', 'VTEX', 'Loft',
            'C6 Bank', 'Inter', 'Creditas',
        ],
        'search_locations': [
            'New York, NY',
            'Miami, FL',
            'Fort Lauderdale, FL',
            'Boca Raton, FL',
            'West Palm Beach, FL',
            'Tampa, FL',
            'São Paulo, Brazil',
            'Remote',
        ],
        'tier1_keywords': [
            'ios', 'swift', 'swiftui', 'uikit', 'mobile',
            'iphone', 'ipad', 'xcode', 'apple',
            'software engineer', 'software developer',
            'full stack', 'fullstack',
            'ai', 'artificial intelligence', 'machine learning', 'ml engineer',
            'deep learning', 'neural network', 'llm', 'large language model',
            'generative ai', 'genai', 'nlp', 'computer vision',
            'pytorch', 'tensorflow', 'hugging face', 'transformers',
        ],
        'tier2_keywords': [
            'mvvm', 'core data', 'combine', 'async await',
            'rest api', 'figma', 'agile', 'scrum',
            'python', 'tensorflow', 'pytorch', 'nlp',
            'computer vision', 'deep learning',
            'react native', 'flutter', 'cross-platform',
            'backend', 'java', 'devops', 'ci/cd',
            'jenkins', 'docker', 'kubernetes',
            'fine-tuning', 'embeddings', 'rag', 'vector database',
            'langchain', 'prompt engineering', 'mlops',
            'data pipeline', 'bigquery', 'spark',
            'reinforcement learning', 'gan', 'diffusion',
        ],
        'geo_keywords': [
            # New York City & surrounding
            'new york', 'nyc', 'manhattan', 'brooklyn',
            'queens', 'bronx', 'staten island',
            'jersey city', 'hoboken', 'newark',
            'weehawken', 'edgewater', 'fort lee',
            'white plains', 'stamford', 'new rochelle',
            # Miami-Dade County
            'miami', 'brickell', 'coral gables', 'coconut grove',
            'doral', 'aventura', 'key biscayne',
            'miami beach', 'south beach', 'wynwood',
            'kendall', 'miami lakes', 'hialeah',
            'miami-dade',
            # Broward County
            'fort lauderdale', 'hollywood, fl', 'plantation',
            'sunrise', 'weston', 'davie',
            'pembroke pines', 'coral springs',
            'deerfield beach', 'pompano beach',
            'broward county',
            # Palm Beach County
            'boca raton', 'delray beach', 'boynton beach',
            'west palm beach', 'palm beach gardens', 'jupiter',
            'palm beach county',
            # General South Florida
            'south florida',
            # Tampa / Orlando / Central FL
            'tampa', 'st. petersburg', 'clearwater',
            'orlando', 'lake mary', 'winter park',
            'jacksonville',
            # São Paulo
            'são paulo', 'sao paulo', 'sp', 'brasil', 'brazil',
            'faria lima', 'pinheiros', 'vila olímpia',
            # Remote
            'remote', 'hybrid', 'anywhere', 'work from home',
        ],
        'exclusions': [
            # Level filters - keep senior OUT for non-iOS
            'intern', 'internship',
            'contract', 'temporary', 'temp ',
            'principal', 'staff engineer', 'director',
            'vp ', 'vice president', 'senior staff',
            'lead architect', 'chief',
            # Dealbreakers from Madison
            'defense', 'defence', 'military', 'dod ', 'department of defense',
            'security clearance', 'ts/sci', 'secret clearance',
            'drug test', 'drug screen', 'pre-employment screening',
            'lockheed', 'northrop', 'raytheon', 'l3harris',
            'leidos', 'booz allen', 'bae systems',
        ],
        # NOTE: Senior iOS/mobile roles are ALLOWED through exclusions.
        # Bedrock scoring prompt should favor junior/entry AI/ML roles
        # but accept mid-to-senior iOS/SwiftUI roles.
        'scoring_guidance': (
            'For AI/ML roles: strongly prefer junior, associate, entry-level, '
            'or mid-level positions. Penalize senior AI/ML roles by 15-20 points. '
            'For iOS/mobile/SwiftUI roles: accept all levels including senior. '
            'Madison has 2+ years iOS experience but is early in her AI/ML journey.'
        ),
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

"""Run the scraper locally to verify it works before deploying as Lambda."""
import sys
sys.path.insert(0, 'scraper')
from app import lambda_handler

result = lambda_handler({}, None)
print(result)
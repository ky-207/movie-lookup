# app/seach_service.py

import os
import json

from dotenv import load_dotenv
import requests

load_dotenv()

#
# INFO INPUTS
#

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
request_url = f"https://omdbapi.com/?t=Iron+Man&apikey={OMDB_API_KEY}"
response = requests.get(request_url)
parsed_response = json.loads(response.text)

print(parsed_response)
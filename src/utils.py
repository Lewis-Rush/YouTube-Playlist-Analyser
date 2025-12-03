import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    api_key = os.environ.get("API_KEY")

    if not api_key:
        raise Exception("No api key found")

    return api_key
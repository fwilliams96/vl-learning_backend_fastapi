import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

API_KEY = os.environ.get("ELEVEN_LABS_API_KEY")
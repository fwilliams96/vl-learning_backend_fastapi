from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

ENVIRONMENT = os.environ.get("ENVIRONMENT")
MONGO_URI = os.environ.get("MONGO_URI")
db_client = MongoClient(MONGO_URI).example

'''if ENVIRONMENT == 'PRODUCTION':
    # Base datos remota
    REMOTE_MONGO_URL = os.environ.get("REMOTE_MONGO_URL")
    db_client = MongoClient(REMOTE_MONGO_URL).ai_teacher
else:
    # Base datos local
    db_client = MongoClient().ai_teacher
'''

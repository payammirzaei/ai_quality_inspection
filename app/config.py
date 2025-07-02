import os
from dotenv import load_dotenv

print("Loading .env file...")
try:
    load_dotenv()
except:
    print("Failed to load .env file, using hardcoded values")

SECRET_KEY = os.getenv("SECRET_KEY") or "your_local_secret_key"
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:root@localhost:5432/ai_enhance"
AZURE_BLOB_CONNECTION_STRING = os.getenv("AZURE_BLOB_CONNECTION_STRING") or "your_azure_blob_connection_string"

print("SECRET_KEY:", SECRET_KEY)
print("DATABASE_URL:", DATABASE_URL)
print("AZURE_BLOB_CONNECTION_STRING:", AZURE_BLOB_CONNECTION_STRING) 
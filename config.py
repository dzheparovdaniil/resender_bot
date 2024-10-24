import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
SOURCE_CHANNEL_ID = os.getenv("SOURCE_CHANNEL_ID")
VK_GROUP_ID = os.getenv("VK_GROUP_ID")
VK_ACCESS_TOKEN =os.getenv("VK_ACCESS_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

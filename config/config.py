import os
from dotenv import load_dotenv
load_dotenv()

CHANNEL_FACEBOOK = int(os.getenv("CHANNEL_FACEBOOK"))  # From ENV file
CHANNEL_TELEGRAM = int(os.getenv("CHANNEL_TELEGRAM"))  # From ENV file
CHANNEL_WEB = int(os.getenv("CHANNEL_WEB"))  # From ENV file
CHANNEL_WHATSAPP = int(os.getenv("CHANNEL_WHATSAPP"))  # From ENV file
CHAT_API_TOKEN = os.getenv("CHAT_API_TOKEN")  # From ENV file
CHAT_API_URL = os.getenv("CHAT_API_URL")  # From ENV file
CHAT_API_INSTANCE = os.getenv("CHAT_API_INSTANCE")  # From ENV file
EBOTIFY_URL = os.getenv("EBOTIFY_URL")  # From ENV file
TENANT_ID = os.getenv("TENANT_ID")  # From ENV file

API_KEY = os.getenv("API_KEY")  # From ENV file
DB_NAME = os.getenv("DB_NAME")   # From ENV file
BOT_NAME = os.getenv("BOT_NAME")   # From ENV file

FB_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")  # From ENV file
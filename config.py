import os

from dotenv import load_dotenv

load_dotenv()

API_KEY_TELEGRAM = os.environ['API_KEY_TELEGRAM']
TG_ADMIN_ID = int(os.environ['TG_ADMIN_ID'])

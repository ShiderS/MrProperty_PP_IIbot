import os

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN_DEV = str(os.getenv("TG_TOKIN_DEV"))

import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_API_KEY = os.getenv("QWEN_API_KEY")
if not TG_TOKEN:
    raise ValueError("Необходимо установить TG_TOKEN в переменных окружения или в .env файле")
if not OPENAI_API_KEY:
    raise ValueError("Необходимо установить QWEN_API_KEY в переменных окружения или в .env файле")


# Настройки базы данных
DB_NAME = "data/db.sqlite"

# Папка для временных файлов
TEMP_IMAGE_FOLDER = "temp_images"
TEMP_DOC_FOLDER = "temp_docs"
OPENAI_VISION_MODEL = "gpt-3.5-turbo"
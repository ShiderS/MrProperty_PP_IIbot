import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TG_TOKEN:
    raise ValueError("Необходимо установить TG_TOKEN в переменных окружения или в .env файле")
if not TOGETHER_API_KEY:
    raise ValueError("Необходимо установить QWEN_API_KEY в переменных окружения или в .env файле")


# Настройки базы данных
DB_NAME = "data/db.sqlite"

# Папка для временных файлов
TEMP_IMAGE_FOLDER = "temp_images"
TEMP_DOC_FOLDER = "temp_docs"
TOGETHER_VISION_MODEL = "Qwen/Qwen2.5-VL-72B-Instruct"
getDescriptionPrompt = "Извлеки весь текст с этого изображения рукописного конспекта. Постарайся сохранить структуру, абзацы и переносы строк, как в оригинале по максимуму."
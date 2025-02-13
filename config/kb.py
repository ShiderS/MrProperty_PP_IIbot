from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_user = [
    [KeyboardButton(text="Обратная связь")],
    [KeyboardButton(text="Распознавание почерка")],
    [KeyboardButton(text="Поиск по фото")],
    [KeyboardButton(text="Анализ одежды")],
    [KeyboardButton(text="Распознавание блюд")],
    [KeyboardButton(text="Помощь")],
]
keyboard_user = ReplyKeyboardMarkup(keyboard=kb_user)

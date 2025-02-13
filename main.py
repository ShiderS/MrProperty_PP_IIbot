import asyncio
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from PIL import Image
from data import db_session
from typing import Optional

from config.config import TG_TOKEN_DEV
from data.user import User
from config.kb import (
    keyboard_user
)

__all__ = []

bot = Bot(TG_TOKEN_DEV)
dp = Dispatcher()

users_in_support = []
in_time = []
in_answer = [False, 0]

flag_pattern_name = False
flag_view_pattern = False


class PhotoState(StatesGroup):
    waiting_for_photo: State = State()
    waiting_for_photo2: State = State()
    waiting_for_photo3: State = State()


class DataForAnswer(CallbackData, prefix="fabnum"):
    action: str
    id: Optional[int] = None


def markup_for_admin_ans(user_id):
    anser_admin_kb = InlineKeyboardBuilder()
    anser_admin_kb.button(text='Ответить', callback_data=DataForAnswer(action="ok", id=user_id))
    anser_admin_kb.button(text='Завершить диалог', callback_data=DataForAnswer(action="cancel", id=user_id))
    anser_admin_kb.adjust(2)
    return anser_admin_kb


def del_last_pattern(message):
    global flag_pattern_name
    if flag_pattern_name:
        flag_pattern_name = False
        patterns_user = DB_SESS.query(Pattern).filter(Pattern.user_id == message.from_user.id)
        last_pattern_id = max(i.pattern_id for i in patterns_user)
        last_pattern_user = DB_SESS.query(Pattern).filter(Pattern.pattern_id == last_pattern_id)
        for p in last_pattern_user:
            if not p.pattern_name:
                DB_SESS.delete(p)
        DB_SESS.commit()


def null_flags():
    global flag_view_pattern
    flag_view_pattern = False


def dir_cleaning(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Ошибка при удалении файла {filename}: {e}")


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> Message:
    del_last_pattern(message)
    null_flags()
    if message.chat.id not in [i.id for i in DB_SESS.query(User).all()]:
        user = User(
            id=message.chat.id,
            full_name=message.from_user.full_name,
            tg_name=message.chat.username
        )
        DB_SESS.add(user)
        DB_SESS.commit()
    text_answer = f"Привет {message.from_user.first_name}"
    await message.answer(text_answer, reply_markup=keyboard_user)


@dp.message(Command("help"))
@dp.message(F.text == "Помощь")
async def help(message: types.Message) -> Message:
    await message.answer("Помощь")


@dp.message(Command("menu"))
@dp.message(F.text == "Меню")
async def menu(message: types.Message) -> Message:
    del_last_pattern(message)
    null_flags()
    await message.answer("Меню", reply_markup=keyboard_user)


# Команда для обращения в поддержку
@dp.message(Command("support"))
@dp.message(F.text == "Обратная связь")
async def support(message: types.Message):
    del_last_pattern(message)
    null_flags()
    if message.from_user.id in [i.id for i in DB_SESS.query(User).filter(User.is_developer).all()]:
        await message.reply("Вы являетесь админом и не можете задавать вопросы.")
    else:
        if message.from_user.id not in users_in_support:
            users_in_support.append(message.from_user.id)
        await message.reply("Введите ваше сообщение для поддержки.")


@dp.message(Command("generate"))
@dp.message(F.text == "")
async def create_stickerpak(message: types.Message) -> Message:
    del_last_pattern(message)
    null_flags()
    await message.answer(
        ""
    )


def create_folder_if_not_exists(folder_name):
    if not os.path.exists(f"faceswap/patterns/{folder_name}"):
        os.makedirs(f"faceswap/patterns/{folder_name}")


async def download_pattern(list_id, pattern_name):
    for i in list_id:
        image_info = await bot.get_file(i)
        image_path = image_info.file_path

        create_folder_if_not_exists(pattern_name)

        output_sticker_path = f"faceswap/patterns/{pattern_name}/{i}.png"

        await bot.download_file(image_path, output_sticker_path)

        with Image.open(output_sticker_path) as img:
            img.save(output_sticker_path)


async def download_image(image_id):
    image_info = await bot.get_file(image_id)
    image_path = image_info.file_path

    output_sticker_path = f"faceswap/inFace/{image_id}.png"

    await bot.download_file(image_path, output_sticker_path)

    with Image.open(output_sticker_path) as img:
        img.save(output_sticker_path)


# -------------------Администратор---------------------------
@dp.message(Command("set_admin"))
async def set_admin(
        message: types.Message,
        command: CommandObject,
):
    if DB_SESS.query(User).filter(User.id == message.from_user.id).first().is_developer:
        if not command.args:
            await message.answer("Вы не ввели никнейм пользователя")
        U = DB_SESS.query(User).filter(User.tg_name == int(command.args)).first()
        U.is_developer = 1
        DB_SESS.commit()
        await message.answer(f"Пользователь {U.tg_name} назначен администратором")
    else:
        await message.answer(f"У вас нет прав, чтобы использовать эту команду")


# -------------------------Поддержка-----------------------------
# @dp.message()
# async def handle_message(message: types.Message):
#     # Проверяем, обратился ли пользователь в поддержку
#     global in_answer, flag_pattern_name, flag_view_pattern
#
#     if in_answer[0]:
#         admin = DB_SESS.query(User).filter(User.id == message.from_user.id).first()
#         admin.workload -= 1
#         DB_SESS.commit()
#         await bot.send_message(in_answer[1], message.text)
#         await message.reply("Ответ отправлен пользователю")
#         users_in_support.remove(in_answer[1])
#         in_time.remove(in_answer[1])
#         in_answer = [False, 0]
#     elif message.from_user.id in users_in_support and message.from_user.id not in in_time:
#         ##################
#         developer_id = sorted(
#             {i.id: i.workload for i in DB_SESS.query(User).filter(User.is_developer).all()}.items(),
#             key=lambda x: x[1])[0][0]
#         admin = DB_SESS.query(User).filter(User.id == developer_id).first()
#         admin.workload += 1
#         DB_SESS.commit()
#         admin_message = f"Пользователь {message.from_user.first_name} задал вопрос: {message.text}"
#         await bot.send_message(developer_id, admin_message, reply_markup=markup_for_admin_ans(message.from_user.id).as_markup())
#         in_time.append(message.from_user.id)
#         ##################
#         await message.reply("Ваше сообщение было передано администратору. Ожидайте ответа.")
#     elif message.from_user.id in in_time:
#         await message.reply("Ваше сообщение было передано администратору. Ожидайте ответа.")
#     else:
#         await message.reply("Простите, я не понимаю вашего сообщения.")
#
#
# @dp.callback_query(DataForAnswer.filter())
# async def callbacks_num_change_fab(callback: types.CallbackQuery, callback_data: DataForAnswer):
#     global in_answer
#     if callback_data.action == "ok":
#         await callback.message.edit_text(f"Напишите текст для ответа:")
#         in_answer = [True, callback_data.id]
#
#     elif callback_data.action == "cancel":
#         admin = DB_SESS.query(User).filter(User.id == callback_data.id).first()
#         admin.workload -= 1
#         DB_SESS.commit()
#         await bot.send_message(callback_data.id, "Вопрос отклонён")
#         await callback.message.edit_text(f"Вопрос отклонён")
#         users_in_support.remove(callback_data.id)
#         in_time.remove(callback_data.id)
#     await callback.answer()
# -----------------------------------------------------------------------------


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    db_session.global_init("db/db.db")
    DB_SESS = db_session.create_session()
    asyncio.run(main())

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
from aiogram import F,types,Bot,Dispatcher
from utils import get_quiz_index,get_user_score,quiz_data,update_quiz_index,update_user_score,get_question


bot = Bot(token='Your api-key')

dp = Dispatcher()

@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_user_score(callback.from_user.id)
    # Отправляем в чат сообщение, что ответ верный
    await callback.message.answer("Верно!")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    current_score += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    await update_user_score(callback.from_user.id,current_score)
    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВаш результат - {current_score} правильных ответов")



@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):


    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_user_score(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    # Отправляем в чат сообщение об ошибке с указанием верного ответа
    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    await update_user_score(callback.from_user.id,current_score)
    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer((f"Это был последний вопрос. Квиз завершен!\nВаш результат - {current_score} правильных ответов"))
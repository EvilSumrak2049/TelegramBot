import aiosqlite
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Как объявить переменную в Python?',
        'options': ['variable x = 5', 'x = 5', 'new x = 5', 'set x = 5'],
        'correct_option': 1
    },
    {
        'question': 'Как вывести текст на экран в Python?',
        'options': ['echo("Hello, World!")', 'print("Hello, World!")', 'display("Hello, World!")', 'output("Hello, World!")'],
        'correct_option': 1
    },
    {
        'question': 'Как проверить, является ли число четным в Python?',
        'options': ['if num % 2 == 0:', 'if num % 2:', 'if num.is_even():', 'if is_even(num):'],
        'correct_option': 0
    },
    {
        'question': 'Какой оператор используется для объединения двух списков в Python?',
        'options': ['merge', 'concat', 'join', '+'],
        'correct_option': 3
    },
    {
        'question': 'Как получить количество элементов в списке?',
        'options': ['len(list)', 'count(list)', 'size(list)', 'elements(list)'],
        'correct_option': 0
    },
    {
        'question': 'Как создать функцию в Python?',
        'options': ['create function my_function:', 'def my_function():', 'function my_function():', 'define my_function():'],
        'correct_option': 1
    },
    {
        'question': 'Какой метод используется для добавления элемента в конец списка?',
        'options': ['append()', 'insert()', 'add()', 'push()'],
        'correct_option': 0
    },
    {
        'question': 'Как проверить, присутствует ли определенный ключ в словаре?',
        'options': ['if key in dictionary:', 'if key.exists(dictionary):', 'if dictionary.has_key(key):', 'if dictionary.include(key):'],
        'correct_option': 0
    },

    # Добавьте другие вопросы
]


async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, score INTEGER)''')
        # Сохраняем изменения
        await db.commit()


async def get_quiz_index(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0




async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()




async def update_user_score(user_id,new_score):
  async with aiosqlite.connect('quiz_bot.db') as db:
    await db.execute(f"INSERT INTO users (user_id, score) VALUES (?,?) ON CONFLICT (user_id) DO UPDATE SET score = excluded.score", (user_id,new_score))
    await db.commit()



async def get_user_score(user_id):
  async with aiosqlite.connect('quiz_bot.db') as db:
    async with db.execute("SELECT score from users WHERE user_id = ?",(user_id,)) as cursor:
      results = await cursor.fetchone()
      if results is not None:
        return results[0]
      else:
        return 0





async def send_keyboard(answer_options, right_answer):
    kb=[[InlineKeyboardButton(text=option,callback_data="right_answer" if option == right_answer else "wrong_answer")] for option in answer_options]
    keyboard=InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard





async def get_question(message, user_id):

    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    #kb = generate_options_keyboard(opts, opts[correct_index])
    kb = await send_keyboard(opts,opts[correct_index])
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)



async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза в 0
    new_score = 0
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await update_user_score(user_id,new_score)
    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)





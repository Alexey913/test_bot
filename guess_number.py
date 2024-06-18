import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '7116164705:AAECUhdUu5bN4hG_LuelHy6evP_vENijEsY'

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Количество попыток, доступных пользователю в игре
ATTEMPTS = 5

# Словарь, в котором будут храниться данные пользователя
users = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

def get_user_id(message: Message) -> int:
    return message.from_user.id

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )

    user_id = get_user_id(message)

    if user_id not in users:
        users[user_id] = {'in_game': False,
                          'secret_number': None,
                          'attempts': None,
                          'total_games': 0,
                          'wins': 0}


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    user_id = get_user_id(message)
    await message.answer(
        f'Всего игр сыграно: {users[user_id]["total_games"]}\n'
        f'Игр выиграно: {users[user_id]["wins"]}'
    )


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    user_id = get_user_id(message)
    if users[user_id]['in_game']:
        users[user_id]['in_game'] = False
        users[user_id]['total_games'] += 1
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    user_id = get_user_id(message)
    if not users[user_id]['in_game']:
        users[user_id]['in_game'] = True
        users[user_id]['secret_number'] = get_random_number()
        users[user_id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    user_id = get_user_id(message)
    if not users[user_id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    user_id = get_user_id(message)
    if users[user_id]['in_game']:
        if int(message.text) == users[user_id]['secret_number']:
            users[user_id]['in_game'] = False
            users[user_id]['total_games'] += 1
            users[user_id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[user_id]['secret_number']:
            users[user_id]['attempts'] -= 1
            await message.answer('Мое число меньше\n'
                                 f'Осталось попыток: {users[user_id]["attempts"]}')
        elif int(message.text) < users[user_id]['secret_number']:
            users[user_id]['attempts'] -= 1
            await message.answer('Мое число больше\n'
                                 f'Осталось попыток: {users[user_id]["attempts"]}')

        if users[user_id]['attempts'] == 0:
            users[user_id]['in_game'] = False
            users[user_id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[user_id]["secret_number"]}\n\nДавайте '
                f'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    user_id = get_user_id(message)
    if users[user_id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )


if __name__ == '__main__':
    dp.run_polling(bot)


    
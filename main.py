# import asyncio
# import logging

# from aiogram import Bot, Dispatcher
# from aiogram.enums.parse_mode import ParseMode
# from aiogram.fsm.storage.memory import MemoryStorage

# from config_reader import config
# from handlers import router


# async def main():
#     # Для записей с типом Secret* необходимо 
#     # вызывать метод get_secret_value(), 
#     # чтобы получить настоящее содержимое вместо '*******'
#     bot = Bot(token=config.bot_token.get_secret_value())
#     dp = Dispatcher(storage=MemoryStorage())
#     dp.include_router(router)
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())

"""
import requests
import time
from pprint import pprint


API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '7116164705:AAECUhdUu5bN4hG_LuelHy6evP_vENijEsY'
TEXT = 'Ура! Классный апдейт!'
MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int


while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')


    time.sleep(1)
    counter += 1
"""

# import requests
# import time


# API_URL = 'https://api.telegram.org/bot'
# API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
# API_DOGS_URL = 'https://random.dog/woof.json'
# API_FOX_URL = 'https://randomfox.ca/floof/'
# BOT_TOKEN = '7116164705:AAECUhdUu5bN4hG_LuelHy6evP_vENijEsY'
# ERROR_TEXT = 'Увы, вся живность спряталась :('

# offset = -2
# counter = 0
# animal_response: requests.Response
# animal_link: str
# animal: str


# while True:
#     print('attempt =', counter)
#     updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

#     if updates['result']:
#         for result in updates['result']:
#             offset = result['update_id']
#             chat_id = result['message']['from']['id']
#             if result['message']['text'] == '/cat':
#                 animal_response = requests.get(API_CATS_URL)
#                 animal = 'cat'
#             elif result['message']['text'] == '/dog':
#                 animal_response = requests.get(API_DOGS_URL)
#                 animal = 'dog'
#             elif result['message']['text'] == '/fox':
#                 animal_response = requests.get(API_FOX_URL)
#                 animal = 'fox'
#             else:
#                 animal_response = requests.get(API_CATS_URL)
#             if animal_response.status_code == 200:
#                 if animal == 'cat':
#                     animal_response = requests.get(API_CATS_URL)
#                     animal_link = animal_response.json()[0]['url']
#                 elif animal == 'dog':
#                     animal_response = requests.get(API_DOGS_URL)
#                     animal_link = animal_response.json()['url']
#                 elif animal == 'fox':
#                     animal_response = requests.get(API_FOX_URL)
#                     animal_link = animal_response.json()['image']
#                 requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={animal_link}')
#             else:
#                 requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

#     time.sleep(1)
#     counter += 1


from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = '7116164705:AAECUhdUu5bN4hG_LuelHy6evP_vENijEsY'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


@dp.message(F.photo)
async def send_photo_echo(message: Message):
    await message.reply_photo(message.photo[0].file_id)


@dp.message(F.content_type == ContentType.AUDIO)
async def send_audio_echo(message: Message):
    await message.answer_audio(message.audio.file_id)

@dp.message(F.content_type == ContentType.VOICE)
async def send_voice_echo(message: Message):
    await message.reply_voice(message.voice.file_id)

@dp.message(F.sticker)
async def send_sticker_echo(message: Message):
    await message.reply_sticker(message.sticker.file_id)


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)




# # Без декораторов
# dp.message.register(process_start_command, Command(commands='start'))
# dp.message.register(process_help_command, Command(commands='help'))
# dp.message.register(send_photo_echo, F.photo)
# dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)



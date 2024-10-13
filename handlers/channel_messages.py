from aiogram import types
from aiogram.dispatcher import FSMContext
from bot import bot
from mistralai import Mistral
from config import MISTRAL_API_KEY


async def forward_channel_messages(message: types.Message):
    message_link = 'https://t.me/c/' + str(message.chat.id) + '/' + str(message.message_id)
    await message.answer(f'линк поста {message_link}')
    if len(message.text) > 490:
          text_thread = rewrite_message(message.text)
    else: 
          text_thread = message.text
    await bot.send_message(chat_id=874188918, text='Пост для публикации в threads ⬇️')
    await bot.send_message(chat_id=874188918, text=text_thread + '\n' + message_link)


def rewrite_message(message):
        api_key = MISTRAL_API_KEY
        model = "mistral-large-latest"

        client = Mistral(api_key=api_key)

        chat_response = client.chat.complete(
            model = model,
            messages = [
                {
                    "role": "user",
                    "content": f"сделай краткий пересказ поста для другой социальной сети 50 до 490 символов в зависимости от длины исходного поста: {message}",
                },
            ]
        )
        return chat_response.choices[0].message.content
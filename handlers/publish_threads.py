from aiogram import types
from bot import bot
from mistralai import Mistral
from config import MISTRAL_API_KEY

async def publish_threads_post(callback_query: types.CallbackQuery):
    message_link = callback_query.data.split(':')[1]
    message_text = callback_query.message.text
    if len(message_text) > 490:
        text_thread = rewrite_message(message_text)
    else:
        text_thread = message_text
    await bot.send_message(chat_id=874188918, text='Пост для публикации в threads ⬇️')
    await bot.send_message(chat_id=874188918, text=text_thread + '\n' + message_link)
    await callback_query.answer("Пост опубликован в Threads")

def rewrite_message(message):
    api_key = MISTRAL_API_KEY
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"""сделай краткий пересказ сообщения для другой социальной сети 
                            от 50 до 490 символов в зависимости от содержания. 
                            сообщение обязательно должно быть не длиннее 490 символов!
                            твоя задача заинтересовать читателя и передать основную суть исходного сообщения. 
                            {message}""",
            },
        ]
    )
    return chat_response.choices[0].message.content

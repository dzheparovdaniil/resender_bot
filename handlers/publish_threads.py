from aiogram import types, F, Router
from bot import bot
from mistralai import Mistral
from config import MISTRAL_API_KEY
from aiogram.types import CallbackQuery

router_threads = Router()
@router_threads.callback_query(F.data == 'publish_threads')
async def publish_threads_post(callback: CallbackQuery):
    print(callback.data)
    if callback.message.caption:
        message_text = callback.message.caption
    else:
        message_text = callback.message.text
    if len(message_text) > 490:
        text_thread = rewrite_message(message_text)
    else:
        text_thread = message_text
    await bot.send_message(chat_id=874188918, text='Пост для публикации в threads ⬇️')
    await bot.send_message(chat_id=874188918, text=text_thread)
    await callback.answer("Софрмирован пост для публикации в Threads")

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

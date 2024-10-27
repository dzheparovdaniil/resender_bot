from aiogram import types, F, Router
from bot import bot
from mistralai import Mistral
from config import MISTRAL_API_KEY, THREADS_ACCESS_TOKEN
from aiogram.types import CallbackQuery
import requests as r
import json
import boto3
import os

session = boto3.session.Session()
s3 = session.client(service_name='s3',endpoint_url='https://storage.yandexcloud.net')

router_threads = Router()
@router_threads.callback_query(F.data == 'publish_threads')
async def publish_threads_post(callback: CallbackQuery):
    if callback.message.caption:
        message_text = callback.message.caption
    else:
        message_text = callback.message.text
    if len(message_text) > 490:
        text_thread = rewrite_message(message_text)
    else:
        text_thread = message_text

    if callback.message.caption:
        print('в посте есть фото')
        file_id = callback.message.photo[-1].file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        # Скачиваем файл
        print('скачиваем файл')
        destination = f"{file_id}.jpg"
        await bot.download_file(file_path, destination)
        s3.upload_file(destination, 'resenderbot-media', destination)
        print('загрузили файл в S3')
        photo_link = 'https://storage.yandexcloud.net/resenderbot-media/' + destination
        print('загрузили файл в S3: ', photo_link)
        photo_id = photo_container(text_thread, photo_link)
        print('сформировали контейнер медиа: ', photo_id)
        post_thread(photo_id)
        print('отправили пост в threads')
        os.remove(destination)
    else:
        text_id = text_container(text_thread)
        post_thread(text_id)
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


def text_container(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {THREADS_ACCESS_TOKEN}'
    }

    response = r.post(f'https://graph.threads.net/me/threads?text={message}&media_type=TEXT', headers=headers)
    response_data = json.loads(response.text)
    return response_data['id']

def photo_container(message, message_url):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {THREADS_ACCESS_TOKEN}'
    }

    response = r.post(f'https://graph.threads.net/me/threads?text={message}&media_type=IMAGE&image_url={message_url}', headers=headers)
    response_data = json.loads(response.text)
    return response_data['id']


def post_thread(container_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {THREADS_ACCESS_TOKEN}'
    }

    response = r.post(f'https://graph.threads.net/me/threads_publish?creation_id={container_id}', headers=headers)
    return response
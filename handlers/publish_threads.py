from aiogram import types, F, Router
from bot import bot
from mistralai import Mistral
from config import MISTRAL_API_KEY, THREADS_ACCESS_TOKEN
from aiogram.types import CallbackQuery
import requests as r
import json
import boto3
import os
from keyboard import keyborad_threads

session = boto3.session.Session()
s3 = session.client(service_name='s3',endpoint_url='https://storage.yandexcloud.net')

router_threads = Router()

@router_threads.callback_query(F.data == 'prepare_threads')
async def prepare_threads_post(callback: CallbackQuery):
    if callback.message.caption:
        message_text = callback.message.caption
    else:
        message_text = callback.message.text
    if len(message_text) > 490:
        text_thread = rewrite_message(message_text)
    else:
        text_thread = message_text
    await callback.answer('')
    await bot.send_message(chat_id=874188918, text='Сформируем пост для публикации в Threads')
    if callback.message.photo:
        await bot.send_photo(chat_id=874188918, caption=text_thread, photo=callback.message.photo[-1].file_id, reply_markup=keyborad_threads)
    else:
        await bot.send_message(chat_id=874188918, text=text_thread, reply_markup=keyborad_threads)


@router_threads.callback_query(F.data == 'rewrite_message')
async def prepare_threads_post(callback: CallbackQuery):
    if callback.message.photo:
        rewrite_text = rewrite_message(callback.message.caption)
        await callback.message.edit_caption(caption=rewrite_text, reply_markup=keyborad_threads)
    else:
        rewrite_text = rewrite_message(callback.message.text)
        await callback.message.edit_text(text=rewrite_text, reply_markup=keyborad_threads)


@router_threads.callback_query(F.data == 'publish_threads')
async def publish_threads_post(callback: CallbackQuery):
    if callback.message.caption:
        text_thread = callback.message.caption
    else:
        text_thread = callback.message.text

    if callback.message.caption:
        file_id = callback.message.photo[-1].file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        # Скачиваем файл
        destination = f"{file_id}.jpg"
        await bot.download_file(file_path, destination)
        s3.upload_file(destination, 'resenderbot-media', destination)
        photo_link = 'https://storage.yandexcloud.net/resenderbot-media/' + destination
        photo_id = photo_container(text_thread, photo_link)
        post_thread(photo_id)
        os.remove(destination)
    else:
        text_id = text_container(text_thread)
        post_thread(text_id)
    await callback.answer("Пост опубликован в Threads")

def rewrite_message(message):
    api_key = MISTRAL_API_KEY
    model = "open-mistral-nemo-2407"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        temperature=0.7,
        messages=[
            {
  "role": "user",
  "content": f"""
    you are a copywriter. summarize the message in 490 characters or less. provide only the summary. make it in Russian.
    do not rephrase narrator's face. 
{message}"""
}, 
{
"role": "user",
  "content": f"""
    ## Summarize:
    In clear and concise language, summarize the key points and themes presented in your answer.
    if the number is greater than 490, summarize the message in 490 characters or less. do not rephrase narrator's face.
    """
}
        ]
    )
    return chat_response.choices[0].message.content



def text_container(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {THREADS_ACCESS_TOKEN}'
    }
    try:
        response = r.post(f'https://graph.threads.net/me/threads?text={message}&media_type=TEXT', headers=headers)
        print(response)
        print(response.text)
        response_data = json.loads(response.text)
    except Exception as e:
        print(e)
    return response_data['id']

def photo_container(message, message_url, is_carousel=False):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {THREADS_ACCESS_TOKEN}'
    }
    if is_carousel:
        is_carousel_param = '&is_carousel=true'
    else:
        is_carousel_param = ''
    response = r.post(f'https://graph.threads.net/me/threads?text={message}&media_type=IMAGE&image_url={message_url}{is_carousel_param}', headers=headers)
    response_data = json.loads(response.text)
    return response_data['id']


def post_thread(container_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {THREADS_ACCESS_TOKEN}'
    }

    response = r.post(f'https://graph.threads.net/me/threads_publish?creation_id={container_id}', headers=headers)
    return response
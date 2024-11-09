from aiogram import types, F, Router
from bot import bot
from config import INST_ACCESS_TOKEN
from aiogram.types import CallbackQuery
import requests as r
import json
import boto3
import os
from keyboard import keyborad_threads

session = boto3.session.Session()
s3 = session.client(service_name='s3',endpoint_url='https://storage.yandexcloud.net')

router_inst = Router()

@router_inst.callback_query(F.data == 'publish_inst')
async def publish_threads_post(callback: CallbackQuery):
    caption = callback.message.caption
    file_id = callback.message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    # Скачиваем файл
    destination = f"{file_id}.jpg"
    await bot.download_file(file_path, destination)
    s3.upload_file(destination, 'resenderbot-media', destination)
    photo_link = 'https://storage.yandexcloud.net/resenderbot-media/' + destination
    print('загрузили фотку:', photo_link)
    photo_id = get_container_id(photo_link,caption)
    print('container id: ',photo_id)
    publish_content(photo_id)
    os.remove(destination)
    await callback.answer("Пост опубликован в Instagram")

def get_container_id(image_url, caption):
        base_url = "https://graph.facebook.com/v21.0/17841404482543324/media"
        params = {
                  "access_token": INST_ACCESS_TOKEN,
                  "image_url" : image_url,
                  "caption" : caption
          }
        response = r.post(base_url, params=params)
        try:
           content_id = json.loads(response.text)['id']
           return content_id
        except Exception as e:
            print(e)
        


def publish_content(creation_id):
        base_url = "https://graph.facebook.com/v21.0/17841404482543324/media_publish"
        params = {
    "creation_id": creation_id,
    "access_token": INST_ACCESS_TOKEN
    }
        response = r.post(base_url, params=params)
        return response.text
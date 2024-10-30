from aiogram import types, F, Router
from bot import bot
from mistralai import Mistral
from aiogram.types import CallbackQuery, Message
from aiogram_media_group import media_group_handler
from keyboard import post_keyboard
import boto3
import os

router_media = Router()

session = boto3.session.Session()
s3 = session.client(service_name='s3',endpoint_url='https://storage.yandexcloud.net')


@router_media.message(F.media_group_id)
@media_group_handler()
async def post_media_group(messages: list[Message]) -> None:
          images = []
          images_links = []
          caption = ""
          for message in messages:
            print(f"command, message_id: {message.message_id}, user_id: {message.from_user.id}, text: {message.caption}, media_group_id: {message.media_group_id}")
            if message.caption != None and caption == "":
                    caption = message.caption
            if message.photo:
                images.append(message.photo[-1].file_id)
                file_id = message.photo[-1].file_id
                photo_link = await upload_photo_s3(file_id)
                images_links.append(photo_link)
          print('images: ', images)
          print('caption: ', caption) 
          print('images_links: ', images_links)         

async def upload_photo_s3(file_id):
      try:
          file = await bot.get_file(file_id)
          file_path = file.file_path
          destination = f"{file_id}.jpg"
          await bot.download_file(file_path, destination)
          s3.upload_file(destination, 'resenderbot-media', destination)
          photo_link = 'https://storage.yandexcloud.net/resenderbot-media/' + destination
          os.remove(destination)
      except Exception as e:
          print(e)    
      return photo_link
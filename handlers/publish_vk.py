from aiogram import types, F, Router
import vk_api
from config import VK_ACCESS_TOKEN, VK_GROUP_ID
import requests
from aiogram.types import CallbackQuery
from log_config import logger
import json
from bot import bot
import os

router = Router()

@router.callback_query(F.text)
async def publish_vk_post_text(callback_query: CallbackQuery):
    try:
        print('обрабатываю текстовый пост')
        vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
        vk = vk_session.get_api()
        vk_post = vk.wall.post(owner_id=-int(VK_GROUP_ID), message=callback_query.message.text, from_group=1)
        await callback_query.answer("Пост опубликован в VK")
        await callback_query.message.answer(f"Пост опубликован в VK: https://vk.com/wall-{VK_GROUP_ID}_{vk_post['post_id']}")
    except Exception as e:
        await callback_query.answer("Ошибка при публикации поста в VK")

@router.callback_query(F.photo)
async def publish_vk_post_photo(callback_query: CallbackQuery):
    try:
        print('обрабатываю пост с фото')
        vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
        vk = vk_session.get_api()
        vk_post = vk.wall.post(owner_id=-int(VK_GROUP_ID), attachments='photo-227832297_457239017', from_group=1)
        await callback_query.answer("Пост опубликован в VK")
        await callback_query.message.answer(f"Пост опубликован в VK: https://vk.com/wall-{VK_GROUP_ID}_{vk_post['post_id']}")
    except Exception as e:
        logger.error(f'Ошибка при отправке поста в vk: {e}')
        await callback_query.answer("Ошибка при публикации поста в VK")

@router.callback_query(F.data == 'publish_vk')
async def publish_vk_post(callback: CallbackQuery):
    try:
        vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
        vk = vk_session.get_api()
        print('обрабатываю сообщение')
        if callback.message.photo:
            file_id = callback.message.photo[-1].file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path

            # Скачиваем файл
            destination = f"{file_id}.jpg"
            await bot.download_file(file_path, destination)
            #file_name = 
            photo_id, owner_id = upload_photo_vk(vk, destination, VK_GROUP_ID)
            if callback.message.caption != None:
                vk_post = vk.wall.post(owner_id=-int(VK_GROUP_ID), message = callback.message.caption, attachments=f'photo{owner_id}_{photo_id}', from_group=1)
                await callback.answer('фото и текст отправлены в vk')
                await callback.message.answer(f"Пост опубликован в VK: https://vk.com/wall-{VK_GROUP_ID}_{vk_post['post_id']}")
            else:
                vk_post = vk.wall.post(owner_id=-int(VK_GROUP_ID), attachments=f'photo{owner_id}_{photo_id}', from_group=1)
                await callback.answer('фото отправлено в vk')
                await callback.message.answer(f"Пост опубликован в VK: https://vk.com/wall-{VK_GROUP_ID}_{vk_post['post_id']}")     
            os.remove(destination)
        else:
            vk_post = vk.wall.post(owner_id=-int(VK_GROUP_ID), message = callback.message.text, from_group=1)
            await callback.answer('текст опубликован в vk')
            await callback.message.answer(f"Пост опубликован в VK: https://vk.com/wall-{VK_GROUP_ID}_{vk_post['post_id']}")
    except Exception as e:
        print(f'ошибка {e}')
        await callback.answer("Ошибка при публикации поста в VK")


def upload_photo_vk(vk, file_name, group_id):
          photo = vk.photos.getWallUploadServer(group_id=group_id)
          upload_url = photo['upload_url']
          with open(file_name, 'rb') as file:
              files = {'photo': file}
              response = requests.post(upload_url, files=files)
          photo_data = json.loads(response.text)
          uploaded_photo = vk.photos.saveWallPhoto(group_id=group_id, server=photo_data['server'], photo=photo_data['photo'], hash=photo_data['hash'])
          photo_id = uploaded_photo[0]['id']
          owner_id = uploaded_photo[0]['owner_id']
          return photo_id, owner_id
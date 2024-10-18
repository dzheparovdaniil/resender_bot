from aiogram import types, F, Router
import vk_api
from config import VK_ACCESS_TOKEN, VK_GROUP_ID
import requests
from aiogram.types import CallbackQuery
from log_config import logger

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
        print('обрабатываю сообщение')
        if callback.message.photo:
            if callback.message.caption != None:
                await callback.answer('в сообщении есть фото и текст')
                print(callback.message.caption)
            else:
                await callback.answer('в сообщении есть только фото')
        else:
            await callback.answer('в сообщении есть только текст')
    except Exception as e:
        print(f'ошибка {e}')
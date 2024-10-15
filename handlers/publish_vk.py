from aiogram import types
from bot import bot
import vk_api
from config import VK_ACCESS_TOKEN, VK_GROUP_ID
from log_config import logger

async def publish_vk_post(callback_query: types.CallbackQuery):
    try:
        message = callback_query.message
        message_text = message.text
        vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
        vk = vk_session.get_api()
        logger.info('отправляю пост в vk')
        vk_post = vk.wall.post(owner_id=-int(VK_GROUP_ID), message=message_text, from_group=1)
        #vk_post = vk.pages.save(group_id=-int(VK_GROUP_ID), text=message_text) - попробовать создавать wiki-страницы с форматированием (нужно разобраться с токеном)
        await callback_query.answer("Пост опубликован в VK")
        await callback_query.message.answer(f"Пост опубликован в VK: https://vk.com/wall-{VK_GROUP_ID}_{vk_post['post_id']}")
    except Exception as e:
        logger.error(f'Ошибка при отправке поста в vk: {e}')
        await callback_query.answer("Ошибка при публикации поста в VK")

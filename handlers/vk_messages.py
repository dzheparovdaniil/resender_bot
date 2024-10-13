from aiogram import types
from bot import bot
import vk_api
from config import VK_ACCESS_TOKEN, VK_GROUP_ID
from log_config import logger

async def vk_post_messages(message: types.Message):
    vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
    vk = vk_session.get_api()
    message_link = 'https://t.me/c/' + str(message.chat.id) + '/' + str(message.message_id)
    await message.answer(f'линк поста {message_link}')
    await bot.send_message(chat_id=874188918, text='Пост для публикации в vk ⬇️')
    await bot.send_message(chat_id=874188918, text=message.text)
    logger.info('отправляю пост в vk')
    vk.wall.post(owner_id=-int(VK_GROUP_ID), message=message.text)

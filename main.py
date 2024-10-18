from aiogram import types
from bot import dp, bot
from handlers import cmd_start, publish_threads_post, publish_vk_post_text, publish_vk_post_photo, send_echo, forward_channel_messages, publish_vk_post
import asyncio
from handlers.publish_vk import router

async def main():
    #dp.message.register(cmd_start, commands=['start'])
    dp.channel_post.register(forward_channel_messages)
    dp.message.register(send_echo)
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
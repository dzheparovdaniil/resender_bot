from aiogram import types
from bot import dp, bot
from handlers import cmd_start, forward_channel_messages, publish_threads_post, publish_vk_post, send_echo
import asyncio

async def main():
    #dp.message.register(cmd_start, commands=['start'])
    dp.channel_post.register(forward_channel_messages)
    dp.callback_query.register(publish_threads_post, lambda c: c.data.startswith('publish_threads'))
    dp.callback_query.register(publish_vk_post, lambda c: c.data.startswith('publish_vk'))
    dp.message.register(send_echo)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
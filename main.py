from aiogram import executor, types
from bot import dp
from handlers import cmd_start, forward_channel_messages, vk_post_messages

if __name__ == '__main__':
    dp.register_message_handler(cmd_start, commands=['start'])
    #dp.register_channel_post_handler(forward_channel_messages, content_types=types.ContentTypes.ANY)
    dp.register_channel_post_handler(vk_post_messages, content_types=types.ContentTypes.ANY)
    executor.start_polling(dp, skip_updates=True)

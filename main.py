from aiogram import executor, types
from bot import dp
from handlers import cmd_start, forward_channel_messages, publish_threads_post, publish_vk_post, send_echo

if __name__ == '__main__':
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_channel_post_handler(forward_channel_messages, content_types=types.ContentTypes.ANY)
    dp.register_callback_query_handler(publish_threads_post, lambda c: c.data.startswith('publish_threads'))
    dp.register_callback_query_handler(publish_vk_post, lambda c: c.data.startswith('publish_vk'))
    dp.register_message_handler(send_echo)
    executor.start_polling(dp, skip_updates=True)

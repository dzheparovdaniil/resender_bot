from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

vk_button = InlineKeyboardButton(text="Опубликовать в VK", callback_data=f"publish_vk")
threads_button = InlineKeyboardButton(text="Опубликовать в Threads", callback_data=f"publish_threads")
prepare_threads_button = InlineKeyboardButton(text="Подготовить для Threads", callback_data=f"prepare_threads")
rewrite_message_button = InlineKeyboardButton(text="Пересказать сообщение", callback_data=f"rewrite_message")


post_keyboard = InlineKeyboardMarkup(inline_keyboard=[[vk_button], [prepare_threads_button], [threads_button]])

keyborad_threads = InlineKeyboardMarkup(inline_keyboard=[[rewrite_message_button], [threads_button]])
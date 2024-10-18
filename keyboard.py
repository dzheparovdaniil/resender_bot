from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

vk_button = InlineKeyboardButton(text="Опубликовать в VK", callback_data=f"publish_vk")
threads_button = InlineKeyboardButton(text="Опубликовать в Threads", callback_data=f"publish_threads")
post_keyboard = InlineKeyboardMarkup(inline_keyboard=[[vk_button], [threads_button]])
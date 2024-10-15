from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot

async def forward_channel_messages(message: types.Message):
    message_link = 'https://t.me/c/' + str(message.chat.id) + '/' + str(message.message_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Опубликовать в VK", callback_data=f"publish_vk_post:{message.message_id}"))
    keyboard.add(InlineKeyboardButton("Опубликовать в Threads", callback_data=f"publish_threads_post:{message.message_id}"))
    
    await bot.send_message(chat_id=874188918, text=message.html_text, parse_mode='HTML', reply_markup=keyboard)

async def send_echo(message: types.Message):
    await message.reply(message.html_text, parse_mode='HTML')
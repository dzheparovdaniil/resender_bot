from aiogram import types, F, Router
from bot import bot
from keyboard import post_keyboard, post_keyboard_inst

router_channel = Router()

photos = {}


async def forward_channel_messages(message: types.Message):
    if message.text:
        await bot.send_message(chat_id=874188918, text=message.html_text, parse_mode='HTML', reply_markup=post_keyboard)
    elif message.photo and message.media_group_id == None:
        await bot.send_photo(chat_id=874188918, photo=message.photo[-1].file_id, caption=message.html_text, parse_mode='HTML', reply_markup=post_keyboard_inst)
    elif message.photo and message.media_group_id != None:
        global photos
        key = str(message.media_group_id)
        photos.setdefault(key, [])
        photos[key].append(message.photo[-1].file_unique_id)

@router_channel.message(F.media_group_id == None)
async def send_echo(message: types.Message):
    if message.photo:
        await message.answer_photo(photo=message.photo[-1].file_id, caption = message.caption, parse_mode='HTML', reply_markup=post_keyboard_inst)
    else:
        await message.answer(message.html_text, parse_mode='HTML', reply_markup=post_keyboard)
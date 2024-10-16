from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from bot import bot
from aiogram_album import AlbumMessage

photos = {}
async def forward_channel_messages(message: types.Message):
    message_link = 'https://t.me/c/' + str(message.chat.id) + '/' + str(message.message_id)
    vk_button = InlineKeyboardButton(text="Опубликовать в VK", callback_data=f"publish_vk_post:{message.message_id}")
    threads_button = InlineKeyboardButton(text="Опубликовать в Threads", callback_data=f"publish_threads_post:{message.message_id}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[vk_button], [threads_button]])
    if message.text:
        await bot.send_message(chat_id=874188918, text=f'ссылка на сообщение в канале {message_link}')
        await bot.send_message(chat_id=874188918, text=message.html_text, parse_mode='HTML', reply_markup=keyboard)
    elif message.photo and message.media_group_id == None:
        print(message.media_group_id)
        await bot.send_photo(chat_id=874188918, photo=message.photo[-1].file_id, caption=message.html_text, parse_mode='HTML', reply_markup=keyboard)
    elif message.photo and message.media_group_id != None:
        await bot.send_media_group(chat_id=874188918, media=message.media_group_id)
        print(message.media_group_id)
        #photos = [InputMediaPhoto(media=photo.file_id) for photo in message.photo[-1]]
        #await bot.send_media_group(chat_id=874188918, media=photos)
        #print(message.photo[-1].file_unique_id)
        #global photos
        #key = str(message.chat.id)
        #photos.setdefault(key, [])
        #photos[key].append(message.photo[-1].file_unique_id)
        #print(photos)
        #photos = []
        #for photo_group in message.photo:
        #    # Выбираем самую большую фотографию из группы
        #    best_photo = max(photo_group, key=lambda p: p.file_size)
        #    photos.append(InputMediaPhoto(media=best_photo.file_id))
        #print(photos)
        #await bot.send_message(chat_id=874188918, text=f'ссылка на сообщение в канале {message_link}')
        #await bot.send_media_group(chat_id=874188918, media=message.photo[-1].file_id)
        ##if len(message.photo) == 1:
        ##await bot.send_message(chat_id=874188918, text=f'ссылка на сообщение в канале {message_link}')
        #await bot.send_photo(chat_id=874188918, photo=message.photo[-1].file_id, caption=message.html_text, parse_mode='HTML', reply_markup=keyboard)
        #else:
        #    await bot.send_message(chat_id=874188918, text='я не умею обрабатывать медиа группу')
async def send_echo(message: types.Message):
    await message.reply(message.html_text, parse_mode='HTML')
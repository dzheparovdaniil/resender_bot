import asyncio
from typing import List, Union
from bot import bot, dp
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMedia
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message

class AlbumMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str, Any]
    ) -> Any:
        if not message.media_group_id:
            await handler(message, data)
            return
        try:
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            data['_is_last'] = True
            data["album"] = self.album_data[message.media_group_id]
            await handler(message, data)

        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]
            del data['_is_last']

# Подключаем AlbumMiddleware
dp.message.middleware(AlbumMiddleware())

#async def forward_channel_messages(message: types.Message, album: list[Message]):
#    message_link = 'https://t.me/c/' + str(message.chat.id) + '/' + str(message.message_id)
#    vk_button = InlineKeyboardButton(text="Опубликовать в VK", callback_data=f"publish_vk_post:{message.message_id}")
#    threads_button = InlineKeyboardButton(text="Опубликовать в Threads", callback_data=f"publish_threads_post:{message.message_id}")
#    keyboard = InlineKeyboardMarkup(inline_keyboard=[[vk_button], [threads_button]])
#
#    if message.text:
#        await bot.send_message(chat_id=874188918, text=f'ссылка на сообщение в канале {message_link}')
#        await bot.send_message(chat_id=874188918, text=message.html_text, parse_mode='HTML', reply_markup=keyboard)
#    elif message.photo and not message.media_group_id:
#        await bot.send_photo(chat_id=874188918, photo=message.photo[-1].file_id, caption=message.html_text, parse_mode='HTML', reply_markup=keyboard)
#    else:
#        media_group = []
#        for obj in album:
#            if obj.photo:
#                file_id = obj.photo[-1].file_id
#                media_group.append(InputMediaPhoto(media=file_id))
#            else:
#                obj_dict = obj.dict()
#                file_id = obj_dict[obj.content_type]['file_id']
#                media_group.append(InputMedia(media=file_id))
#            #elif obj.video:
            #    file_id = obj.video.file_id
            #    media_group.append(InputMediaPhoto(media=file_id))
            #elif obj.document:
            #    file_id = obj.document.file_id
            #    media_group.append(InputMediaPhoto(media=file_id))

#        await bot.send_media_group(chat_id=874188918, media=media_group)
#        await bot.send_message(chat_id=874188918, text=f'ссылка на сообщение в канале {message_link}', reply_markup=keyboard)

async def handle_albums(message: Message, album: list[Message]):
    media_group = []
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            media_group.append(InputMediaPhoto(media=file_id))
        else:
            obj_dict = msg.dict()
            file_id = obj_dict[msg.content_type]['file_id']
            media_group.append(InputMedia(media=file_id))

    await message.answer_media_group(media_group)

async def send_echo(message: types.Message):
    await message.reply(message.html_text, parse_mode='HTML')

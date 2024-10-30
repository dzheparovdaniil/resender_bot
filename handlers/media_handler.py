from aiogram import types, F, Router
from bot import bot
from mistralai import Mistral
from aiogram.types import CallbackQuery, Message
from aiogram_media_group import media_group_handler

router_media = Router()


@router_media.message(F.media_group_id)
@media_group_handler()
async def post_media_group(messages: list[Message]) -> None:
    """
    Here I'm handling offline media group
    :param messages:
    :return:
    """
    for message in messages:
        print(f"command, message_id: {message.message_id}, user_id: {message.from_user.id}, text: {message.caption}, media_group_id: {message.media_group_id}")

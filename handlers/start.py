from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    await message.answer(f"Привет, {user_name}! Я буду пересылать сообщения из канала в этот чат. Твой id {user_id}")

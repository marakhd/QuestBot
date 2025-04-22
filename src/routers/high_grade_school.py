from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Welcome! I'm a bot created with aiogram.")

@router.message(Command("help")) 
async def help_handler(message: Message):
    await message.answer("Available commands:\n/start - Start the bot\n/help - Show this help message")

@router.message(F.text)
async def echo_handler(message: Message):
    await message.answer(message.text)


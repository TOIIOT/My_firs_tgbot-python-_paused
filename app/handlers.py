from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import aiohttp
import app.keyboard as kb
import asyncio

router = Router()
api_url_cat = "https://api.thecatapi.com/v1/images/search?mime_types=gif"


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот!", reply_markup=kb.main)
    await message.reply("напиши 'кот' или нажми на кнопку 'Картинка коте 🐱', если хочешь увидеть котика")


@router.message(F.text.casefold().in_(["кот", "картинка коте 🐱"]))
async def send_random_cat(message: Message):
    await message.answer("Подожди немного, я ищу для тебя картинку котика...🐾")

    await asyncio.sleep(1)

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url_cat) as response:
            if response.status == 200:
                data = await response.json()
                ph_url = data[0]["url"]

                await message.answer_photo(
                    photo= ph_url,
                    caption="Вот твой рандомный котик 🐾",
                )
            else:
                await message.answer("Не удалось получить картинку кота.😿")


@router.message(F.text.casefold() == "помощь")
async def cmd_help(message: Message):
    await message.answer("Ты нажал на кнопку помощи, помощи не жди")


@router.message(F.text.casefold() == "о проекте")
async def cmd_about(message: Message):
    await message.answer("ПЕРВЫЙ ТГ БОТЯРА МОЙ")


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer("Вот актуальное меню:", reply_markup=kb.main)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("Ты нажал на кнопку помощи")

@router.message(F.text == "Как дела?")
async def cmd_hello(message: Message):
    await message.answer("Отлично, а у тебя как?")


from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import aiohttp
import app.keyboard as kb
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_gender = State()


router = Router()
api_url_cat = "https://api.thecatapi.com/v1/images/search?mime_types=gif"
api_url_dog = "https://dog.ceo/api/breeds/image/random"
api_url_fox = "https://randomfox.ca/floof/"

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот!", reply_markup=kb.main)
    await message.reply("Если хочешь получить случайную картинку животного, нажми на кнопку 'случайные картинки животных' 🐾")


@router.message(F.text.casefold() == "случайные картинки животных")
async def send_random_cat(message: Message):
    await message.answer("Выберите картинку животного 🐾", reply_markup=kb.catalog)


@router.message(F.text.casefold() == "помощь")
async def cmd_help(message: Message):
    await message.answer("Ты нажал на кнопку помощи, помощи не жди")


@router.message(F.text.casefold() == "о проекте")
async def cmd_about(message: Message):
    await message.answer("ПЕРВЫЙ ТГ БОТЯРА МОЙ")


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer("Вот актуальное меню:", reply_markup=kb.main)


@router.callback_query(F.data == "cat")
async def send_random_cat_callback(callback_query):
    await callback_query.message.answer("Подожди немного, я ищу для тебя картинку котика...🐾")

    await asyncio.sleep(1)

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url_cat) as response:
            if response.status == 200:
                data = await response.json()
                ph_url = data[0]["url"]

                await callback_query.message.answer_photo(
                    photo=ph_url,
                    caption="Вот твой рандомный котик 🐾",
                )
            else:
                await callback_query.message.answer("Не удалось получить картинку кота.😿")


@router.callback_query(F.data == "dog")
async def send_random_dog_callback(callback_query):
    await callback_query.message.answer("Подожди немного, я ищу для тебя картинку собаки...🐾")

    await asyncio.sleep(1)

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url_dog) as response:
            if response.status == 200:
                data = await response.json()
                ph_url = data["message"]

                await callback_query.message.answer_photo(
                    photo=ph_url,
                    caption="Вот твоя рандомная собака 🐶",
                )
            else:
                await callback_query.message.answer("Не удалось получить картинку собаки.")


@router.callback_query(F.data == "fox")
async def send_random_fox_callback(callback_query):
    await callback_query.message.answer("Подожди немного, я ищу для тебя картинку лисы...🦊")

    await asyncio.sleep(1)

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url_fox) as response:
            if response.status == 200:
                data = await response.json()
                ph_url = data["image"]

                await callback_query.message.answer_photo(
                    photo=ph_url,
                    caption="Вот твоя рандомная лиса 🦊",
                )
            else:
                await callback_query.message.answer("Не удалось получить картинку лисы.")


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await message.answer("Давай начнем регистрацию! Как тебя зовут?")
    await state.set_state(Register.waiting_for_name)


@router.message(Register.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Register.waiting_for_age)


@router.message(Register.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Какой у тебя пол? (мужской/женский)", reply_markup=kb.get_gender)
    await state.set_state(Register.waiting_for_gender)


@router.message(Register.waiting_for_gender)
async def process_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    user_data = await state.get_data()
    name = user_data.get("name")
    age = user_data.get("age")
    gender = user_data.get("gender")

    await message.answer(f"Регистрация завершена!\nИмя: {name}\nВозраст: {age}\nПол: {gender}")
    await state.clear()
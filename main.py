from aiogram import Bot, Dispatcher
import asyncio
import sys
from app.handlers import router
from aiogram.client.session.aiohttp import AiohttpSession

session = AiohttpSession(proxy="socks5://127.0.0.1:10808")
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) #тут для инета

async def main():
    bot = Bot(token="8715657901:AAE1GHhm5Q6HvMzLhEyX23yoOWkYrdXf0Mk", session=session)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
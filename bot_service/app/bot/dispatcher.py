from aiogram import Bot, Dispatcher

from app.bot.handlers import router


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(router)
    return dp


def create_bot(token: str) -> Bot:
    return Bot(token=token)
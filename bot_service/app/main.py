import asyncio

from fastapi import FastAPI

from app.bot.dispatcher import create_bot, create_dispatcher
from app.core.config import settings

app = FastAPI(title="Bot Service", version="0.1.0")


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}


async def run_bot() -> None:
    bot = create_bot(settings.TELEGRAM_BOT_TOKEN)
    dp = create_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
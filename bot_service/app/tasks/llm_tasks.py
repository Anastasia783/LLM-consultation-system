import asyncio

from app.infra.celery_app import celery_app
from app.services.openrouter_client import call_openrouter


@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> None:
    from aiogram import Bot
    from app.core.config import settings

    async def _run():
        try:
            answer = await call_openrouter(prompt)
        except RuntimeError as e:
            answer = f"Ошибка при обращении к LLM: {e}"

        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        try:
            await bot.send_message(chat_id=tg_chat_id, text=answer)
        finally:
            await bot.session.close()

    asyncio.run(_run())
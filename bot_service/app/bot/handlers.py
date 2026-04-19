from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()


@router.message(Command("token"))
async def cmd_token(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Использование: /token <jwt>")
        return

    token = args[1].strip()
    try:
        decode_and_validate(token)
    except ValueError as e:
        await message.answer(f"Токен неверный: {e}")
        return

    redis = get_redis()
    await redis.set(f"token:{message.from_user.id}", token)
    await message.answer("Токен принят и сохранён. Можно отправлять запросы.")


@router.message()
async def cmd_message(message: Message) -> None:
    redis = get_redis()
    token = await redis.get(f"token:{message.from_user.id}")

    if not token:
        await message.answer(
            "Токен неверный. Авторизуйтесь через Auth Service "
            "и отправьте токен /token <jwt>"
        )
        return

    try:
        decode_and_validate(token)
    except ValueError as e:
        await message.answer(f"Токен недействителен: {e}. Получите новый токен.")
        return

    llm_request.delay(message.chat.id, message.text)
    await message.answer("Запрос принят, ожидайте ответа...")
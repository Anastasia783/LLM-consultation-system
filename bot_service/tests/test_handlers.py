import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

from jose import jwt
from aiogram.types import Message, User, Chat

from app.core.config import settings


def make_token(sub: str = "123", role: str = "user", expired: bool = False) -> str:
    now = datetime.now(timezone.utc)
    exp = now - timedelta(minutes=1) if expired else now + timedelta(minutes=60)
    payload = {"sub": sub, "role": role, "iat": now, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def make_message(text: str, user_id: int = 123) -> AsyncMock:
    message = AsyncMock(spec=Message)
    message.text = text
    message.from_user = AsyncMock(spec=User)
    message.from_user.id = user_id
    message.chat = AsyncMock(spec=Chat)
    message.chat.id = user_id
    message.answer = AsyncMock()
    return message


@pytest.mark.anyio
async def test_cmd_token_saves_token(fake_redis):
    from app.bot.handlers import cmd_token

    token = make_token()
    message = make_message(f"/token {token}")

    with patch("app.bot.handlers.get_redis", return_value=fake_redis):
        await cmd_token(message)

    saved = await fake_redis.get("token:123")
    assert saved == token
    message.answer.assert_called_once()


@pytest.mark.anyio
async def test_cmd_token_invalid(fake_redis):
    from app.bot.handlers import cmd_token

    message = make_message("/token invalidtoken")

    with patch("app.bot.handlers.get_redis", return_value=fake_redis):
        await cmd_token(message)

    saved = await fake_redis.get("token:123")
    assert saved is None


@pytest.mark.anyio
async def test_cmd_message_no_token(fake_redis):
    from app.bot.handlers import cmd_message

    message = make_message("Привет")

    with patch("app.bot.handlers.get_redis", return_value=fake_redis):
        await cmd_message(message)

    message.answer.assert_called_once()
    call_text = message.answer.call_args[0][0]
    assert "авторизуйтесь" in call_text.lower() or "токен" in call_text.lower()


@pytest.mark.anyio
async def test_cmd_message_with_token_calls_celery(fake_redis, mocker):
    from app.bot.handlers import cmd_message

    token = make_token()
    await fake_redis.set("token:123", token)

    mock_delay = mocker.patch("app.bot.handlers.llm_request.delay")
    message = make_message("Расскажи про Python")

    with patch("app.bot.handlers.get_redis", return_value=fake_redis):
        await cmd_message(message)

    mock_delay.assert_called_once_with(123, "Расскажи про Python")
    message.answer.assert_called_once()
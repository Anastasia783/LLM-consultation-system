import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def make_token(sub: str = "123", role: str = "user", expired: bool = False) -> str:
    now = datetime.now(timezone.utc)
    exp = now - timedelta(minutes=1) if expired else now + timedelta(minutes=60)
    payload = {"sub": sub, "role": role, "iat": now, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def test_decode_valid_token():
    token = make_token(sub="42", role="user")
    payload = decode_and_validate(token)
    assert payload["sub"] == "42"
    assert payload["role"] == "user"


def test_decode_expired_token():
    token = make_token(expired=True)
    with pytest.raises(ValueError, match="expired"):
        decode_and_validate(token)


def test_decode_invalid_token():
    with pytest.raises(ValueError, match="Invalid token"):
        decode_and_validate("this.is.not.a.token")


def test_decode_missing_sub():
    now = datetime.now(timezone.utc)
    payload = {"role": "user", "exp": now + timedelta(minutes=60)}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    with pytest.raises(ValueError, match="sub"):
        decode_and_validate(token)
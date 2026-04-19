import pytest
from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_password_not_equal_plain():
    hashed = hash_password("mysecret")
    assert hashed != "mysecret"


def test_verify_password_correct():
    hashed = hash_password("mysecret")
    assert verify_password("mysecret", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("mysecret")
    assert verify_password("wrongpassword", hashed) is False


def test_create_and_decode_token():
    token = create_access_token(subject="42", role="user")
    payload = decode_token(token)

    assert payload["sub"] == "42"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_invalid_token():
    from jose import JWTError
    with pytest.raises(JWTError):
        decode_token("invalid.token.here")
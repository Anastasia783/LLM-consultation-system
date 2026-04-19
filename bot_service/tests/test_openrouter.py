import pytest
import respx
import httpx

from app.services.openrouter_client import call_openrouter


@pytest.mark.anyio
async def test_call_openrouter_success():
    mock_response = {
        "choices": [
            {"message": {"content": "Привет! Я БОТ."}}
        ]
    }

    with respx.mock:
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=mock_response)
        )
        result = await call_openrouter("Привет")

    assert result == "Привет! Я БОТ."


@pytest.mark.anyio
async def test_call_openrouter_http_error():
    with respx.mock:
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=httpx.Response(500, json={"error": "Server error"})
        )
        with pytest.raises(RuntimeError, match="OpenRouter HTTP error"):
            await call_openrouter("Привет")


@pytest.mark.anyio
async def test_call_openrouter_network_error():
    with respx.mock:
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            side_effect=httpx.ConnectError("Connection failed")
        )
        with pytest.raises(RuntimeError, match="OpenRouter request error"):
            await call_openrouter("Привет")
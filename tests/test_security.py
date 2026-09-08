from unittest.mock import Mock, AsyncMock

import pytest

import jwt
from app.core.security import create_access_token, decode_access_token
from app.db.dependencies import get_current_user

def test_create_and_decode_access_token():
    user_id = 123
    token = create_access_token(user_id)
    result = decode_access_token(token)

    assert result == user_id

def test_decode_invalid_token():
    token = "Invalid token"

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token)

@pytest.mark.asyncio
async def test_current_user_returns_active_user():
    repo = AsyncMock()

    user = Mock()
    user_id = 123
    user.is_active = True

    repo.get_by_id.return_value = user
    token = create_access_token(user_id)
    result = await get_current_user(token, repo)

    assert result is user
    repo.get_by_id.assert_awaited_once_with(123)
import pytest
from unittest.mock import AsyncMock, Mock

from fastapi import HTTPException

from app.models.enum import SubscriptionStatus
from app.models.subscription import SubscriptionPlan
from app.schemas.subscription import SubscriptionResponse
from app.services.subscription_service import SubscriptionService

@pytest.mark.asyncio
async def test_free_user_can_upload_when_under_limit():
    subscription_repo = AsyncMock()
    document_repo = AsyncMock()

    subscription_repo.get_subscription_by_user_id.return_value.plan = (
        SubscriptionPlan.FREE
    )
    document_repo.count_by_user.return_value = 2
    service = SubscriptionService(
        subscription_repo=subscription_repo,
        document_repo=document_repo
    )
    result = await service.can_upload_document(user_id=1)
    assert result is True

@pytest.mark.asyncio
async def test_free_user_cannot_upload_at_limit():
    subscription_repo = AsyncMock()
    document_repo = AsyncMock()

    subscription_repo.get_subscription_by_user_id.return_value.plan = (
        SubscriptionPlan.FREE
    )
    document_repo.count_by_user.return_value = 3

    service = SubscriptionService(
        subscription_repo=subscription_repo,
        document_repo=document_repo
    )
    result = await service.can_upload_document(user_id=1)

    assert result is False


@pytest.mark.asyncio
async def test_pro_user_can_upload_under_limit():
    subscription_repo = AsyncMock()
    document_repo = AsyncMock()

    subscription_repo.get_subscription_by_user_id.return_value.plan = (
        SubscriptionPlan.PRO
    )
    document_repo.count_by_user.return_value = 49

    service = SubscriptionService(
        subscription_repo=subscription_repo,
        document_repo=document_repo
    )
    result = await service.can_upload_document(user_id=1)

    assert result is True

@pytest.mark.asyncio
async def test_pro_user_cannot_upload_at_limit():
    subscription_repo = AsyncMock()
    document_repo = AsyncMock()

    subscription_repo.get_subscription_by_user_id.return_value.plan = (
        SubscriptionPlan.PRO
    )
    document_repo.count_by_user.return_value = 50

    service = SubscriptionService(
        subscription_repo=subscription_repo,
        document_repo=document_repo
    )
    result = await service.can_upload_document(user_id=1)

    assert result is False

@pytest.mark.asyncio
async def test_get_subscription_info_for_pro_user():
    subscription_repo = AsyncMock()
    document_repo = AsyncMock()


    subscription = Mock()
    subscription.plan = SubscriptionPlan.PRO
    subscription.status = SubscriptionStatus.ACTIVE

    subscription_repo.get_subscription_by_user_id.return_value = subscription
    document_repo.count_by_user.return_value = 5

    service = SubscriptionService(
        subscription_repo=subscription_repo,
        document_repo=document_repo
    )
    result = await service.get_subscription_info(user_id=1)

    assert isinstance(result, SubscriptionResponse)
    assert result.plan == SubscriptionPlan.PRO
    assert result.status == SubscriptionStatus.ACTIVE
    assert result.documents_used == 5
    assert result.documents_limit == 50

@pytest.mark.asyncio
async def test_get_subscription_info_fails_when_subscription_not_found():
    subscription_repo = AsyncMock()
    document_repo = AsyncMock()

    subscription_repo.get_subscription_by_user_id.return_value = None

    service = SubscriptionService(
        subscription_repo=subscription_repo,
        document_repo=document_repo
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.get_subscription_info(user_id=1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Subscription not found"

    document_repo.count_by_user.assert_not_awaited()
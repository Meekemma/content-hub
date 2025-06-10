# base/test/test_views.py
import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_user_login(api_client, login_payload, user):
    url = "/base/login/"
    response = api_client.post(url, data=login_payload, format="json")

    logger.info(f"Login Response Data: {response.data}")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
    assert response.data["email"] == login_payload["email"]
    assert response.data["is_verified"] is True

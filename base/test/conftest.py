# base/test/conftest.py
import pytest
from rest_framework.test import APIClient
from base.models import User  # adjust import if your User model is elsewhere


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def login_payload():
    return {
        "email": "ibehemmanuel32@gmail.com",
        "password": "Iloveemmaa1@"
    }


@pytest.fixture
def user(db):
    """
    Creates a test user directly in the DB with verified email.
    """
    password = "Iloveemmaa1@"
    user = User.objects.create_user(
        email="ibehemmanuel32@gmail.com",
        first_name="Emmanuel",
        last_name="Ibeh",
        password=password
    )
    user.is_verified = True
    user.save()
    return user

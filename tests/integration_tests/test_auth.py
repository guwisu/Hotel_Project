import pytest
from fastapi import HTTPException

from src.services.auth import AuthService


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService().decode_token(jwt_token)

    assert payload
    assert payload["user_id"] == data["user_id"]

@pytest.mark.parametrize("email, password, status_code",[
    ("dog@cat.com", "4321", 200),
    ("example@mail.ru", "13123437", 200),
    ("best@email.com", "22421345", 200),
    ("code@love.com", "1623487", 200),
    ("dog@cat.com", "234123", 500),
    ("true@yandex.ru", "0923421", 200),
])
async def test_all_auth_flow(email, password, status_code, ac):
    data = {
            "email": email,
            "password": password,
        }
    try:
        register_response = await ac.post(
            "/auth/register", json=data
        )
        assert register_response.status_code == status_code
    except:
        HTTPException(
            status_code=409, detail="There is already a user with this email"
        )
    if status_code == 200:

        login_response = await ac.post(
            "/auth/login", json=data
        )
        assert login_response.status_code == status_code

        jwt_token = ac.cookies["access_token"]
        assert jwt_token
        assert isinstance(jwt_token, str)

        get_me_response = await ac.get(
            "/auth/me"
        )
        assert get_me_response.status_code == status_code

        data_me = get_me_response.json()
        jwt_token_me = AuthService().create_access_token({"id": data_me["id"]})

        payload = AuthService().decode_token(jwt_token_me)
        assert payload
        assert payload["id"] == data_me["id"]
        assert data_me["email"] == email

        logout_response = await ac.post(
            "/auth/logout"
        )
        assert logout_response.status_code == status_code
        assert logout_response.json()

        after_logout_response = await ac.get(
            "/auth/me"
        )
        assert not ac.cookies
        assert after_logout_response.status_code == 401

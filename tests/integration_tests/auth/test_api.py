import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("dog@cat.com", "4321", 200),
        ("example@test.com", "13123437", 200),
        ("abcde", "22421345", 422),
        ("abcde@abc", "1623487", 422),
        ("dog@cat.com", "234123", 409),
        ("true@yandex.ru", "0923421", 200),
    ],
)
async def test_auth_flow(email: str, password: str, status_code: int, ac):
    data = {
        "email": email,
        "password": password,
    }
    # /register
    register_resp = await ac.post("/auth/register", json=data)
    assert register_resp.status_code == status_code

    if status_code != 200:
        return
    # /login
    login_resp = await ac.post("/auth/login", json=data)
    assert login_resp.status_code == status_code

    assert "access_token" in login_resp.json()

    # /me
    get_me_resp = await ac.get("/auth/me")
    assert get_me_resp.status_code == status_code
    user = get_me_resp.json()

    assert "id" in user
    assert user["email"] == email
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    logout_resp = await ac.post("/auth/logout")
    assert "access_token" not in ac.cookies
    assert logout_resp.status_code == status_code
    assert logout_resp.json()

    # /me
    after_logout_resp = await ac.get("/auth/me")
    assert not ac.cookies
    assert after_logout_resp.status_code == 401

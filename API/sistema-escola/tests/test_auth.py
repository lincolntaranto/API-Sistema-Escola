USERDATA = {
    "name": "Teste",
    "email": "pyteste@email.com",
    "password": "123",
    "role_id": 1,
    "phone": "123",
}


def create_default_user(client, invite):
    return client.post(
        "/auth/users",
        json={
            "name": USERDATA["name"],
            "email": USERDATA["email"],
            "password": USERDATA["password"],
            "phone": USERDATA["phone"],
            "invite": invite,
        },
    )


def test_create_user(client, invite):
    response = create_default_user(client, invite)
    assert response.status_code == 200


def test_create_user_wrong_email(client, invite):
    response = client.post(
        "/auth/users",
        json={
            "name": "Teste",
            "email": "pytesteemail.com",
            "password": "123",
            "phone": "123",
            "invite": invite,
        },
    )
    assert response.status_code == 422


def test_create_user_duplicate_email(client, invite):
    create_default_user(client, invite)
    response = create_default_user(client, invite)
    assert response.status_code == 400


def test_login(client, invite):
    create_default_user(client, invite)
    response = client.post(
        "/auth/sessions",
        json={"email": USERDATA["email"], "password": USERDATA["password"]},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_email_wrong(client, invite):
    response = client.post(
        "/auth/sessions",
        json={"email": "wrongemail@email.com", "password": USERDATA["password"]},
    )
    assert response.status_code == 400


def test_login_password_wrong(client, invite):
    create_default_user(client, invite)
    response = client.post(
        "/auth/sessions", json={"email": USERDATA["email"], "password": "1234"}
    )
    assert response.status_code == 400

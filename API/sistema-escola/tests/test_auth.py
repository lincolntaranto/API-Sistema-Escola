USERDATA = {
    "nome": "Teste",
    "email": "pyteste@email.com",
    "senha": "123",
    "cargo": 1,
    "numero": "123",
}


def criar_usuario_padrao(client, invite):
    return client.post(
        "/auth/usuarios",
        json={
            "nome": USERDATA["nome"],
            "email": USERDATA["email"],
            "senha": USERDATA["senha"],
            "cargo": USERDATA["cargo"],
            "numero": USERDATA["numero"],
            "convite": invite,
        },
    )


def test_create_user(client, invite):
    response = criar_usuario_padrao(client, invite)
    assert response.status_code == 200


def test_create_user_wrong_email(client, invite):
    response = client.post(
        "/auth/usuarios",
        json={
            "nome": "Teste",
            "email": "pytesteemail.com",
            "senha": "123",
            "cargo": 1,
            "numero": "123",
            "convite": invite,
        },
    )
    assert response.status_code == 422


def test_create_user_duplicate_email(client, invite):
    criar_usuario_padrao(client, invite)
    response = criar_usuario_padrao(client, invite)
    assert response.status_code == 400


def test_login(client, invite):
    criar_usuario_padrao(client, invite)
    response = client.post(
        "/auth/sessions", json={"email": USERDATA["email"], "senha": USERDATA["senha"]}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_email_wrong(client, invite):
    response = client.post(
        "/auth/sessions",
        json={"email": "wrongemail@email.com", "senha": USERDATA["senha"]},
    )
    assert response.status_code == 400


def test_login_password_wrong(client, invite):
    criar_usuario_padrao(client, invite)
    response = client.post(
        "/auth/sessions", json={"email": USERDATA["email"], "senha": "1234"}
    )
    assert response.status_code == 400

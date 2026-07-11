def criar_usuario_padrao(client, invite):
    return client.post(
        "/auth/criar_conta",
        json={
            "nome": "Teste",
            "email": "pyteste@email.com",
            "senha": "123",
            "cargo": 1,
            "numero": "123",
            "convite": invite,
        },
    )


def test_create_user(client, invite):
    response = criar_usuario_padrao(client, invite)
    assert response.status_code == 200


def test_create_user_wrong_email(client, invite):
    response = client.post(
        "/auth/criar_conta",
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
        "/auth/login", json={"email": "pyteste@email.com", "senha": "123"}
    )
    assert response.status_code == 200

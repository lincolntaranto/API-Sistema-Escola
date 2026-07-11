def test_create_user(client, invite):
    response = client.post(
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
    assert response.status_code == 200

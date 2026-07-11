def test_consult_student(client, token):
    response = client.get(
        "/management/alunos",
        params={"id_aluno": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert "nome" in response.json()

def test_consult_student(client, token):
    response = client.get(
        "/management/alunos",
        params={"id_aluno": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert "nome" in response.json()


def test_consult_nonexistent_stundet(client, token):
    response = client.get(
        "/management/alunos",
        params={"id_aluno": 200},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

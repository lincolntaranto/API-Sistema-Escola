def create_default_student(client, token):
    return client.post(
        "/management/cadastrar_aluno",
        json={
            "nome": "Yugi",
            "data_nascimento": "2001-01-11",
            "turma": 1,
            "nome_responsavel": "Solomon Muto",
            "celular_responsavel": "123456",
        },
        headers={"Authorization": f"Bearer {token}"},
    )


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


def test_register_student(client, token):
    response = create_default_student(client, token)
    assert response.status_code == 200


def test_register_student_non_existent_class(client, token):
    response = client.post(
        "/management/cadastrar_aluno",
        json={
            "nome": "Yugi",
            "data_nascimento": "2001-01-11",
            "turma": 404,
            "nome_responsavel": "Solomon Muto",
            "celular_responsavel": "123456",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_register_duplicate_student(client, token):
    create_default_student(client, token)
    response = create_default_student(client, token)
    assert response.status_code == 400


def test_delete_student(client, token):
    response = client.delete(
        "/management/apagar_aluno",
        params={"id_aluno": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_delete_non_existent_student(client, token):
    response = client.delete(
        "/management/apagar_aluno",
        params={"id_aluno": 200},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

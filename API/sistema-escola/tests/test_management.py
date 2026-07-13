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


def create_default_classroom(client, token):
    return client.post(
        "management/cadastrar_turma",
        json={"nome": "Girafas", "serie": "1 ano", "ano": 2022, "turno": "noite"},
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


def test_register_student_non_existent_classroom(client, token):
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


def test_delete_student_deleted(client, token):
    client.delete(
        "/management/apagar_aluno",
        params={"id_aluno": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.delete(
        "/management/apagar_aluno",
        params={"id_aluno": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_update_student(client, token):
    response = client.patch(
        "/management/atualizar_aluno",
        params={"id_aluno": 1},
        json={
            "nome": "Cheetara",
            "data_nascimento": "2000-04-04",
            "turma": 1,
            "nome_responsavel": "Taro",
            "celular_responsavel": "1234567",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_update_non_existent_student(client, token):
    response = client.patch(
        "/management/atualizar_aluno",
        params={"id_aluno": 404},
        json={
            "nome": "Cheetara",
            "data_nascimento": "2000-04-04",
            "turma": 1,
            "nome_responsavel": "Taro",
            "celular_responsavel": "1234567",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_consult_classroom(client, token):
    response = client.get(
        "/management/turmas",
        params={"id_turma": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_consult_non_existent_classroom(client, token):
    response = client.get(
        "/management/turmas",
        params={"id_turma": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_register_classroom(client, token):
    response = create_default_classroom(client, token)
    assert response.status_code == 200


def test_register_duplicate_classroom(client, token):
    create_default_classroom(client, token)
    response = create_default_classroom(client, token)
    assert response.status_code == 400


def test_delete_classroom(client, token):
    create_default_classroom(client, token)
    response = client.delete(
        "/management/apagar_turma",
        params={"id_turma": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_delete_non_existent_classroom(client, token):
    create_default_classroom(client, token)
    response = client.delete(
        "/management/apagar_turma",
        params={"id_turma": 404},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_update_classroom(client, token):
    response = client.patch(
        "/management/atualizar_turma",
        params={"id_turma": 1},
        json={"nome": "Elefantes", "serie": "2 ano", "ano": 2023, "turno": "noite"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_update_non_existent_classroom(client, token):
    response = client.patch(
        "/management/atualizar_turma",
        params={"id_turma": 404},
        json={"nome": "Elefantes", "serie": "2 ano", "ano": 2023, "turno": "noite"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

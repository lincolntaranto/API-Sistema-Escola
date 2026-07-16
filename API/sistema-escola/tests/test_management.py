def create_default_student(client, token):
    return client.post(
        "/alunos",
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
        "/turmas",
        json={"nome": "Girafas", "serie": "1 ano", "ano": 2022, "turno": "noite"},
        headers={"Authorization": f"Bearer {token}"},
    )


def create_initial_grade(client, token):
    return client.post(
        "/notas",
        json={
            "id_aluno": 1,
            "materia": "sociologia",
            "nota": 8.5,
            "bimestre": 1,
            "ano": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )


def test_consult_student(client, token):
    response = client.get(
        "/alunos/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert "nome" in response.json()


def test_consult_nonexistent_stundet(client, token):
    response = client.get(
        "/alunos/200",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_register_student(client, token):
    response = create_default_student(client, token)
    assert response.status_code == 200


def test_register_student_non_existent_classroom(client, token):
    response = client.post(
        "/alunos",
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
        "/alunos/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_delete_non_existent_student(client, token):
    response = client.delete(
        "/alunos/200",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_delete_student_deleted(client, token):
    client.delete(
        "/alunos/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.delete(
        "/alunos/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_update_student(client, token):
    response = client.patch(
        "/alunos/1",
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
        "/alunos/404",
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
        "/turmas/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_consult_non_existent_classroom(client, token):
    response = client.get(
        "/turmas/2",
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
        "/turmas/2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_delete_non_existent_classroom(client, token):
    create_default_classroom(client, token)
    response = client.delete(
        "/turmas/404",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_update_classroom(client, token):
    response = client.patch(
        "/turmas/1",
        json={"nome": "Elefantes", "serie": "2 ano", "ano": 2023, "turno": "noite"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_update_non_existent_classroom(client, token):
    response = client.patch(
        "/turmas/404",
        json={"nome": "Elefantes", "serie": "2 ano", "ano": 2023, "turno": "noite"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_consult_position(client, token):
    response = client.get(
        "/cargos/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_consult_non_existent_position(client, token):
    response = client.get(
        "/cargos/404",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_register_position(client, token):
    response = client.post(
        "/cargos",
        json={"nome": "Professor"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_register_duplicate_position(client, token):
    response = client.post(
        "/cargos",
        json={"nome": "Diretor"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_update_position(client, token):
    response = client.patch(
        "/cargos/1",
        json={"nome": "CEO"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_update_non_existent_position(client, token):
    response = client.patch(
        "/cargos/404",
        json={"nome": "CEO"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_consult_grade(client, token):
    create_initial_grade(client, token)
    response = client.get(
        "/alunos/1/notas",
        params={
            "materia": "sociologia",
            "bimestre": 1,
            "ano": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_consult_non_existent_grade(client, token):
    response = client.get(
        "/alunos/1/notas",
        params={
            "materia": "Educação Mágica",
            "bimestre": 1,
            "ano": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_consult_grade_non_existent_student(client, token):
    response = client.get(
        "/alunos/404/notas",
        params={
            "id_aluno": 404,
            "materia": "Educação Mágica",
            "bimestre": 1,
            "ano": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_register_grade(client, token):
    response = create_initial_grade(client, token)
    assert response.status_code == 200


def test_register_duplicate_grade(client, token):
    create_initial_grade(client, token)
    response = create_initial_grade(client, token)
    assert response.status_code == 400


def test_update_grade(client, token):
    create_initial_grade(client, token)
    response = client.patch(
        "/notas/1",
        json={
            "aluno": 1,
            "materia": "filosofia",
            "nota": 10,
            "bimestre": 2,
            "ano": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_update_non_existent_grade(client, token):
    response = client.patch(
        "/notas/404",
        json={
            "aluno": 1,
            "materia": "filosofia",
            "nota": 10,
            "bimestre": 2,
            "ano": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_create_invite(client, token):
    response = client.post(
        "/convites",
        json={"id_cargo": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "convite_token" in response.json()


def test_create_non_existent_position_invite(client, token):
    response = client.post(
        "/convites",
        json={"id_cargo": 404},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

def create_default_student(client, token):
    return client.post(
        "/students",
        json={
            "name": "Yugi",
            "birth_date": "2001-01-11",
            "classroom": 1,
            "guardian_name": "Solomon Muto",
            "guardian_phone": "123456",
        },
        headers={"Authorization": f"Bearer {token}"},
    )


def create_default_classroom(client, token):
    return client.post(
        "/classrooms",
        json={
            "name": "Girafas",
            "school_year": "1 year",
            "year": 2022,
            "shift": "night",
        },
        headers={"Authorization": f"Bearer {token}"},
    )


def create_initial_grade(client, token):
    return client.post(
        "/grades",
        json={
            "student_id": 1,
            "school_subject": "sociologia",
            "grade": 8.5,
            "bimester": 1,
            "year": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )


def test_consult_student(client, token):
    response = client.get(
        "/students/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert "name" in response.json()


def test_consult_nonexistent_stundet(client, token):
    response = client.get(
        "/students/200",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_register_student(client, token):
    response = create_default_student(client, token)
    assert response.status_code == 200


def test_register_student_non_existent_classroom(client, token):
    response = client.post(
        "/students",
        json={
            "name": "Yugi",
            "birth_date": "2001-01-11",
            "classroom": 404,
            "guardian_name": "Solomon Muto",
            "guardian_phone": "123456",
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
        "/students/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_delete_non_existent_student(client, token):
    response = client.delete(
        "/students/200",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_delete_student_deleted(client, token):
    client.delete(
        "/students/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.delete(
        "/students/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_update_student(client, token):
    response = client.patch(
        "/students/1",
        json={
            "name": "Cheetara",
            "birth_date": "2000-04-04",
            "classroom": 1,
            "parents_name": "Taro",
            "guardian_phone": "1234567",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_update_non_existent_student(client, token):
    response = client.patch(
        "/students/404",
        json={
            "name": "Cheetara",
            "birth_date": "2000-04-04",
            "classroom": 1,
            "parents_name": "Taro",
            "guardian_phone": "1234567",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_consult_classroom(client, token):
    response = client.get(
        "/classrooms/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_consult_non_existent_classroom(client, token):
    response = client.get(
        "/classrooms/2",
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
        "/classrooms/2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_delete_non_existent_classroom(client, token):
    create_default_classroom(client, token)
    response = client.delete(
        "/classrooms/404",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_update_classroom(client, token):
    response = client.patch(
        "/classrooms/1",
        json={
            "name": "Elefantes",
            "school_year": "2 year",
            "year": 2023,
            "shift": "night",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_update_non_existent_classroom(client, token):
    response = client.patch(
        "/classrooms/404",
        json={
            "name": "Elefantes",
            "school_year": "2 year",
            "year": 2023,
            "shift": "night",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_consult_position(client, token):
    response = client.get(
        "/roles/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_consult_non_existent_position(client, token):
    response = client.get(
        "/roles/404",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_register_position(client, token):
    response = client.post(
        "/roles",
        json={"name": "Professor"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_register_duplicate_position(client, token):
    response = client.post(
        "/roles",
        json={"name": "Diretor"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_update_position(client, token):
    response = client.patch(
        "/roles/1",
        json={"name": "CEO"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_update_non_existent_position(client, token):
    response = client.patch(
        "/roles/404",
        json={"name": "CEO"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_consult_grade(client, token):
    create_initial_grade(client, token)
    response = client.get(
        "/students/1/grades",
        params={
            "school_subject": "sociologia",
            "bimester": 1,
            "year": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_consult_non_existent_grade(client, token):
    response = client.get(
        "/students/1/grades",
        params={
            "school_subject": "Educação Mágica",
            "bimester": 1,
            "year": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_consult_grade_non_existent_student(client, token):
    response = client.get(
        "/students/404/grades",
        params={
            "school_subject": "Educação Mágica",
            "bimester": 1,
            "year": 2026,
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
        "/grades/1",
        json={
            "student_id": 1,
            "school_subject": "filosofia",
            "grade": 10,
            "bimester": 2,
            "year": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_update_non_existent_grade(client, token):
    response = client.patch(
        "/grades/404",
        json={
            "student_id": 1,
            "school_subject": "filosofia",
            "grade": 10,
            "bimester": 2,
            "year": 2026,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_create_invite(client, token):
    response = client.post(
        "/invites",
        json={"role_id": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "invite_token" in response.json()


def test_create_non_existent_position_invite(client, token):
    response = client.post(
        "/invites",
        json={"role_id": 404},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

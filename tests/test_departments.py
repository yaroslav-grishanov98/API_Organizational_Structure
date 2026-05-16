from fastapi.testclient import TestClient


def test_create_department(client: TestClient):
    """Проверка создания отдела"""
    response = client.post("/departments/", json={"name": "IT"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "IT"
    assert data["parent_id"] is None

def test_create_duplicate_department(client: TestClient):
    """Проверка дублей отдела"""
    client.post("/departments/", json={"name": "IT"})
    response = client.post("/departments/", json={"name": "IT"})
    assert response.status_code == 409

def test_create_child_department(client: TestClient):
    """Проверка создания подотдела"""
    parent = client.post("/departments/", json={"name": "IT"}).json()
    response = client.post("/departments/", json={"name": "Backend", "parent_id": parent["id"]})
    assert response.status_code == 201
    assert response.json()["parent_id"] == parent["id"]

def test_get_department(client: TestClient):
    """Проверка получения отдела"""
    dept = client.post("/departments/", json={"name": "IT"}).json()
    response = client.get(f"/departments/{dept['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "IT"

def test_get_department_not_found(client: TestClient):
    """Проверка несуществующего отдела"""
    response = client.get("/departments/99999")
    assert response.status_code == 404

def test_create_employee(client: TestClient):
    """Проверка создания сотрудника"""
    dept = client.post("/departments/", json={"name": "IT"}).json()
    response = client.post(
        f"/departments/{dept['id']}/employees/",
        json={"full_name": "Иван Иванов", "position": "Разработчик"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Иван Иванов"
    assert data["department_id"] == dept["id"]

def test_create_employee_in_nonexistent_department(client: TestClient):
    """Проверка создания сотрудника в несуществующий отдел"""
    response = client.post(
        "/departments/99999/employees/",
        json={"full_name": "Иван Иванов", "position": "Разработчик"},
    )
    assert response.status_code == 404

def test_update_department(client: TestClient):
    """Проверка обновления отдела"""
    dept = client.post("/departments/", json={"name": "IT"}).json()
    response = client.patch(f"/departments/{dept['id']}", json={"name": "Tech"})
    assert response.status_code == 200
    assert response.json()["name"] == "Tech"

def test_delete_department_cascade(client: TestClient):
    """Проверка удаления"""
    dept = client.post("/departments/", json={"name": "IT"}).json()
    response = client.delete(f"/departments/{dept['id']}?mode=cascade")
    assert response.status_code == 204

def test_delete_department_reassign(client: TestClient):
    """Проверка удаления и перевода сотрудников"""
    dept1 = client.post("/departments/", json={"name": "IT"}).json()
    dept2 = client.post("/departments/", json={"name": "HR"}).json()
    client.post(
        f"/departments/{dept1['id']}/employees/",
        json={"full_name": "Иван Иванов", "position": "Разработчик"},
    )
    response = client.delete(
        f"/departments/{dept1['id']}?mode=reassign&reassign_to_department_id={dept2['id']}"
    )
    assert response.status_code == 204

def test_self_parent(client: TestClient):
    """Проверка защиты"""
    dept = client.post("/departments/", json={"name": "IT"}).json()
    response = client.patch(
        f"/departments/{dept['id']}", json={"parent_id": dept["id"]}
    )
    assert response.status_code == 400

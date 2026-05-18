import pytest


@pytest.mark.parametrize(
    "name, parent_id, status_code",
    [
        ("Отдел 1", None, 200),
        ("Отдел 11", 999, 404),
        ("", None, 422),
        ("Отдел 1.1", 1, 200),
        ("Отдел 1.1", 1, 409),
        ("Отдел 1.1.1", 2, 200),
        ("Отдел 1.1.2", 2, 200),
    ],
)
async def test_create_department(name, parent_id, status_code, ac):
    response = await ac.post(
        "/departments", json={"name": name, "parent_id": parent_id}
    )
    assert response.status_code == status_code
    if status_code != 200:
        return
    result = response.json()
    assert isinstance(result, dict)
    assert result["name"] == name
    assert result["parent_id"] == parent_id


@pytest.mark.parametrize(
    "id, full_name, position, hired_at, status_code",
    [
        (1, "Ф И О", "Позиция", "2026-05-17", 200),
        (4, "Ф1 И1 О1", "Позиция", "2026-05-17", 200),
        (999, "Ф И О", "Позиция", "2026-05-17", 404),
        (4, "Ф2 И2 О2", "Позиция", None, 200),
        (1, "Ф И О", None, "2026-05-17", 422),
    ],
)
async def test_create_employee(id, full_name, position, hired_at, status_code, ac):
    response = await ac.post(
        f"/departments/{id}/employees",
        json={
            "full_name": full_name,
            "position": position,
            "hired_at": hired_at,
        },
    )
    assert response.status_code == status_code
    if status_code != 200:
        return
    result = response.json()
    assert isinstance(result, dict)
    assert result["full_name"] == full_name
    assert result["position"] == position
    assert result["department_id"] == id


@pytest.mark.parametrize(
    "id, depth, include_employees, status_code, len_children",
    [
        (1, 5, True, 200, 2),
        (999, 5, True, 404, 1),
        (1, 1, True, 200, 0),
    ],
)
async def test_get_department(
    id, depth, include_employees, status_code, len_children, ac
):
    response = await ac.get(
        f"/departments/{id}",
        params={
            "depth": depth,
            "include_employees": include_employees,
        },
    )
    assert response.status_code == status_code
    if status_code != 200:
        return
    result = response.json()
    assert isinstance(result, dict)
    assert result["department"]["name"] == "Отдел 1"
    assert len(result["children"][-1]["children"]) == len_children


@pytest.mark.parametrize(
    "id, name, parent_id, status_code",
    [
        (1, "Отдел 1", 1, 400),
        (1, "Отдел 1", 2, 400),
        (3, "Отдел 1.1.1", 1, 200),
        (999, "Отдел 1", 1, 404),
        (1, "Отдел 1", 999, 404),
    ],
)
async def test_update_department(id, name, parent_id, status_code, ac):
    response = await ac.patch(
        f"/departments/{id}", json={"name": name, "parent_id": parent_id}
    )
    assert response.status_code == status_code
    if status_code != 200:
        return
    result = response.json()
    assert isinstance(result, dict)
    assert result["name"] == name
    assert result["parent_id"] == parent_id


@pytest.mark.parametrize(
    "id, mode, reassign_to_department_id, status_code",
    [
        (1, "reassign", 1, 400),
        (999, "reassign", 1, 404),
        (1, "reassign", 999, 404),
        (1, "reassign", None, 422),
        (4, "reassign", 1, 204),
        (1, "cascade", 4, 204),
    ],
)
async def test_delete_department(id, mode, reassign_to_department_id, status_code, ac):
    response = await ac.delete(
        f"/departments/{id}",
        params={
            "mode": mode,
            "reassign_to_department_id": reassign_to_department_id,
        },
    )
    assert response.status_code == status_code

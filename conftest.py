import pytest

from api_client import StellarBurgersApiClient
from data import generate_user, User


@pytest.fixture(scope="session")
def api_client() -> StellarBurgersApiClient:
    """Клиент API Stellar Burgers на всю сессию."""
    return StellarBurgersApiClient()


@pytest.fixture
def new_user() -> User:
    """Новый уникальный пользователь, ещё НЕ зарегистрирован в системе."""
    return generate_user()


@pytest.fixture
def registered_user(api_client: StellarBurgersApiClient, new_user: User):
    """
    Уже зарегистрированный пользователь.

    Фикстура:
    - регистрирует пользователя;
    - возвращает словарь с самим пользователем и токенами.
    """
    response = api_client.register_user(new_user)
    assert response.status_code == 200, "Не удалось зарегистрировать пользователя для теста"

    body = response.json()
    access_token = body.get("accessToken")
    refresh_token = body.get("refreshToken")

    return {
        "user": new_user,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@pytest.fixture(scope="session")
def ingredients(api_client: StellarBurgersApiClient):
    """
    Список id ингредиентов из /api/ingredients.

    Формат ответа в документации не расписан подробно, поэтому берём
    либо поле data, либо ingredients и вытаскиваем _id из каждого элемента.
    """
    response = api_client.get_ingredients()
    assert response.status_code == 200, "Не удалось получить ингредиенты"

    data = response.json()
    items = data.get("data") or data.get("ingredients") or []

    ids = [item["_id"] for item in items if "_id" in item]
    assert ids, "Список ингредиентов пустой — тесты на создание заказа не смогут выполняться"

    return ids

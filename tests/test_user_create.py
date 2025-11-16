import allure
import pytest

from api_client import StellarBurgersApiClient
from data import generate_user
from conftest import User  # type: ignore  # чтобы IDE не ругалась на импорт
# (если IDE ругается — можно просто убрать этот импорт, он не обязателен)


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.title("Создание уникального пользователя")
    @allure.description("Успешная регистрация нового уникального пользователя.")
    def test_create_unique_user_success(self, api_client: StellarBurgersApiClient, new_user: User):
        response = api_client.register_user(new_user)

        assert response.status_code == 200
        body = response.json()

        assert body["success"] is True
        assert body["user"]["email"] == new_user.email
        assert body["user"]["name"] == new_user.name
        assert "accessToken" in body
        assert "refreshToken" in body

    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.description(
        "Повторная регистрация того же пользователя должна вернуть 403 и сообщение "
        "\"User already exists\"."
    )
    def test_create_user_already_exists(self, api_client: StellarBurgersApiClient, registered_user):
        user = registered_user["user"]

        response = api_client.register_user(user)
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @allure.description(
        "Если убрать одно из обязательных полей (email, password или name), "
        "регистрация должна завершиться ошибкой 403."
    )
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(
        self,
        api_client: StellarBurgersApiClient,
        missing_field: str,
    ):
        user = generate_user()
        payload = user.to_dict()
        payload.pop(missing_field)

        response = api_client.register_user(payload)
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"

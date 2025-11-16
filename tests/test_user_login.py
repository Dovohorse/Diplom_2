import allure

from api_client import StellarBurgersApiClient
from data import generate_unique_email


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Логин под существующим пользователем")
    @allure.description("Успешная авторизация уже зарегистрированного пользователя.")
    def test_login_existing_user_success(
        self,
        api_client: StellarBurgersApiClient,
        registered_user,
    ):
        user = registered_user["user"]

        response = api_client.login_user(user.email, user.password)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == user.email

    @allure.title("Логин с неверным логином и паролем")
    @allure.description(
        "При неверном логине или пароле API должно вернуть 401 и сообщение "
        "\"email or password are incorrect\"."
    )
    def test_login_with_invalid_credentials(self, api_client: StellarBurgersApiClient):
        # гарантированно несуществующий пользователь
        email = generate_unique_email()
        password = "wrong_password"

        response = api_client.login_user(email, password)
        body = response.json()

        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"

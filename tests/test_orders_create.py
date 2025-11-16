import allure

from api_client import StellarBurgersApiClient


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.description("Успешное создание заказа авторизованным пользователем с валидными ингредиентами.")
    def test_create_order_authorized_with_ingredients(
        self,
        api_client: StellarBurgersApiClient,
        ingredients,
        registered_user,
    ):
        access_token = registered_user["access_token"]
        # берём первые два ингредиента из списка
        ingredients_ids = ingredients[:2]

        response = api_client.create_order(ingredients_ids, access_token=access_token)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без авторизации")
    @allure.description(
        "Создание заказа без авторизации тоже должно быть успешным: "
        "сервер возвращает 200 и success=true."
    )
    def test_create_order_without_authorization(
        self,
        api_client: StellarBurgersApiClient,
        ingredients,
    ):
        ingredients_ids = ingredients[:2]

        response = api_client.create_order(ingredients_ids, access_token=None)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]


    @allure.title("Создание заказа без ингредиентов (с авторизацией)")
    @allure.description(
        "Если не передать ни одного ингредиента, должен прийти код 400 и "
        "сообщение \"Ingredient ids must be provided\"."
    )
    def test_create_order_authorized_without_ingredients(
        self,
        api_client: StellarBurgersApiClient,
        registered_user,
    ):
        access_token = registered_user["access_token"]

        response = api_client.create_order([], access_token=access_token)
        body = response.json()

        assert response.status_code == 400
        assert body["success"] is False
        assert body["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.description(
        "При передаче невалидного id ингредиента должен вернуться код ответа 500 Internal Server Error."
    )
    def test_create_order_with_invalid_ingredient_hash(
        self,
        api_client: StellarBurgersApiClient,
        registered_user,
    ):
        access_token = registered_user["access_token"]
        invalid_ingredients = ["invalid_ingredient_id"]

        response = api_client.create_order(invalid_ingredients, access_token=access_token)

        assert response.status_code == 500

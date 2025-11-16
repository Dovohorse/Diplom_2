from typing import Union, Dict, Any, List

import requests

import endpoints
from data import User


class StellarBurgersApiClient:
    def __init__(self) -> None:
        # Session даёт переиспользование соединений и общих настроек
        self.session = requests.Session()

    # ---------- Пользователи ----------

    def register_user(self, user: Union[User, Dict[str, Any]]):
        """Регистрация пользователя (создание)."""
        if isinstance(user, User):
            payload = user.to_dict()
        else:
            payload = user
        return self.session.post(endpoints.REGISTER_USER, json=payload)

    def login_user(self, email: str, password: str):
        """Логин пользователя."""
        payload = {"email": email, "password": password}
        return self.session.post(endpoints.LOGIN_USER, json=payload)

    # ---------- Ингредиенты ----------

    def get_ingredients(self):
        """Получение списка ингредиентов."""
        return self.session.get(endpoints.INGREDIENTS)

    # ---------- Заказы ----------

    def create_order(self, ingredients_ids: List[str], access_token: str | None = None):
        """Создание заказа. Если токен не указан — запрос без авторизации."""
        headers: Dict[str, str] = {}
        if access_token:
            headers["Authorization"] = access_token

        payload = {"ingredients": ingredients_ids}
        return self.session.post(endpoints.ORDERS, json=payload, headers=headers)

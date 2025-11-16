from dataclasses import dataclass, asdict
from uuid import uuid4


@dataclass
class User:
    email: str
    password: str
    name: str

    def to_dict(self) -> dict:
        return asdict(self)


def generate_unique_email() -> str:
    """Генерирует уникальный email, чтобы регистрация всегда проходила успешно."""
    unique_part = uuid4().hex
    return f"qa_{unique_part}@example.com"


def generate_user(
    password: str = "password123",
    name: str = "Test User",
) -> User:
    """Создаёт нового уникального пользователя."""
    return User(
        email=generate_unique_email(),
        password=password,
        name=name,
    )

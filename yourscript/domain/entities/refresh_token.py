from dataclasses import dataclass

from domain.value_objects.user_id import UserId


@dataclass
class RefreshToken:
    token: str
    user_id: UserId

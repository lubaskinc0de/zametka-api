from abc import abstractmethod

from typing import Protocol

from domain.entities.user import User

from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects import Token


class TokenSender(Protocol):
    """Token sender interface"""

    @abstractmethod
    def create(
        self, secret_key: str, algorithm: str, user: User, jwt: "JWTOperations"
    ) -> Token:
        """Create verification token"""


class MailTokenSender(TokenSender):
    """Token sender via email interface"""

    @abstractmethod
    def send(self, token: str, subject: str, to_email: str):
        """Send token to the user via email"""


class JWTOperations(Protocol):
    """JWT Operations interface"""

    @abstractmethod
    def encode(self, payload: dict, secret_key: str, algorithm: str) -> str:
        """Encode JWT"""

    @abstractmethod
    def decode(self, token: str, secret_key: str, algorithm: str) -> dict:
        """Decode JWT"""


class JWT(Protocol):
    """JWT Tokens management"""

    @abstractmethod
    def create_access_token(self, subject: str) -> str:
        """Create access JWT"""

    @abstractmethod
    def create_refresh_token(self, subject: str) -> str:
        """Create refresh JWT"""

    @abstractmethod
    def set_access_cookies(self, token: str) -> None:
        """Set access cookies"""

    @abstractmethod
    def set_refresh_cookies(self, token: str) -> None:
        """Set refresh cookies"""

    @abstractmethod
    def get_jwt_subject(self) -> str | int | None:
        pass


class PasswordHasher(Protocol):
    """CryptContext interface"""

    @abstractmethod
    def hash(self, plain: str) -> HashedPassword:
        """Hash the plain password"""

    @abstractmethod
    def verify(self, plain: str, hashed: HashedPassword) -> bool:
        """Compare that plain hash is equal hashed"""


class AuthSettings(Protocol):
    """Auth settings interface"""

    secret_key: str
    algorithm: str

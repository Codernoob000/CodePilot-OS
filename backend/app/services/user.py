from uuid import UUID

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class EmailAlreadyExistsError(Exception):
    """Raised when the email is already registered."""


class UsernameAlreadyExistsError(Exception):
    """Raised when the username is already taken."""


class InvalidCredentialsError(Exception):
    """Raised when email or password is invalid."""


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(
        self,
        user_data: UserCreate,
    ) -> User:
        if await self.repository.get_by_email(user_data.email):
            raise EmailAlreadyExistsError("Email already exists")

        if await self.repository.get_by_username(user_data.username):
            raise UsernameAlreadyExistsError("Username already exists")

        hashed_password = hash_password(user_data.password)

        return await self.repository.create(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User:
        """Authenticate a user using email and password."""

        user = await self.repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError("Invalid email or password.")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password.")

        return user

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User:
        """Retrieve a user by ID."""

        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError(
                "Invalid authentication credentials."
            )

        return user
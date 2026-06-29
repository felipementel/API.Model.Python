"""Domain exceptions for the Usuarios bounded context."""


class UserAlreadyExistsError(Exception):
    """Raised when attempting to create a user with a duplicate ID."""

    def __init__(self, user_id: int) -> None:
        """Initialise with the duplicate user ID."""
        super().__init__(f"Usuario com id {user_id} ja existe.")


class UserNotFoundError(Exception):
    """Raised when a requested user does not exist."""

    def __init__(self, user_id: int) -> None:
        """Initialise with the missing user ID."""
        super().__init__(f"Usuario com id {user_id} nao foi encontrado.")

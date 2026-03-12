class UserAlreadyExistsError(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"Usuario com id {user_id} ja existe.")


class UserNotFoundError(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"Usuario com id {user_id} nao foi encontrado.")

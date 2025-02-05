from typing import List, Optional
from app.schemas import UserCreate, UserResponse

class UserRepository:
    def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        raise NotImplementedError

    def create_user(self, user: UserCreate) -> UserResponse:
        raise NotImplementedError

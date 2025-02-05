from typing import Dict, Optional
from app.schemas import UserCreate, UserResponse

# 🌟 讓 `users` 資料儲存在全域變數，避免每次請求都重設 🌟
_mock_users_db: Dict[str, UserResponse] = {}

class MockUserRepository:
    def __init__(self):
        self.users = _mock_users_db  # 共享全域變數

    def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        """根據 username 取得使用者資料"""
        return self.users.get(username)

    def create_user(self, user: UserCreate) -> UserResponse:
        """新增使用者"""
        if user.username in self.users:
            raise ValueError("User already exists")
        
        user_id = len(self.users) + 1
        user_response = UserResponse(id=user_id, username=user.username, email=user.email)
        self.users[user.username] = user_response
        return user_response

    def clear(self):
        """🌟 測試時可清除所有使用者 🌟"""
        self.users.clear()

import os
from app.repositories import UserRepository
from app.repositories import MockUserRepository
from app.schemas import UserCreate, UserResponse
from typing import List, Optional
from fastapi import Depends
from dotenv import load_dotenv

# 從 .env 檔案讀取環境變數
load_dotenv()

# 初始化 Mock Repository
mock_repo = MockUserRepository()

# 依賴注入
def get_user_repository() -> UserRepository:
    """依據環境變數動態決定使用 Mock 還是真實 DB"""
    use_mock = os.getenv("USE_MOCK_DB", "True").lower() == "true"
    return MockUserRepository() if use_mock else UserRepository()
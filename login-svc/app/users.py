from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserResponse
from app.repository import UserRepository
from app.dependencies import get_user_repository

router = APIRouter()


@router.post("/", response_model=UserResponse)
def register(user: UserCreate, repo: UserRepository = Depends(get_user_repository)):
    """
    用戶註冊處理函數。
    
    該函數會檢查用戶名是否已經存在於資料庫中，如果存在，則返回錯誤提示；如果不存在，
    則會創建新用戶並返回用戶資料。

    :param user: 用戶註冊資料，包括用戶名、電子郵件和密碼
    :param repo: 用來進行資料庫操作的 UserRepository 實例
    :return: 新創建的用戶資料（回應模型 UserResponse）
    :raises HTTPException: 當用戶名已經存在時，會引發 400 錯誤
    """
    if repo.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = repo.create_user(user)
    return new_user

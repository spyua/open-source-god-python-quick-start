from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.schemas import Token, LoginRequest
from app.repository import UserRepository
from app.dependencies import get_user_repository
import os

# 建立 FastAPI 的 APIRouter，這樣可以將路由模組化管理
router = APIRouter()

# 讀取環境變數中的 SECRET_KEY，如果沒有則使用預設值
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
# 設定 JWT 的加密演算法
ALGORITHM = "HS256"
# 設定存取令牌（Access Token）過期時間（分鐘）
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 設定密碼雜湊（Hashing）方式，這裡使用 bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    """
    使用 bcrypt 產生密碼的雜湊值。
    :param password: 明文密碼
    :return: 雜湊後的密碼
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    驗證使用者輸入的密碼是否與資料庫中儲存的雜湊密碼相符。
    :param plain_password: 使用者輸入的明文密碼
    :param hashed_password: 資料庫中儲存的雜湊密碼
    :return: 布林值，表示密碼是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    創建 JWT 存取令牌（Access Token）。
    :param data: 包含 JWT 負載的字典，例如 {"sub": "username"}
    :param expires_delta: 過期時間的 timedelta 物件，預設為 30 分鐘
    :return: 加密後的 JWT Token
    """
    to_encode = data.copy()  # 複製資料，避免修改原始字典
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # 新增過期時間到負載
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # 使用 SECRET_KEY 及演算法簽署 JWT


@router.post("/login", response_model=Token)
def login(request: LoginRequest, repo: UserRepository = Depends(get_user_repository)):
    """
    用戶登入端點，驗證使用者憑證並返回 JWT Token。
    :param request: 登入請求的請求體（包含 username 和 password）
    :param repo: 依賴注入的 UserRepository，用於查詢使用者資訊
    :return: 包含 JWT Token 的字典 {"access_token": "...", "token_type": "bearer"}
    """
    # 查詢使用者是否存在於資料庫
    user = repo.get_user_by_username(request.username)
    if not user:
        # 若使用者不存在，拋出 HTTP 400 錯誤（Bad Request）
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # 生成 JWT Token，將 username 存入 "sub"（Subject）欄位
    access_token = create_access_token({"sub": user.username})
    
    # 返回存取令牌與 token 類型
    return {"access_token": access_token, "token_type": "bearer"}

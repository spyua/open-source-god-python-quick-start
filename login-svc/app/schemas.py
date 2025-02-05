# 從 pydantic 引入 BaseModel 和 EmailStr
from pydantic import BaseModel, EmailStr

# 基礎用戶資料模型，所有用戶資料類別都會繼承此類別
class UserBase(BaseModel):
    username: str  # 用戶名
    email: EmailStr  # 用戶 email，驗證 email 格式

# 用戶創建模型，新增密碼欄位
class UserCreate(UserBase):
    password: str  # 密碼欄位

# 用戶回應模型，包含用戶 ID
class UserResponse(UserBase):
    id: int  # 用戶 ID

    class Config:
        orm_mode = True  # 允許從 ORM 物件自動轉換

# 登錄請求模型，包含用戶名和密碼
class LoginRequest(BaseModel):
    username: str  # 用戶名
    password: str  # 密碼

# Token 模型，包含訪問令牌和令牌類型
class Token(BaseModel):
    access_token: str  # 訪問令牌
    token_type: str  # 令牌類型

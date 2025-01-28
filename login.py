from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import datetime, timedelta

# 假設密鑰和算法
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Router 設置
login_router = APIRouter()

# 模擬用戶數據庫
fake_users_db = {
    "testuser": {"username": "testuser", "password": "testpassword"}
}

# 定義 Pydantic 模型
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    username: str
    password: str

# Token 生成函數
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 登入端點（公開）
@login_router.post("/login", response_model=Token)
async def login(data: LoginData):
    user = fake_users_db.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Token 驗證函數
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def decode_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

# 受保護的路由
@login_router.get("/tokenTest")
async def protected_route(username: str = Depends(decode_access_token)):
    return {"message": f"Token Authorized!!"}
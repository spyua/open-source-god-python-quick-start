from fastapi import FastAPI
from app.api import auth_router, users_router
from app.database import engine, Base

# 建立資料庫表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Auth Service")

# 註冊路由
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Auth Service"}

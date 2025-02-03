from fastapi import FastAPI
from login import login_router  # 匯入 login.py 的路由
from fastapi.openapi.utils import get_openapi

# 自定義 OpenAPI Schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom API with Bearer Token Authentication",
        version="1.0.0",
        description="This is a sample API using Bearer token authentication.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"Bearer": []}]  # 全局預設需要 Bearer Token
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# 初始化 FastAPI 應用
app = FastAPI(
    title="Login API with Bearer Token",
    description="使用 Bearer Token 進行驗證",
    version="1.0.0",
    swagger_ui_oauth2_redirect_url=None,  # 禁用默認 OAuth2
)

# 替換默認 OpenAPI
app.openapi = custom_openapi

# 包含 login.py 中的路由，且不添加驗證需求
app.include_router(
    login_router,  # 匯入的路由
    prefix="",     # 路由前綴
    tags=None      # 不標記為特定分類
)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Application"}
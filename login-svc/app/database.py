# 載入 SQLAlchemy 和其他所需的模組
from sqlalchemy import create_engine  # 用來創建資料庫引擎（engine）
from sqlalchemy.ext.declarative import declarative_base  # 用來創建資料表的基類（Base）
from sqlalchemy.orm import sessionmaker  # 用來創建會話（Session）
import os  # 用來處理作業系統相關的功能（如環境變數）
from dotenv import load_dotenv  # 用來載入 .env 環境變數

# 載入 .env 檔案中的環境變數，方便設定資料庫連線等資訊
load_dotenv()

# 從 .env 檔案中取得資料庫的 URL，若未設定則使用預設的 SQLite 資料庫
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# 創建資料庫引擎，根據不同的資料庫類型來設定引擎
# 如果是 SQLite 則會加上 connect_args 參數來禁用同一線程的檢查
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# 創建 SessionLocal，用來生成資料庫會話
# `autocommit=False`：表示不會自動提交交易，需要手動提交
# `autoflush=False`：表示不會自動將變更刷新到資料庫
# `bind=engine`：將會話綁定到我們之前創建的資料庫引擎上
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 創建基類（Base），所有的模型類別將繼承這個基類
Base = declarative_base()

# 定義依賴注入函數 `get_db`，用來管理資料庫會話
def get_db():
    # 創建資料庫會話
    db = SessionLocal()
    try:
        # 使用 yield 回傳資料庫會話，這樣才能實現依賴注入
        yield db
    finally:
        # 在使用完後關閉資料庫會話
        db.close()

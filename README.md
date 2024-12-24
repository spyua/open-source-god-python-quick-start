# Python Side Project

## 主要功能
1. 註冊登入系統
   - OAuth2
   - 加密  
   - IP / 裝置登入記錄
2. AI文字多輪對答
   - 上下文記憶
   - 模型參數調整（temperature）
3. 對話紀錄儲存/檢閱/刪除
   - 清理機制
4. （進階）上傳文件供LLM檢索
   - 向量嵌入
   - 向量資料儲存
   - 檔案儲存
5. （進階）對話紀錄下載
   - 格式與壓縮

## 資源需求：
1. 程式語言版本：Python 3.11（待定）
2. 生成語言框架：Langchain
3. LLM模型：
   - Local: Ollama/LLama 3.2 1B（資源使用最少）
4. 嵌入模型：（待定，繁中模型？）
5. 資料庫
   - 使用者資訊
   - 對話紀錄
   - 檢索用資料（VectorDB）
6. 前端頁面：待定
7. 後端框架：FastAPI
8. 資源管理：Docker-compose
9.  版本控制：GitHub
10. CICD：GitHub Action
11. 單元測試：unittest / pytest（待定）
12. 負載擴展：Nginx
13. 日誌記錄：Open telemetry, Prometheus , Grafana

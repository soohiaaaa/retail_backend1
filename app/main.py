import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ⚠️ 關鍵：必須清清楚楚地從你寫好的 api 文件夾中導入這兩個路由模組
from app.api import analytics, chatbot
from app.db.session import get_db_connection

# 初始化 FastAPI 實例
app = FastAPI(title="零售智能運營與數倉分析平台", version="1.0.0")

# 暴力允許跨域，確保前端 5173/5174 端口可以順利通車
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模擬數倉數據初始化（啟動時如果發現 DuckDB 沒表，會自動建立並塞入測試數據）
# 将 app/main.py 中的初始化逻辑替换为以下代码：

@app.on_event("startup")
def verify_warehouse_data():
    """
    服务器启动时，只对已存在的 Kaggle 数仓进行数据量校正和保护，
    不再强行插入旧的 4 列模拟假数据。
    """
    from app.db.session import get_db_connection
    
    with get_db_connection() as conn:
        try:
            # 统计当前真实数据量
            row_count = conn.execute("SELECT COUNT(*) FROM retail_sales;").fetchone()[0]
            print(f"==================================================")
            print(f"📊 数仓引擎启动成功！当前 Kaggle 数据表活跃行数: {row_count} 行")
            print(f"==================================================")
        except Exception as e:
            print(f"⚠️ 启动警告：未检测到 retail_sales 表，请确保已正确导入 Kaggle CSV！")


# ⚠️ 核心中的核心：必須在這裡把數據分析和聊天的路牌掛載到 FastAPI 的總地圖中
app.include_router(analytics.router)
app.include_router(chatbot.router)

# 根路徑返回信息（直接覆蓋掉你原本寫的舊提示）
@app.get("/")
def health_check():
    return {"status": "operational", "service": "Retail Data Warehouse Engine"}

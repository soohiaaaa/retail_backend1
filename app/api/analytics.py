from fastapi import APIRouter, HTTPException, status
from app.db.session import get_db_connection
import logging

router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = logging.getLogger("uvicorn.error")

@router.get("/top-products-share")
async def get_top_products_sales_share():
    """
    针对 Kaggle 零售数据集定制的销量分析路由。
    使用 CTE + 窗口函数，计算各品类销量前五的产品及其全店销量占比。
    """
#productsales #把每樣商品按照名字和分類加總，算出每樣東西總共賣了幾件。
#SalesMetrics#算出全店所有人一共賣了幾件（總大餅）。再給每一類排名次
#SELECT#選出各類前五名，算百分比
    complex_sql = """
   
    WITH ProductSales AS (
        SELECT 
            product_name,
            category,
            COUNT(transaction_id) as total_sales
        FROM retail_sales
        GROUP BY product_name, category
    ),
    SalesMetrics AS (
        SELECT 
            product_name,
            category,
            total_sales,
            SUM(total_sales) OVER() as grand_total,
            ROW_NUMBER() OVER(PARTITION BY category ORDER BY total_sales DESC) as rank_in_category
        FROM ProductSales
    )
    SELECT 
        product_name,
        category,
        total_sales,
        ROUND((CAST(total_sales AS DOUBLE) / grand_total) * 100, 2) as sales_percentage_share,
        rank_in_category
    FROM SalesMetrics
    WHERE rank_in_category <= 5
    ORDER BY category, rank_in_category;
    """

    try:
        with get_db_connection() as conn:
            df = conn.execute(complex_sql).fetchdf()
            result = df.to_dict(orient="records")
            return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"数仓 SQL 执行失败，请检查 CSV 列名是否对齐。错误详情: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数仓服务错误: {str(e)}"
        )

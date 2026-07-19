"""
数据服务模块 - 从 CSV 读取和处理数据
"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")

# 全局缓存
_ecommerce_df = None


def _load_ecommerce_df():
    global _ecommerce_df
    if _ecommerce_df is None:
        excel_path = os.path.join(DATA_DIR, "E Commerce Dataset.xlsx")
        _ecommerce_df = pd.read_excel(excel_path, sheet_name="E Comm")
    return _ecommerce_df


def get_overall_metrics():
    """计算总体指标"""
    df = _load_ecommerce_df()
    total_users = int(df["CustomerID"].nunique())
    churned = int(df[df["Churn"] == 1]["CustomerID"].nunique())
    churn_rate = df["Churn"].mean()
    avg_orders = df["OrderCount"].mean()
    median_orders = df["OrderCount"].median()
    avg_coupon = df["CouponUsed"].mean()
    avg_cashback = df["CashbackAmount"].mean()
    avg_app_time = df["HourSpendOnApp"].mean()
    avg_satisfaction = df["SatisfactionScore"].mean()
    avg_days_since = df["DaySinceLastOrder"].mean()

    return {
        "用户数": total_users,
        "流失人数": churned,
        "总体流失率": f"{churn_rate * 100:.1f}%",
        "平均订单数": f"{avg_orders:.2f}",
        "订单数中位数": f"{median_orders:.1f}",
        "平均优惠券使用": f"{avg_coupon:.2f}",
        "平均返现": f"¥{avg_cashback:.2f}",
        "平均App使用时长": f"{avg_app_time:.2f}小时",
        "平均满意度": f"{avg_satisfaction:.2f}",
        "平均距上次下单天数": f"{avg_days_since:.1f}",
    }


def get_segment_analysis():
    """生命周期阶段分析"""
    df = _load_ecommerce_df()

    def tenure_group(t):
        if pd.isna(t):
            return "未知"
        t = int(t)
        if t <= 6:
            return "0-6个月"
        elif t <= 12:
            return "7-12个月"
        elif t <= 24:
            return "13-24个月"
        else:
            return "24个月以上"

    df["TenureGroup"] = df["Tenure"].apply(tenure_group)

    result = df.groupby("TenureGroup", sort=False).agg(
        用户数=("CustomerID", "nunique"),
        流失率=("Churn", "mean"),
        流失人数=("Churn", "sum"),
        平均订单数=("OrderCount", "mean"),
        平均返现=("CashbackAmount", "mean"),
        平均优惠券=("CouponUsed", "mean"),
    ).reset_index()

    result["流失人数"] = result["流失人数"].astype(int)
    return result


def get_cross_analysis():
    """交叉分析：生命周期阶段 × 支付方式"""
    df = _load_ecommerce_df()

    def tenure_group(t):
        if pd.isna(t):
            return "未知"
        t = int(t)
        if t <= 6:
            return "0-6个月"
        elif t <= 12:
            return "7-12个月"
        elif t <= 24:
            return "13-24个月"
        else:
            return "24个月以上"

    df["TenureGroup"] = df["Tenure"].apply(tenure_group)

    result = df.groupby(["TenureGroup", "PreferredPaymentMode"], sort=False).agg(
        用户数=("CustomerID", "nunique"),
        流失人数=("Churn", "sum"),
        流失率=("Churn", "mean"),
        平均订单数=("OrderCount", "mean"),
    ).reset_index()

    result["流失人数"] = result["流失人数"].astype(int)
    return result


def get_category_data():
    """品类用户统计"""
    df = _load_ecommerce_df()
    return df["PreferedOrderCat"].value_counts().to_dict()


def get_filtered_data(category):
    """按品类筛选数据"""
    df = _load_ecommerce_df()
    if category == "all":
        return df
    return df[df["PreferedOrderCat"] == category].copy()


def get_download_data(category):
    """获取可下载的数据（用于拓展A）"""
    return get_filtered_data(category)

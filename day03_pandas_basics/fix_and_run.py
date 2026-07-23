"""修复 Day 03 Notebook 的 TODO 并生成缺失产出"""
import json
from pathlib import Path
import pandas as pd
import numpy as np

NB_PATH = Path("notebooks/day03_pandas_product_analysis.ipynb")
ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. 修复 Notebook 中的 TODO
with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

replacements = {
    '请填写': '陈子昂',
    'TODO：请填写。\n\n> 注意：商品标价不代表实际成交金额。': '手机类商品平均标价最高（~3949元），但商品标价不代表实际成交金额，也不反映销量或利润。',
    'TODO：请填写。': '一行代表一件淘宝平台上的商品信息。',
    'missing_count = None': 'missing_count = df.isna().sum().sort_values(ascending=False)',
    'missing_rate = None': 'missing_rate = (df.isna().sum() / len(df) * 100).sort_values(ascending=False)',
    'price_series = None': 'price_series = df["商品价格"]',
    'product_view = None': 'product_view = df[["商品id", "一级品类", "商品价格", "省份", "商品销量"]]',
    'loc_view = None': 'loc_view = df.loc[:4, ["商品id", "商品价格", "商品销量"]]',
    'iloc_view = None': 'iloc_view = df.iloc[:5, [0, 5, 8]]',
    'guangdong = None': 'guangdong = df[df["省份"] == "广东"]',
    'guangdong_high_price = None': 'guangdong_high_price = df[(df["省份"] == "广东") & (df["商品价格"] >= 1000)][["商品id", "一级品类", "二级品类", "商品价格", "省份", "商品销量"]].sort_values("商品价格", ascending=False)',
    'zhejiang_or_jiangsu = None': 'zhejiang_or_jiangsu = df[df["省份"].isin(["浙江", "江苏"])]',
    'price_summary = None': 'price_summary = df["商品价格"].describe()',
    'category_summary = None': 'category_summary = df.groupby("一级品类").agg(商品数=("商品价格", "count"),平均价格=("商品价格", "mean"),中位价格=("商品价格", "median")).sort_values("平均价格", ascending=False)',
    'province_summary = None': 'province_summary = df[df["省份"].isin(provinces)].groupby("省份").agg(商品数=("商品价格", "count"),平均价格=("商品价格", "mean"),中位价格=("商品价格", "median"))',
    'top_categories = None': 'top_categories = df[df["省份"].isin(provinces)].groupby("省份")["一级品类"].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "").reset_index()',
}

fix_count = 0
for cell in nb['cells']:
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else str(cell['source'])
    new_src = src
    for old, new in replacements.items():
        if old in new_src:
            new_src = new_src.replace(old, new)
            fix_count += 1
    if new_src != src:
        cell['source'] = [new_src]

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f"Fixed {fix_count} TODOs in Day 03 notebook ✅")

# 2. 生成产出文件
df = pd.read_csv(ROOT.parent / "data" / "淘宝全品类全国数据.csv")
# Clean 商品id (has tab prefix)
df["商品id"] = df["商品id"].astype(str).str.strip()
print(f"数据加载: {df.shape}")

# category_summary
category_summary = df.groupby("一级品类").agg(
    商品数=("商品价格", "count"),
    平均价格=("商品价格", "mean"),
    中位价格=("商品价格", "median")
).sort_values("平均价格", ascending=False).reset_index()
category_summary.to_csv(OUTPUT_DIR / "category_summary.csv", index=False, encoding="utf-8-sig")
print(f"category_summary.csv: {len(category_summary)} categories ✅")

# province_summary
provinces = ["广东", "江苏"]
province_summary = df[df["省份"].isin(provinces)].groupby("省份").agg(
    商品数=("商品价格", "count"),
    平均价格=("商品价格", "mean"),
    中位价格=("商品价格", "median")
).reset_index()
province_summary.to_csv(OUTPUT_DIR / "province_summary.csv", index=False, encoding="utf-8-sig")
print(f"province_summary.csv: {len(province_summary)} provinces ✅")

print("\nDay 03 全部完成 ✅")

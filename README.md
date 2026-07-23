# 🛒 电商用户行为数据分析系统 · 全栈实训项目

> **从数据清洗到机器学习，从 Web 应用到模型部署 — 十天完整实训旅程**  
> 基于 Python + Pandas + Flask + Scikit-learn 的企业级数据分析全流程项目

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-red.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)
![pytest](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Machine Learning](https://img.shields.io/badge/ML-Logistic--DT--RF-ff69b4.svg)

**👤 作者**: 陈子昂 ｜ **🆔 学号**: 24012474  
**📅 实训周期**: Day 03 – Day 10 ｜ **🎯 主题**: 电商用户行为分析与流失预测

</div>

---

## 📋 项目全景

本项目以 **淘宝电商用户数据集**（5,630 名用户，22 个特征）为核心，通过 **10 天系统化实训**，完成了从原始数据清洗到机器学习模型部署的全链路数据科学项目。

| 阶段 | 天数 | 核心主题 | 技术栈 |
|:----:|:----:|---------|--------|
| 📊 基础分析 | Day 03–04 | NumPy/Pandas 数据处理 & 数据清洗 | Python, Pandas, NumPy |
| 🔍 业务分析 | Day 05 | 用户流失分析与 RFM 分群 | Pandas, 统计分析 |
| 📈 可视化 | Day 06 | 数据可视化与洞察提炼 | Matplotlib, Seaborn |
| 🌐 Web 应用 | Day 07 | Flask 交互式数据看板 | Flask, HTML/CSS/JS |
| ⚡ API 升级 | Day 08 | Flask API 强化 + 自动化测试 | Flask, pytest |
| 🧠 机器学习 | Day 09 | 特征工程与预处理流水线 | Scikit-learn Pipeline |
| 🤖 模型比较 | Day 10 | 三分类模型训练、比较与部署 | LR/DT/RF, joblib |

---

## 🗓️ 每日任务详解

### Day 03 — NumPy & Pandas 基础运算
> **掌握数据分析核心库的基础操作**

- NumPy 数组运算、矩阵操作、广播机制
- Pandas DataFrame 创建、索引、筛选、分组聚合
- 商品维度统计分析：品类分布、价格区间、销量排名
- 📁 `notebooks/day03_pandas_product_analysis.ipynb`

### Day 04 — 数据清洗与预处理
> **真实场景中的数据清洗完整流程**

- 缺失值检测与处理（中位数填充 / 删除策略）
- 异常值识别与修正（IQR 方法、Z-Score）
- 数据类型转换与标准化
- 用户行为数据清洗流水线
- 📁 产出：`ecommerce_customer_cleaned.csv`

### Day 05 — 用户流失分析与分群
> **RFM 模型 + 用户生命周期理论**

- 用户生命周期划分：新用户 / 0-6月 / 7-12月 / 13-24月 / 24月+
- RFM 模型构建（Recency, Frequency, Monetary）
- 流失用户识别与交叉分析
- 📁 `notebooks/day05_pm_student_project.ipynb`

### Day 06 — 数据可视化
> **将分析结果转化为可视化图表**

| 图表 | 类型 | 分析内容 |
|:----:|:----:|---------|
| 01 | 📊 柱状图 | 不同偏好品类的用户分布 |
| 02 | 🔵 散点图 | 用户行为特征关系 |
| 03 | 📈 折线图 | 生命周期阶段趋势 |
| 04 | 🥧 组合图 | 用户构成综合分析 |

### Day 07 — Flask Web 应用
> **将分析成果封装为交互式 Web 系统**

```
┌──────────────────────────────────────────────────┐
│                  Flask Web 系统                    │
├──────────┬──────────┬──────────┬─────────────────┤
│ 🔐 登录   │ 📊 看板  │ 🤖 问答  │ 📈 生命周期     │
│ /login   │ /dashboard│ /api/ask │ /segments       │
│ /logout  │ /download │ /assistant│                 │
└──────────┴──────────┴──────────┴─────────────────┘
     ↓           ↓           ↓           ↓
┌──────────────────────────────────────────────────┐
│              services/ 业务逻辑层                 │
│     data_service.py ｜ qa_service.py             │
└──────────────────────────────────────────────────┘
     ↓
┌──────────────────────────────────────────────────┐
│         data/ 数据层 + static/ 前端资源           │
└──────────────────────────────────────────────────┘
```

### Day 08 — Flask API 升级与测试 ⚡
> **将页面功能升级为可测试的 JSON API**

**新增 API 接口：**

| 接口 | 方法 | 功能 | 状态 |
|:----|:----:|------|:---:|
| `/health` | GET | 服务健康检查 | ✅ |
| `/api/metrics` | GET | 返回四张指标卡 JSON | ✅ |
| `/api/categories` | GET | 品类列表（支持 `?category=Fashion` 筛选） | ✅ |

**统一错误处理：**
```json
// 400 错误响应
{"ok": false, "error": "请求格式不正确。"}
```

**测试覆盖（9 项全部通过）：**
```
✅ /health 返回 200
✅ 未登录访问被拦截（302 重定向）
✅ 登录后 /api/metrics 返回完整数据
✅ /api/categories 品类筛选正确
✅ 登录认证（成功/失败）
✅ 400/404 错误处理
```

📁 `day08_flask_upgrade/` — 完整项目 + `tests/test_api.py`

### Day 09 — 机器学习准备：特征工程 🧠
> **第一次接触机器学习 — 理解特征、标签与数据流水线**

**核心概念理解：**
- **样本**：一名用户
- **特征**：判断时可查看的信息（使用月数、投诉情况等 20 个特征）
- **标签**：希望预测的答案（Churn 是否流失）
- **分类**：在"流失/未流失"中做出判断

**数据流水线：**

```
原始数据 (5630×22)
  → 排除 CustomerID + Churn
  → 分层划分 (stratify=y) → 训练集 4504 / 测试集 1126
  → 数值分支：中位数填充 + StandardScaler
  → 类别分支：众数填充 + OneHotEncoder
  → 36 列特征矩阵
  → 最低参照线 (DummyClassifier)
```

**成果文件：**
| 文件 | 内容 |
|:----|------|
| `feature_schema.csv` | 22 个字段的角色与处理方式 |
| `split_summary.csv` | 训练/测试集规模与流失比例 |
| `model_matrix_preview.csv` | 预处理后矩阵前 20 行 |
| `baseline_metrics.csv` | 最低参照线：准确率 83.1%，流失召回率 **0%** |

📁 `day09_ml_preparation/`

### Day 10 — 三分类模型训练、比较与应用 🤖
> **逻辑回归 vs 决策树 vs 随机森林 — 同一测试集公平较量**

**模型比较结果：**

| 模型 | 准确率 | 精确率 | 流失召回率 | 预测流失 | FN(漏报) | FP(误报) |
|:----|:-----:|:------:|:---------:|:--------:|:--------:|:--------:|
| ⚪ 最低参照线 | 83.1% | 0.0% | 0.0% | 0 | 190 | 0 |
| 🔵 逻辑回归 | 80.3% | 45.4% | 82.6% | 346 | 33 | 189 |
| 🟢 决策树 | 77.7% | 42.1% | 85.3% | 385 | 28 | 223 |
| 🟡 **随机森林 🏆** | **88.0%** | **60.5%** | **83.2%** | 261 | **32** | **103** |

**🏆 最终选择：随机森林 (Random Forest)**
- 准确率最高（88.0%），远超最低参照线
- 流失召回率优秀（83.2%），有效识别流失用户
- 漏报人数低（FN=32），误报控制最佳（FP=103）
- 100 棵树投票，比单棵决策树更稳定

**业务应用：**
- 输出 **261 名高风险客户** 优先关注名单
- 模型已保存并验证：`output/selected_model.joblib`
- 特征重要性 Top 3：`Tenure` > `Complain` > `TenureGroup_新用户`

📁 `day10_model_comparison/` — 全部 9 个成果文件

---

## 📊 核心发现

### 用户生命周期流失分析

| 阶段 | 用户数 | 流失率 | 风险 | 建议策略 |
|:----|:-----:|:-----:|:----:|---------|
| 👶 新用户 | 508 | **53.5%** | 🔴 极高 | 新手引导 + 首单优惠 |
| 🌱 0-6个月 | 1,642 | 25.9% | 🟠 高 | 活跃度激励 |
| 🌿 7-12个月 | 1,584 | 9.8% | 🟡 中 | 交叉销售 |
| 🌳 13-24个月 | 1,467 | 6.5% | 🟢 低 | 忠诚度维护 |
| 🏆 24个月以上 | 429 | 0.0% | ✅ 稳定 | VIP 权益 |

### 品类分析

| 偏好品类 | 用户数 | 流失率 | 平均订单 | 特征 |
|:--------|:-----:|:-----:|:--------:|------|
| 📱 Mobile Phone | 2,080 | 27.4% | 2.18 | 用户最多，流失最高 |
| 💻 Laptop & Accessory | 2,050 | 10.2% | 2.77 | 高价值用户群 |
| 👗 Fashion | 826 | 15.5% | 3.87 | 高活跃度 |
| 🛒 Grocery | 410 | 4.9% | 4.60 | 粘性最强 |
| 📦 Others | 264 | 7.6% | 5.25 | 低频但忠诚 |

### 机器学习重要发现

- **Tenure（使用月数）** 是最重要的预测特征（贡献 28.9%）
- **是否投诉** 是第二大特征（8.6%），说明投诉行为与流失高度相关
- **新用户** 群体流失风险远高于老用户，验证了业务分析结论
- 机器学习的结论与 Day 05 业务分析一致，形成 **数据→分析→模型→业务** 闭环

---

## 🚀 快速开始

### 环境要求
- Python 3.12+
- 推荐虚拟环境

### 分项目运行

```bash
# ├── Day 03: Pandas 基础分析
# │   cd day03_pandas_basics/
# │   jupyter notebook notebooks/day03_pandas_product_analysis.ipynb
# │
# ├── Day 04: 数据清洗
# │   cd day04_data_cleaning/
# │   jupyter notebook notebooks/day04_pm_user_cleaning_project.ipynb
# │
# ├── Day 05: 用户分析
# │   cd day05_user_analysis/
# │   jupyter notebook notebooks/day05_pm_student_project.ipynb
# │
# ├── Day 06: 可视化
# │   cd day06_visualization/
# │   jupyter notebook notebooks/day06_pm_student_visualization.ipynb
# │
# ├── Day 07: Flask Web 应用
# │   cd day07_web_app/
# │   pip install -r requirements.txt
# │   python app.py
# │   → http://127.0.0.1:5000 (student/day07)
# │   pytest tests/test_app.py
# │
# ├── Day 08: Flask API 升级
# │   cd day08_flask_upgrade/
# │   pip install -r requirements.txt
# │   python app.py
# │   → http://127.0.0.1:5500
# │   pytest tests/test_api.py  (9项测试 ✅)
# │
# ├── Day 09: ML 数据预处理
# │   cd day09_ml_preparation/
# │   python run_day09.py
# │   # 或使用 Jupyter:
# │   jupyter notebook notebooks/day09_ml_preparation_student.ipynb
# │
# └── Day 10: 模型比较
#     cd day10_model_comparison/
#     python run_day10.py
#     # 或使用 Jupyter:
#     jupyter notebook notebooks/day10_model_comparison_student.ipynb
```

---

## 🛠️ 技术栈全景

| 层级 | 技术 | 用途 |
|:----|:----|:----|
| 💾 数据处理 | Python, Pandas, NumPy | 数据清洗、特征工程、统计分析 |
| 📊 可视化 | Matplotlib, Seaborn | 品类分布、趋势分析、构成图 |
| 🌐 Web 框架 | Flask 3.x | REST API、模板渲染、会话管理 |
| 🎨 前端 | HTML5, CSS3, Vanilla JS | 响应式看板、交互式问答 |
| 🤖 机器学习 | Scikit-learn | Pipeline、LR/DT/RF、模型序列化 |
| ✅ 测试 | pytest | Flask 测试、断言验证 |
| 📦 版本控制 | Git, GitHub | 代码托管、提交管理 |

---

## 📁 项目结构

```
muc-commerce-3-24012474/
├── README.md                         # 项目主页（本文件）
├── SUBMISSION_CHECKLIST.md           # 提交检查清单
├── data/                             # 共享原始数据
│   ├── 淘宝全品类全国数据.csv         # Day 03 原始数据
│   └── E Commerce Dataset.xlsx       # Day 04-10 原始数据
├── scripts/                          # 共享验证脚本
│
├── day03_pandas_basics/              # Day 03: Pandas基础
│   ├── notebooks/day03_*.ipynb       #     Pandas探索分析
│   └── output/                       #     category + province 汇总
│
├── day04_data_cleaning/              # Day 04: 数据清洗
│   ├── notebooks/day04_*.ipynb       #     清洗流水线
│   └── output/                       #     6个清洗报告文件
│
├── day05_user_analysis/              # Day 05: 用户分析
│   ├── notebooks/day05_*.ipynb       #     RFM + 生命周期
│   └── output/                       #     overall/segment/cross
│
├── day06_visualization/              # Day 06: 可视化
│   ├── notebooks/day06_*.ipynb       #     4张图表
│   └── output/                       #     4PNG + chart_manifest
│
├── day07_web_app/                    # Day 07: Flask Web
│   ├── app.py                        #     主应用
│   ├── services/                     #     业务逻辑层
│   ├── templates/                    #     Jinja2模板
│   ├── static/                       #     前端资源+图表
│   ├── tests/                        #     Flask自动化测试
│   └── screenshots/                  #     验收截图
│
├── day08_flask_upgrade/              # Day 08: Flask API 升级
│   ├── app.py                        #     API 路由
│   ├── tests/test_api.py             #     9项测试全部通过 ✅
│   └── services/                     #     数据服务
│
├── day09_ml_preparation/             # Day 09: ML 预处理
│   ├── notebooks/                    #     特征工程Notebook
│   ├── run_day09.py                  #     完整运行脚本
│   └── output/                       #     4个成果文件
│
└── day10_model_comparison/           # Day 10: 模型比较
    ├── notebooks/                    #     三分类模型Notebook
    ├── run_day10.py                  #     完整运行脚本
    └── output/                       #     9个成果文件（含模型）
```

---

## ✅ 提交检查清单

| 检查项 | 状态 |
|:-------|:----:|
| Day 03: NumPy/Pandas 基础分析 | ✅ |
| Day 04: 数据清洗与预处理 | ✅ |
| Day 05: 用户流失分析与分群 | ✅ |
| Day 06: 数据可视化（4 张图表） | ✅ |
| Day 07: Flask Web 应用 | ✅ |
| Day 08: Flask API 升级 + 9 项测试 | ✅ |
| Day 09: ML 特征工程 + 4 个成果文件 | ✅ |
| Day 10: 三分类模型比较 + 9 个成果文件 | ✅ |
| GitHub 提交 | ✅ |

---

## 📝 实训总结

本次实训从 **Day 03 到 Day 10**，完成了一个完整的电商用户分析项目：

1. **数据处理**：从原始 CSV 到清洗后的结构化数据
2. **业务分析**：通过 RFM 和生命周期发现新用户流失率高达 53.5%
3. **可视化呈现**：4 张专业图表直观展示分析结论
4. **Web 系统**：Flask 框架构建交互式数据看板
5. **API 升级**：RESTful API + 自动化测试保障质量
6. **机器学习**：逻辑回归、决策树、随机森林公平比较
7. **模型部署**：随机森林模型序列化与预测管线

**核心价值**：从数据清洗到模型部署的全链路实践，形成了"**数据→分析→可视化→应用→模型→业务**"的完整闭环。

---

<div align="center">

**Built with ❤️ by 陈子萌 (24012474) · 中央民族大学 · 2026 暑期实训**

[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-red.svg)](https://pandas.pydata.org/)

</div>

# 🛒 E-Commerce User Analysis System

> **电商用户行为数据分析与可视化 Web 系统**  
> 基于 Python + Pandas + Flask 的完整数据分析项目，覆盖数据清洗 → 统计分析 → 可视化 → Web 应用开发全流程。

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-red.svg)
![pytest](https://img.shields.io/badge/tests-passing-brightgreen.svg)

**📅 实习周期**: Day 03 – Day 07 ｜ **🎯 主题**: 电商用户行为分析

</div>

---

## 📊 项目概览

本项目以 **淘宝全品类全国电商数据集** 为基础，通过 5 天的系统化训练，完成从原始数据到交互式 Web 数据分析应用的完整流程。

### 数据源

| 数据集 | 描述 | 规模 |
|--------|------|------|
| 淘宝全品类全国数据.csv | 用户行为日志（浏览、加购、收藏、购买） | ~10万+条 |
| E Commerce Dataset.xlsx | 用户画像与交易数据 | 5,630 名用户 |

---

## 🗓️ 每日任务总览

### Day 03 — NumPy & Pandas 基础

**目标**: 掌握数据分析核心库的基础操作

- ✅ NumPy 数组运算、矩阵操作
- ✅ Pandas DataFrame 创建、索引、筛选
- ✅ 商品维度统计分析（品类分布、价格区间、销量排名）
- ✅ 产出：`notebooks/day03_pandas_product_analysis.ipynb`

**核心技能**:
```
NumPy 基础 → Pandas 入门 → 商品数据分析 → 统计摘要生成
```

### Day 04 — 数据清洗与预处理

**目标**: 掌握真实场景中的数据清洗流程

- ✅ 缺失值检测与处理（填充/删除策略）
- ✅ 异常值识别与修正（IQR 方法、Z-Score）
- ✅ 数据类型转换与标准化
- ✅ 用户行为数据清洗流水线
- ✅ 产出：`ecommerce_customer_cleaned.csv`（清洗后数据集）

**清洗成果**:
```
原始数据 → 去重 → 缺失值处理 → 异常值修正 → 标准化 → 清洗后数据
```

### Day 05 — 用户流失分析与分群

**目标**: 运用 RFM 模型和用户生命周期理论进行深度分析

- ✅ 用户生命周期阶段划分（新用户/成长期/成熟期/休眠期/流失期）
- ✅ RFM 模型构建（Recency, Frequency, Monetary）
- ✅ 用户分群与特征提取
- ✅ 流失用户识别与风险评分
- ✅ 产出：`day05_pm_student_project.ipynb` + 用户分群报告

**分析维度**:
```
生命周期阶段 → 用户数 → 流失率 → 平均订单数 → 平均返现 → 风险评级
```

### Day 06 — 数据可视化

**目标**: 将分析结果转化为直观的可视化图表

- ✅ Matplotlib / Seaborn 高级图表绘制
- ✅ 品类用户比较柱状图（01_category_bar.png）
- ✅ 用户行为散点图（02_behavior_scatter.png）
- ✅ 生命周期趋势折线图（03_ordered_line.png）
- ✅ 用户构成饼图/堆叠图（04_composition_chart.png）
- ✅ 可视化总结面板（day06_visualization_summary.png）
- ✅ 产出：`output/day06_visualization/` 目录

**图表清单**:
| 图表编号 | 类型 | 内容 |
|---------|------|------|
| 01 | 柱状图 | 不同偏好品类用户比较 |
| 02 | 散点图 | 用户行为特征分布 |
| 03 | 折线图 | 生命周期阶段趋势 |
| 04 | 组合图 | 用户构成分析 |

### Day 07 — Flask Web 应用开发 ⭐

**目标**: 将分析成果封装为交互式 Web 应用

#### 系统架构

```
┌─────────────────────────────────────────────┐
│              Flask Web App (Day 07)           │
├──────────┬──────────┬───────────┬────────────┤
│  登录系统 │ 数据看板  │ 智能问答  │ 生命周期   │
│ /login   │ /dashboard│ /api/ask │ /segments  │
│ /logout  │ /download│ /assistant│            │
└──────────┴──────────┴───────────┴────────────┘
         ↓              ↓            ↓
   ┌─────────────────────────────────────┐
   │       services/ 业务逻辑层           │
   │  data_service.py │ qa_service.py   │
   └─────────────────────────────────────┘
         ↓
   ┌─────────────────────────────────────┐
   │         data/ 数据层                 │
   │  overall_metrics.csv                │
   │  category_analysis.csv              │
   │  segment_analysis.csv               │
   └─────────────────────────────────────┘
```

#### 功能模块

| 模块 | 路由 | 功能 |
|------|------|------|
| 🔐 登录系统 | `GET/POST /login` | 用户认证，Session 管理 |
| 📊 数据看板 | `GET /dashboard` | 4张指标卡 + 2张图表 + 品类筛选 |
| 🤖 智能问答 | `GET /assistant` + `POST /api/ask` | 5类离线规则问答 |
| 📈 生命周期 | `GET /segments` | 各阶段用户数/流失率明细表 |
| 📥 CSV导出 | `GET /download` | 按品类筛选结果导出 |
| 🔍 404页面 | `GET /*` | 自定义错误页面 |

#### 指标看板

| 指标卡 | 数值 | 单位 |
|--------|------|------|
| 总用户数 | 5,630 | 人 |
| 流失用户 | 948 | 人 |
| 总体流失率 | 16.8% | % |
| 平均订单数 | 2.96 | 单 |

#### 智能问答（5类规则）

1. **总用户数** → "系统中有多少用户？" → 5,630名
2. **总体流失率** → "总体流失率是多少？" → 16.8%
3. **偏好品类** → "哪个品类用户最多？" → Mobile Phone (2,080人)
4. **生命周期风险** → "哪个阶段风险最高？" → 新用户 (53.5%)
5. **平均订单数** → "平均订单数是多少？" → 2.96单

#### 自动化测试

```bash
pytest tests/test_app.py
```

测试覆盖：
- ✅ 登录/登出/拦截
- ✅ 看板页面渲染
- ✅ API 问答接口
- ✅ 品类筛选与CSV导出
- ✅ 生命周期页面
- ✅ 404错误处理

---

## 📁 项目结构

```
muc-commerce-3-24012474/
├── README.md                      # 项目主页（本文件）
├── requirements.txt               # 依赖包
├── SUBMISSION_CHECKLIST.md        # 提交检查清单
│
├── app.py                         # Flask 主应用
├── services/
│   ├── __init__.py
│   ├── data_service.py            # 数据加载与处理
│   └── qa_service.py              # 离线规则问答引擎
│
├── templates/                     # Jinja2 模板
│   ├── base.html                  # 基础布局
│   ├── login.html                 # 登录页
│   ├── dashboard.html             # 数据看板
│   ├── assistant.html             # 智能问答
│   ├── segments.html              # 生命周期页
│   └── 404.html                   # 错误页
│
├── static/
│   ├── css/style.css              # 全局样式
│   ├── js/assistant.js            # 问答前端逻辑
│   └── images/                    # 可视化图表
│       ├── 01_category_bar.png    # 品类柱状图
│       ├── 02_behavior_scatter.png # 行为散点图
│       ├── 03_ordered_line.png    # 趋势折线图
│       ├── 04_composition_chart.png # 构成图
│       └── day06_visualization_summary.png
│
├── data/                          # 数据文件
│   ├── overall_metrics.csv        # 整体指标汇总
│   ├── category_analysis.csv      # 品类分析
│   └── segment_analysis.csv       # 生命周期分群
│
├── screenshots/                   # 验收截图
│   ├── 01_login.png
│   ├── 02_dashboard.png
│   ├── 03_interaction.png
│   ├── 04_assistant.png
│   └── README.md
│
├── tests/
│   └── test_app.py                # Flask 自动化测试
│
├── ecommerce-user-analysis-seed/  # Day 03-05 种子项目
│   ├── notebooks/                 # Jupyter 笔记本
│   ├── docs/                      # 任务文档
│   ├── scripts/                   # 验证脚本
│   └── output/                    # 分析产出
│
├── day6/                          # Day 06 可视化项目
│   ├── notebooks/                 # 可视化 Notebook
│   ├── output/                    # 图表产出
│   └── docs/                      # 教学材料
│
└── Day07/                         # Day 07 Web 应用（副本）
    └── ... (同上)
```

---

## 🚀 快速开始

### 环境要求

- Python 3.12+
- 推荐虚拟环境

### 安装与运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 Flask 应用
python app.py

# 3. 浏览器访问
# http://127.0.0.1:5000
# 登录账号: student / day07

# 4. 运行自动化测试
pytest tests/test_app.py
```

---

## 📈 核心发现

### 用户流失洞察

| 生命周期阶段 | 用户数 | 流失人数 | 流失率 | 风险等级 |
|------------|--------|---------|--------|---------|
| 👶 新用户 | 508 | 272 | **53.5%** | 🔴 极高 |
| 🌱 0-6个月 | 1,642 | 425 | 25.9% | 🟠 高 |
| 🌿 7-12个月 | 1,584 | 156 | 9.8% | 🟡 中 |
| 🌳 13-24个月 | 1,467 | 95 | 6.5% | 🟢 低 |
| 🏆 24个月以上 | 429 | 0 | 0.0% | ✅ 稳定 |

### 品类用户分布

| 偏好品类 | 用户数 | 流失率 | 平均订单数 |
|---------|--------|--------|-----------|
| 📱 Mobile Phone | 2,080 | 27.4% | 2.18 |
| 💻 Laptop & Accessory | 2,050 | 10.2% | 2.77 |
| 👗 Fashion | 826 | 15.5% | 3.87 |
| 🛒 Grocery | 410 | 4.9% | 4.60 |
| 📦 Others | 264 | 7.6% | 5.25 |

**关键发现**:
- 🎯 新用户流失率高达 **53.5%**，是运营重点
- 📱 Mobile Phone 用户最多但流失率也最高
- 🛒 Grocery 品类流失率最低（4.9%），用户粘性最强
- 💻 Laptop 品类用户多且流失率低，是高价值品类

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 数据分析 | Python, Pandas, NumPy |
| 可视化 | Matplotlib, Seaborn |
| Web 框架 | Flask 3.x |
| 前端 | HTML5, CSS3, Vanilla JS |
| 测试 | pytest |
| 版本控制 | Git, GitHub |

---

## 📝 实习日志

| 日期 | 主题 | 关键产出 |
|------|------|---------|
| Day 03 | NumPy & Pandas 基础 | 商品维度统计分析 Notebook |
| Day 04 | 数据清洗与预处理 | 清洗后数据集 + 清洗流水线 |
| Day 05 | 用户流失与分群 | RFM模型 + 生命周期分析 |
| Day 06 | 数据可视化 | 4张专业图表 + 可视化面板 |
| Day 07 | Flask Web 应用 | 完整数据分析 Web 系统 |

---

## 📄 License

MIT License

---

<div align="center">

**Built with ❤️ using Python + Flask + Pandas**

[📊 查看数据看板](http://127.0.0.1:5000) · [🤖 智能问答](http://127.0.0.1:5000/assistant) · [📈 生命周期分析](http://127.0.0.1:5000/segments)

</div>

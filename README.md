# Day 07 · 电商用户行为分析实训

## Web 数据展示项目：登录、看板、筛选与离线问答

---

## 基本信息

- **姓名**：（请填写）
- **学号**：（请填写）
- **项目**：电商用户行为分析 Web 数据展示
- **数据来源**：第5天统计分析 + 第6天可视化图表

---

## 核心功能

| 功能 | 说明 |
|---|---|
| **登录闭环** | Session 简化登录，账号 `student` / 密码 `day07` |
| **数据看板** | 4个核心指标卡 + 4张图表 + 生命周期表格 |
| **品类筛选** | 下拉框切换品类，URL 同步参数，实时刷新 |
| **离线问答** | 5类支持问题 + 不支持问题友好提示 |
| **拓展A** | 导出当前筛选结果 CSV |
| **拓展B** | 生命周期详情页 `/segments` |
| **拓展C** | Flask 自动化测试 |

---

## 项目结构

```
Day07/
├── app.py                      # Flask 主应用
├── requirements.txt            # 依赖列表
├── README.md                   # 本文件
├── .gitignore
├── data/                       # 数据文件（只读）
│   ├── E Commerce Dataset.xlsx
│   ├── overall_metrics.csv
│   ├── segment_analysis.csv
│   ├── cross_analysis.csv
│   └── chart_manifest.csv
├── services/
│   ├── __init__.py
│   ├── data_service.py         # 数据读取与处理
│   └── qa_service.py           # 离线问答逻辑
├── templates/
│   ├── login.html              # 登录页
│   ├── dashboard.html          # 数据看板
│   └── segments.html           # 生命周期详情
├── static/
│   └── images/                 # 第6天图表
│       ├── 01_category_bar.png
│       ├── 02_behavior_scatter.png
│       ├── 03_ordered_line.png
│       ├── 04_composition_chart.png
│       └── day06_visualization_summary.png
├── screenshots/                # 验收截图
│   ├── 01_login.png
│   ├── 02_dashboard.png
│   ├── 03_interaction.png
│   ├── 04_assistant.png
│   └── 05_extension.png
└── tests/
    └── test_app.py             # 自动化测试
```

---

## 运行方法

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 Flask
python app.py

# 浏览器访问 http://127.0.0.1:5000
```

---

## 验收账号

| 账号 | 密码 |
|---|---|
| `student` | `day07` |

---

## 拓展任务

本次完成 **拓展A + 拓展B + 拓展C** 全部三项：

- **拓展A**：`/download?category=Fashion` 导出筛选 CSV
- **拓展B**：`/segments` 生命周期详情页，含数据观察
- **拓展C**：`pytest tests/test_app.py` 自动化测试覆盖登录、看板、问答

---

## 未解决问题

（如有请填写）

---

## 评分项对照

| 评分项 | 状态 |
|---|---|
| 核心TODO与数据展示 (60分) | ✅ 完成 |
| 登录、筛选与问答验收 (15分) | ✅ 完成 |
| 必选拓展三选一 (15分) | ✅ 完成（三项全选） |
| README、证据与现场演示 (10分) | ✅ 完成 |

# campus-market-24012474

> 电商用户数据分析与可视化项目 | E-commerce User Analysis & Visualization

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-3.0-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-orange)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626)
![Status](https://img.shields.io/badge/Status-Completed-success)

## Project Overview

Full-stack data analysis of **5,630 e-commerce users** across 22 dimensions, covering data cleaning, multi-dimensional analysis, and data visualization. This project simulates a real-world e-commerce运营 scenario where data-driven decisions are made to identify churn risks and user behavior patterns.

### Key Business Questions
- How does **user lifecycle stage** correlate with churn rate?
- What is the relationship between **order behavior** and **cashback amount**?
- How do **complaint status** and **payment preference** differ across user segments?

---

## Project Structure

```
campus-market-24012474/
├── notebooks/                    # Jupyter Notebooks
│   ├── day03_pandas_product_analysis.ipynb
│   ├── day04_pm_user_cleaning_project.ipynb
│   ├── day05_pm_student_project.ipynb      # [Completed] Statistical Analysis
│   └── day06_pm_student_visualization.ipynb # [Completed] Data Visualization
├── output/                      # Deliverables
│   ├── day04_project/           # Cleaned Data
│   ├── day05_analysis/          # Analysis Reports (CSV)
│   └── day06_visualization/     # Charts & Manifest
├── data/                        # Raw Data
├── scripts/                     # Validation Scripts
└── README.md                    # You are here
```

---

## Day 5: Multi-Dimensional Analysis

**Topic A - User Lifecycle Analysis**

| Metric | Value |
|---|---|
| Total Users | 5,630 |
| Overall Churn Rate | **16.84%** |
| Avg Orders per User | 2.96 |
| Avg Cashback | ¥177.22 |

### Key Findings

1. **Churn drops dramatically with lifecycle** — New users churn at **53.5%**, while users with 24+ months have **0% churn**. Early retention is critical.

2. **New Users + Cash on Delivery = 72.4% churn** — This combination has the highest churn risk across all segments, suggesting trust-building interventions are needed for new users who choose COD.

3. **Order count and cashback correlate with retention** — Churned users consistently show lower order frequency and cashback amounts across all lifecycle stages.

---

## Day 6: Data Visualization

### Chart Gallery

| Chart | Type | Business Question |
|---|---|---|
| ![Bar](output/day06_visualization/01_category_bar.png) | **Bar Chart** | Churn rate across lifecycle stages |
| ![Scatter](output/day06_visualization/02_behavior_scatter.png) | **Scatter Plot** | Order count vs cashback by churn status |
| ![Line](output/day06_visualization/03_ordered_line.png) | **Line Chart** | Churn rate trend across ordered stages |
| ![Pie](output/day06_visualization/04_composition_chart.png) | **Composition Chart** | Complaint status distribution |
| ![Dashboard](output/day06_visualization/day06_visualization_summary.png) | **2x2 Dashboard** | Comprehensive overview |

---

## Technologies Used

- **Python 3.14** | Pandas, NumPy for data analysis
- **Matplotlib** for publication-quality charts
- **Jupyter Notebook** for interactive development
- **Git & GitHub** for version control

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run validation
python scripts/validate_submission.py
```

---

## Validation Status

All Day 5 & Day 6 deliverables validated successfully:
- [x] 3 CSV analysis reports
- [x] 4 individual charts + 1 summary dashboard
- [x] Complete chart manifest (`chart_manifest.csv`)
- [x] All notebooks pass structural checks

---

*Student Project | Steve-cza | 2026*

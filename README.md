# SAP Document & Compliance Master Data Quality Audit Tool

## Overview

This project simulates a SAP-like master data quality audit process focused on document and compliance records.

The tool identifies data quality issues such as expired active documents, missing approvals, inactive owners, invalid date sequences, missing review cycles, missing file references, and incomplete ownership records.

The project uses synthetic SAP-like data and demonstrates how Python, SQL, and Streamlit can be used to automate data quality audits, calculate risk-based scores, and generate executive remediation reports.

---

## Business Problem

In regulated industries such as aerospace, manufacturing, supply chain, and quality management, poor data quality in document and compliance records can create audit exposure, missed renewals, unclear ownership, obsolete documentation, and delayed corrective actions.

Companies often rely on SAP exports, spreadsheets, and manual reviews to monitor document status, approvals, expiration dates, ownership, and review cycles. This manual process increases the risk of missed issues and weak audit readiness.

---

## Objective

Build an automated data quality audit tool that:

- Reviews SAP-like document and compliance master data
- Applies documented data quality rules
- Detects high-risk records
- Calculates a risk-based data quality score
- Classifies documents by risk category
- Generates exception reports
- Creates a remediation backlog
- Displays executive KPIs in a dashboard

---

## Scope

This project focuses on document and compliance master data, including:

- NDAs
- Contracts
- Standard Operating Procedures
- Work Instructions
- Quality Records
- Compliance Documents
- Approval Records
- Document Owners
- Expiration Dates
- Review Cycles
- Document Versions
- Document Status
- Business Areas
- Plant or operating locations

---

## Out of Scope

This project does not include:

- Vendor Master
- Material Master
- Real SAP data
- Confidential company data
- Live SAP system integration
- Financial transactions
- Purchase orders
- Inventory records
- Customer master data

---

## Tools Used

- Python
- Pandas
- NumPy
- SQL
- PostgreSQL-compatible SQL scripts
- Streamlit
- Plotly
- CSV files
- GitHub

---

## Repository Structure

```text
sap-document-compliance-data-quality-audit-tool/
│
├── data/
│   ├── raw/
│   │   ├── sap_document_master.csv
│   │   ├── owner_directory.csv
│   │   └── approval_history.csv
│   │
│   └── processed/
│       ├── cleaned_document_master.csv
│       ├── cleaned_owner_directory.csv
│       ├── cleaned_approval_history.csv
│       ├── audit_results.csv
│       └── document_quality_scores.csv
│
├── dashboard/
│   └── app.py
│
├── docs/
│   ├── project_scope.md
│   ├── data_dictionary.md
│   └── business_rules.md
│
├── reports/
│   ├── executive_summary.csv
│   ├── exception_report.csv
│   └── remediation_backlog.csv
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_quality_views.sql
│   ├── 03_kpi_queries.sql
│   └── 04_data_quality_checks.sql
│
├── src/
│   ├── generate_sample_data.py
│   ├── clean_data.py
│   ├── run_quality_audit.py
│   ├── calculate_scores.py
│   └── export_reports.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Data Sources

The project uses three synthetic CSV files:

| File | Description |
|---|---|
| `sap_document_master.csv` | Main SAP-like document and compliance master data |
| `owner_directory.csv` | Document owner reference table |
| `approval_history.csv` | Approval records linked to documents |

All data is synthetic and generated using Python.

---

## Data Quality Rules

The audit engine applies documented rules such as:

| Rule ID | Rule Name | Severity |
|---|---|---|
| DQ-001 | Active Document Is Expired | Critical |
| DQ-002 | Missing Document Owner | High |
| DQ-003 | Inactive Owner Assigned | High |
| DQ-004 | Active Document Missing Approval | Critical |
| DQ-005 | Confidential Document Missing Approval | Critical |
| DQ-006 | Invalid Date Sequence | Critical |
| DQ-007 | Missing Next Review Date | Medium |
| DQ-008 | Review Overdue | Medium |
| DQ-009 | Missing Version | Medium |
| DQ-010 | Missing File Reference | Medium |
| DQ-011 | Draft Document Open Too Long | Medium |
| DQ-012 | Missing Business Area | Low |
| DQ-013 | Missing Plant | Low |
| DQ-014 | Invalid Approval History | High |

Full rule details are documented in:

```text
docs/business_rules.md
```

---

## Data Quality Score Model

Each document starts with a score of 100 points.

Penalty points are deducted based on issue severity:

| Severity | Score Impact |
|---|---:|
| Critical | -30 |
| High | -20 |
| Medium | -10 |
| Low | -5 |

The final score is calculated as:

```text
Data Quality Score = 100 - Total Penalty Points
```

Scores cannot go below 0.

---

## Risk Categories

| Data Quality Score | Risk Category |
|---:|---|
| 90 - 100 | Healthy |
| 75 - 89 | Low Risk |
| 60 - 74 | Medium Risk |
| 40 - 59 | High Risk |
| 0 - 39 | Critical Risk |

---

## Main Outputs

The pipeline generates:

| Output File | Description |
|---|---|
| `audit_results.csv` | All detected audit issues |
| `document_quality_scores.csv` | Final score and risk category by document |
| `executive_summary.csv` | Executive-level KPI summary |
| `exception_report.csv` | Detailed exception report |
| `remediation_backlog.csv` | Prioritized corrective action backlog |

---

## How to Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full pipeline:

```bash
python main.py
```

This command will:

1. Generate synthetic SAP-like datasets
2. Clean and standardize the data
3. Apply data quality audit rules
4. Calculate quality scores
5. Export executive reports and remediation backlog

---

## How to Run the Dashboard

After running the full pipeline, start the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

The dashboard includes:

- Executive KPIs
- Documents by risk category
- Issues by severity
- Top audit rules by issue count
- Average quality score by business area
- Highest risk documents
- Remediation backlog
- Exception report

---

## SQL Layer

The `sql/` folder includes PostgreSQL-compatible scripts for:

- Creating tables
- Creating analytical views
- Running KPI queries
- Validating audit rules with SQL checks

SQL files:

| File | Purpose |
|---|---|
| `01_create_tables.sql` | Creates database tables |
| `02_quality_views.sql` | Creates analytical views |
| `03_kpi_queries.sql` | Provides executive KPI queries |
| `04_data_quality_checks.sql` | Provides SQL checks aligned to audit rules |

---

## Documentation

| File | Description |
|---|---|
| `docs/project_scope.md` | Defines project scope, objective, and exclusions |
| `docs/data_dictionary.md` | Documents all input and output fields |
| `docs/business_rules.md` | Documents severity levels, audit rules, scoring, and remediation priority |

---

## Why Synthetic Data?

Real SAP and compliance data cannot be shared publicly due to confidentiality.

This project uses synthetic data designed to reflect realistic enterprise data quality problems, including:

- Expired active documents
- Missing approvals
- Inactive document owners
- Missing review dates
- Overdue reviews
- Invalid date sequences
- Missing file references
- Missing business ownership fields

---

## Business Value

This tool helps compliance, quality, operations, supply chain, and business systems teams:

- Improve audit readiness
- Identify risky records before audits
- Prioritize corrective actions
- Reduce manual spreadsheet review
- Improve document control governance
- Create visibility into master data quality

---

## Key Skills Demonstrated

- SAP-like data analysis
- Data quality auditing
- Compliance data governance
- Python automation
- Pandas data processing
- SQL modeling and validation
- Risk scoring logic
- Dashboard development
- Executive reporting
- Remediation backlog creation

---

## Confidentiality Notice

This project does not use real SAP data, vendor master data, material master data, or confidential company information.

All datasets are synthetic and created for portfolio demonstration purposes.
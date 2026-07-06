cat > docs/project_scope.md << 'EOF'
# Project Scope

## Project Name

SAP Document & Compliance Master Data Quality Audit Tool

## Business Problem

In regulated industries such as aerospace, manufacturing, supply chain, and quality management, poor data quality in SAP-like document and compliance records can create audit exposure, missed renewals, unclear ownership, obsolete documentation, and delayed corrective actions.

Organizations often rely on SAP exports, spreadsheets, and manual reviews to monitor document status, approvals, expiration dates, ownership, and review cycles. This creates a risk of inconsistent data, late renewals, and incomplete audit readiness.

## Objective

Build an automated data quality audit tool that reviews SAP-like document and compliance master data, identifies data quality issues, calculates a risk-based quality score, and generates exception reports and remediation backlogs.

## Scope

This project focuses on SAP-like document and compliance master data, including:

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
- Plants or Operating Locations

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

## Data Sources

The project will use syntethic CSV files that simulate SAP-like exports:

- sap_document_master.csv
- owner-directory.csv
- approval_history.csv

These files will be generated using Python and stored under the data/raw folder.

## Main Process Flow

1. Generate syntethic SAP-like document and compliance data.
2. Load raw CSV files.
3. Clean and standardize the data.
4. Apply data quality validation rules.
5. Detect issues and assign severity levels.
6. Calculate a risk-based data quality score.
7. Generate exception reports.
8. Create a remediation backlog.
9. Display results in an executive dashboard.

## Tools Used

- Python
- Pandas
- NumPy
- SQL
- PostgreSQL
- Streamlit
- Plotly
- CSV Files
- GitHub

## Main Deliverables

- Syntethic SAP-like dataset
- Data dictionary
- Business rules documentation
- Data cleaning scripts
- Automated quality audit rules
- Risk scoring model
- Exception report
- Remediation backlog
- Executive dashboard
- SQL validation queries
- GitHub repository documentation

## Business Value

This tool helps compliance, supply chain, quality, operations, and business systems teams identify risky document records before audits, prioritize corrective actions, and improve data governance.

The project demonstrates how SAP-like data exports can be transformed into actionable audit insights using Python, SQL, and automation.

## Confidentiality Note

This project does not use real SAP data or confidential company information. All data is syntethic and created for portafolio and demonstration purposes.
EOF
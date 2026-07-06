cat > docs/data_dictionary.md << 'EOF'
# Data Dictionary

This document describes syntethic SAP-like datasets used in the SAP Document & Compliance Master Data Quality Audit Tool.

The project uses three main raw data files:

1. sap_document_master.csv
2. owner_directory.csv
3. approval_history.csv

These files simulate SAP-like exports related to document control, compliance records, approvals, ownership, expiration dates and review cycles.

---

# 1. sap_document_master.csv

This file contains the main document and compliance master data records.

| Field Name | Data Type | Description | Example |
|---|---|---|---|
| document_id | String | Unique identifier for each document | DOC-10001 |
| document_type | String | Type of document | NDA, Contract, SOP, Work Instruction, Quality Record |
| document_title | String | Title or short description of the document | Supplier NDA Agreement |
| business_area | String | Business area responsible for the document | Supply Chain, Quality, Engineering |
| plant | String | Operating location or plant code | CHI-01 |
| owner_id | String | ID of the person responsible for the document | OWN-001 |
| status | String | Current document status | Active, Expired, Obsolete, Draft, Pending Approval |
| version | String | Current document version or revision | v1.0, v2.1 |
| effective_date | Date | Date when the document became effective | 2025-01-15 |
| expiration_date | Date | Date when the document expires | 2026-01-15 |
| last_review_date | Date | Date when the document was last reviewed | 2025-07-15 |
| next_review_date | Date | Date when the document should be reviewed again | 2026-07-15 |
| approval_status | String | Approval state of the document | Approved, Pending, Rejected, Missing |
| confidentiality_level | String | Sensitivity classification of the document | Public, Internal, Confidential, Restricted |
| file_reference | String | Simulated file path or SAP document reference | SAP/DOCS/DOC-10001.pdf |
| created_date | Date | Date when the record was created | 2024-12-01 |
| updated_date | Date | Date when the record was last updated | 2025-12-15 |

---

# 2. owner_directory.csv

This file contains information about document owners.

| Field Name | Data Type | Description | Example |
|---|---|---|---|
| owner_id | String | Unique owner identifier | OWN-001 |
| owner_name | String | Name of the document owner | Maria Lopez |
| department | String | Owner department | Supply Chain |
| role | String | Owner job role | Compliance Analyst |
| active_flag | Boolean | Indicates whether the owner is currently active | True, False |
| email | String | Simulated email address | maria.lopez@example.com |

---

# 3. approval_history.csv

This file contains approval records related to documents.

| Field Name | Data Type | Description | Example |
|---|---|---|---|
| approval_id | String | Unique approval record identifier | APR-50001 |
| document_id | String | Document linked to the approval record | DOC-10001 |
| approver_name | String | Name of the approver | John Smith |
| approval_date | Date | Date when the approval was completed | 2025-01-10 |
| approval_result | String | Approval decision | Approved, Rejected, Pending |
| comments | String | Approval notes or comments | Approved for annual use |

---

# 4. Processed Output Files

The project will generate the following processed files.

## cleaned_document_master.csv

Cleaned version of the raw document master data.

Main transformations:

- Standardized date fileds
- Trimmed text fields
- Normalized status values
- Normalized approval status values
- Standardized document types
- Validated missing values

## audit_results.csv

Contains all data quality issues detected by the audit rules.

| Field Name | Data Type | Description |
|---|---|---|
| audit_id | String | Unique audit result identifier |
| document_id | String | Document being audited |
| rule_id | String | Data quality rule identifier |
| rule_name | String | Name of the rule applied |
| severity | String | Low, Medium, High, or Critical |
| issue_detected | Boolean | Indicates if an issue was detected |
| issue_description | String | Description of the issue |
| recommended_action | String | Suggested remediation action |

## document_quality_scores.csv

Contains the final quality score per document.

| Field Name | Data Type | Description |
|---|---|---|
| document_id | String | Document identifier |
| total_issues | Integer | Number of issues detected |
| critical_issues | Integer | Number of critical issues |
| high_issues | Integer | Number of high severity issues |
| medium_issues | Integer | Number of medium severity issues |
| low_issues | Integer | Number of low severity issues |
| data_quality_score | Integer | Final quality score from 0 to 100 |
| risk_category | String | Healthy, Low Risk, Medium Risk, High Risk, Critical Risk |

## remediation_backlog.csv

Contains prioritized corrective actions.

| Field Name | Data Type | Description |
|---|---|---|
| priority | String | Critical, High, Medium, Low |
| document_id | String | Document requiring remediation |
| document_title | String | Title of the document |
| business_area | String | Responsible business area |
| owner_id | String | Assigned owner |
| issue_description | String | Description of the issue |
| recommended_action | String | Action needed to fix the issue |
| target_resolution_days | Integer | Suggested number of days to resolve |

---

# 5. Notes

All data used in this project is synthetic. No real SAP records, confidential company data, vendor master data, or material master data are used.
EOF
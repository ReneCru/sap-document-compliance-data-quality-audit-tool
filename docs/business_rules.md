cat > docs/business_rules.md << 'EOF'
# Business Rules

## Overview

This document defines the data quality validation rules used in the SAP Document & Compliance Master Data Quality Audit Tool.

The rules are designed to identify data quality issues in SAP-like document and compliance master data, assign severity levels, calculate risk-based scores, and generate remediation actions.

---

# 1. Severity Levels

Each data quality issue is classified using one of the following severity levels:

| Severity | Description | Score Impact |
|---|---|---:|
| Critical | Major compliance or audit risk | -30 |
| High | Significant ownership, approval, or process risk | -20 |
| Medium | Moderate data quality or process control issue | -10 |
| Low | Minor formatting or completeness issue | -5 |

---

# 2. Data Quality Score Model

Each document starts with a score of 100 points.

Points are deducted based on the severity of each issue detected.

## Score Formula

```text
Data Quality Score = 100 - Total Penalty Points

---

# 3. Risk Categories

| Data Quality Score | Risk Category |
| -----------------: | ------------- |
|           90 - 100 | Healthy       |
|            75 - 89 | Low Risk      |
|            60 - 74 | Medium Risk   |
|            40 - 59 | High Risk     |
|             0 - 39 | Critical Risk |

---

# 4. Audit Rules

Rule DQ-001: Active Document is Expired

| Field                  | Value                                                                          |
| ---------------------- | ------------------------------------------------------------------------------ |
| Rule ID                | DQ-001                                                                         |
| Rule Name              | Active Document Is Expired                                                     |
| Severity               | Critical                                                                       |
| Logic                  | status = Active AND expiration_date < current_date                             |
| Issue Description      | Document is marked as active but the expiration date has already passed.       |
| Recommended Action     | Renew the document, update the expiration date, or change the document status. |
| Target Resolution Days | 7                                                                              |

---

Rule DQ-002: Missing Document Owner

| Field                  | Value                                     |
| ---------------------- | ----------------------------------------- |
| Rule ID                | DQ-002                                    |
| Rule Name              | Missing Document Owner                    |
| Severity               | High                                      |
| Logic                  | owner_id is blank or null                 |
| Issue Description      | Document does not have an assigned owner. |
| Recommended Action     | Assign an active document owner.          |
| Target Resolution Days | 10                                        |

---

Rule DQ-003: Inactive Owner Assigned

| Field                  | Value                                         |
| ---------------------- | --------------------------------------------- |
| Rule ID                | DQ-003                                        |
| Rule Name              | Inactive Owner Assigned                       |
| Severity               | High                                          |
| Logic                  | document owner exists but active_flag = False |
| Issue Description      | Document is assigned to an inactive owner.    |
| Recommended Action     | Reassign the document to an active owner.     |
| Target Resolution Days | 10                                            |

---

Rule DQ-004: Active Document Missing Approval

| Field                  | Value                                                             |
| ---------------------- | ----------------------------------------------------------------- |
| Rule ID                | DQ-004                                                            |
| Rule Name              | Active Document Missing Approval                                  |
| Severity               | Critical                                                          |
| Logic                  | status = Active AND approval_status is Missing, Pending, or blank |
| Issue Description      | Active document does not have a valid approval status.            |
| Recommended Action     | Route the document for approval or update the approval record.    |
| Target Resolution Days | 7                                                                 |

---

Rule DQ-005: Confidential Document Missing Approval

| Field                  | Value                                                                                   |
| ---------------------- | --------------------------------------------------------------------------------------- |
| Rule ID                | DQ-005                                                                                  |
| Rule Name              | Confidential Document Missing Approval                                                  |
| Severity               | Critical                                                                                |
| Logic                  | confidentiality_level in Confidential or Restricted AND approval_status is not Approved |
| Issue Description      | Confidential or restricted document does not have formal approval.                      |
| Recommended Action     | Obtain formal approval for the document.                                                |
| Target Resolution Days | 7                                                                                       |

---

Rule DQ-006: Invalid Date Sequence

| Field                  | Value                                               |
| ---------------------- | --------------------------------------------------- |
| Rule ID                | DQ-006                                              |
| Rule Name              | Invalid Date Sequence                               |
| Severity               | Critical                                            |
| Logic                  | expiration_date < effective_date                    |
| Issue Description      | Expiration date is earlier than the effective date. |
| Recommended Action     | Correct the effective date or expiration date.      |
| Target Resolution Days | 7                                                   |

---

Rule DQ-007: Missing Next Review Date

| Field                  | Value                                                             |
| ---------------------- | ----------------------------------------------------------------- |
| Rule ID                | DQ-007                                                            |
| Rule Name              | Missing Next Review Date                                          |
| Severity               | Medium                                                            |
| Logic                  | next_review_date is blank or null                                 |
| Issue Description      | Document does not have a scheduled next review date.              |
| Recommended Action     | Define the next review date based on the document control policy. |
| Target Resolution Days | 20                                                                |

---

Rule DQ-008: Review Overdue

| Field                  | Value                                                     |
| ---------------------- | --------------------------------------------------------- |
| Rule ID                | DQ-008                                                    |
| Rule Name              | Review Overdue                                            |
| Severity               | Medium                                                    |
| Logic                  | next_review_date < current_date AND status = Active       |
| Issue Description      | Active document is overdue for review.                    |
| Recommended Action     | Complete the document review and update the review cycle. |
| Target Resolution Days | 15                                                        |

---

Rule DQ-009: Missing Version

| Field                  | Value                                           |
| ---------------------- | ----------------------------------------------- |
| Rule ID                | DQ-009                                          |
| Rule Name              | Missing Version                                 |
| Severity               | Medium                                          |
| Logic                  | version is blank or null                        |
| Issue Description      | Document version is missing.                    |
| Recommended Action     | Update the document version or revision number. |
| Target Resolution Days | 20                                              |

---

Rule DQ-010: Missing File Reference

| Field                  | Value                                                                            |
| ---------------------- | -------------------------------------------------------------------------------- |
| Rule ID                | DQ-010                                                                           |
| Rule Name              | Missing File Reference                                                           |
| Severity               | Medium                                                                           |
| Logic                  | file_reference is blank or null                                                  |
| Issue Description      | Document does not have a file reference or SAP document link.                    |
| Recommended Action     | Add the correct file path, SAP document reference, or document storage location. |
| Target Resolution Days | 20                                                                               |

---

Rule DQ-011: Draft Document Open Too Long

| Field                  | Value                                                    |
| ---------------------- | -------------------------------------------------------- |
| Rule ID                | DQ-011                                                   |
| Rule Name              | Draft Document Open Too Long                             |
| Severity               | Medium                                                   |
| Logic                  | status = Draft AND created_date is older than 60 days    |
| Issue Description      | Draft document has remained open for more than 60 days.  |
| Recommended Action     | Approve, reject, complete, or cancel the draft document. |
| Target Resolution Days | 20                                                       |

---

Rule DQ-012: Missing Business Area

| Field                  | Value                                            |
| ---------------------- | ------------------------------------------------ |
| Rule ID                | DQ-012                                           |
| Rule Name              | Missing Business Area                            |
| Severity               | Low                                              |
| Logic                  | business_area is blank or null                   |
| Issue Description      | Document does not have a business area assigned. |
| Recommended Action     | Assign the correct business area.                |
| Target Resolution Days | 30                                               |

---

Rule DQ-013: Missing Plant

| Field                  | Value                                                          |
| ---------------------- | -------------------------------------------------------------- |
| Rule ID                | DQ-013                                                         |
| Rule Name              | Missing Plant                                                  |
| Severity               | Low                                                            |
| Logic                  | plant is blank or null                                         |
| Issue Description      | Document does not have a plant or operating location assigned. |
| Recommended Action     | Assign the correct plant or operating location.                |
| Target Resolution Days | 30                                                             |

---

Rule DQ-014: Invalid Approval History

| Field                  | Value                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------- |
| Rule ID                | DQ-014                                                                                      |
| Rule Name              | Invalid Approval History                                                                    |
| Severity               | High                                                                                        |
| Logic                  | approval_status = Approved but no approved record exists in approval_history                |
| Issue Description      | Document is marked as approved, but no approval record exists in the approval history file. |
| Recommended Action     | Add the missing approval history record or correct the approval status.                     |
| Target Resolution Days | 10                                                                                          |

---

5. Remediation Priority

| Severity | Priority | Target Resolution Days |
| -------- | -------- | ---------------------: |
| Critical | Critical |                      7 |
| High     | High     |                     10 |
| Medium   | Medium   |                15 - 20 |
| Low      | Low      |                     30 |

---

6. Notes

These rules are designed for synthetic SAP-like document and compliance data.

The project does not use vendor master data, material master data, real SAP data, or confidential company information.

Pero ojo: **este comando puede fallar** porque adentro usamos un bloque Markdown con triple backticks:

```text id="62qvak"
```text
Data Quality Score = 100 - Total Penalty Points
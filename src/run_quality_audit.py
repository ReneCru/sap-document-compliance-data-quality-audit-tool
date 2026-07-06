import os
from datetime import datetime, timedelta

import pandas as pd


PROCESSED_DATA_PATH = "data/processed"

DOCUMENT_MASTER_FILE = os.path.join(PROCESSED_DATA_PATH, "cleaned_document_master.csv")
OWNER_DIRECTORY_FILE = os.path.join(PROCESSED_DATA_PATH, "cleaned_owner_directory.csv")
APPROVAL_HISTORY_FILE = os.path.join(PROCESSED_DATA_PATH, "cleaned_approval_history.csv")

AUDIT_RESULTS_FILE = os.path.join(PROCESSED_DATA_PATH, "audit_results.csv")

# Fixed date for reproducible portfolio results
REFERENCE_DATE = pd.Timestamp(datetime(2026, 7, 6))


DATE_COLUMNS_DOCUMENT_MASTER = [
    "effective_date",
    "expiration_date",
    "last_review_date",
    "next_review_date",
    "created_date",
    "updated_date",
]

DATE_COLUMNS_APPROVAL_HISTORY = [
    "approval_date",
]


RULES = {
    "DQ-001": {
        "rule_name": "Active Document Is Expired",
        "severity": "Critical",
        "issue_description": "Document is marked as active but the expiration date has already passed.",
        "recommended_action": "Renew the document, update the expiration date, or change the document status.",
        "target_resolution_days": 7,
    },
    "DQ-002": {
        "rule_name": "Missing Document Owner",
        "severity": "High",
        "issue_description": "Document does not have an assigned owner.",
        "recommended_action": "Assign an active document owner.",
        "target_resolution_days": 10,
    },
    "DQ-003": {
        "rule_name": "Inactive Owner Assigned",
        "severity": "High",
        "issue_description": "Document is assigned to an inactive owner.",
        "recommended_action": "Reassign the document to an active owner.",
        "target_resolution_days": 10,
    },
    "DQ-004": {
        "rule_name": "Active Document Missing Approval",
        "severity": "Critical",
        "issue_description": "Active document does not have a valid approval status.",
        "recommended_action": "Route the document for approval or update the approval record.",
        "target_resolution_days": 7,
    },
    "DQ-005": {
        "rule_name": "Confidential Document Missing Approval",
        "severity": "Critical",
        "issue_description": "Confidential or restricted document does not have formal approval.",
        "recommended_action": "Obtain formal approval for the document.",
        "target_resolution_days": 7,
    },
    "DQ-006": {
        "rule_name": "Invalid Date Sequence",
        "severity": "Critical",
        "issue_description": "Expiration date is earlier than the effective date.",
        "recommended_action": "Correct the effective date or expiration date.",
        "target_resolution_days": 7,
    },
    "DQ-007": {
        "rule_name": "Missing Next Review Date",
        "severity": "Medium",
        "issue_description": "Document does not have a scheduled next review date.",
        "recommended_action": "Define the next review date based on the document control policy.",
        "target_resolution_days": 20,
    },
    "DQ-008": {
        "rule_name": "Review Overdue",
        "severity": "Medium",
        "issue_description": "Active document is overdue for review.",
        "recommended_action": "Complete the document review and update the review cycle.",
        "target_resolution_days": 15,
    },
    "DQ-009": {
        "rule_name": "Missing Version",
        "severity": "Medium",
        "issue_description": "Document version is missing.",
        "recommended_action": "Update the document version or revision number.",
        "target_resolution_days": 20,
    },
    "DQ-010": {
        "rule_name": "Missing File Reference",
        "severity": "Medium",
        "issue_description": "Document does not have a file reference or SAP document link.",
        "recommended_action": "Add the correct file path, SAP document reference, or document storage location.",
        "target_resolution_days": 20,
    },
    "DQ-011": {
        "rule_name": "Draft Document Open Too Long",
        "severity": "Medium",
        "issue_description": "Draft document has remained open for more than 60 days.",
        "recommended_action": "Approve, reject, complete, or cancel the draft document.",
        "target_resolution_days": 20,
    },
    "DQ-012": {
        "rule_name": "Missing Business Area",
        "severity": "Low",
        "issue_description": "Document does not have a business area assigned.",
        "recommended_action": "Assign the correct business area.",
        "target_resolution_days": 30,
    },
    "DQ-013": {
        "rule_name": "Missing Plant",
        "severity": "Low",
        "issue_description": "Document does not have a plant or operating location assigned.",
        "recommended_action": "Assign the correct plant or operating location.",
        "target_resolution_days": 30,
    },
    "DQ-014": {
        "rule_name": "Invalid Approval History",
        "severity": "High",
        "issue_description": "Document is marked as approved, but no approval record exists in the approval history file.",
        "recommended_action": "Add the missing approval history record or correct the approval status.",
        "target_resolution_days": 10,
    },
}


def load_clean_data():
    """Load cleaned datasets."""

    document_df = pd.read_csv(DOCUMENT_MASTER_FILE)
    owner_df = pd.read_csv(OWNER_DIRECTORY_FILE)
    approval_df = pd.read_csv(APPROVAL_HISTORY_FILE)

    for column in DATE_COLUMNS_DOCUMENT_MASTER:
        document_df[column] = pd.to_datetime(document_df[column], errors="coerce")

    for column in DATE_COLUMNS_APPROVAL_HISTORY:
        approval_df[column] = pd.to_datetime(approval_df[column], errors="coerce")

    owner_df["active_flag"] = owner_df["active_flag"].astype(str).str.lower().map(
        {
            "true": True,
            "false": False,
            "1": True,
            "0": False,
            "yes": True,
            "no": False,
        }
    )

    print("Clean data loaded successfully.")
    print(f"Document master records: {len(document_df)}")
    print(f"Owner directory records: {len(owner_df)}")
    print(f"Approval history records: {len(approval_df)}")

    return document_df, owner_df, approval_df


def is_blank(value):
    """Return True when a value should be treated as blank."""

    if pd.isna(value):
        return True

    if str(value).strip() == "":
        return True

    return False


def add_issue(audit_results, audit_counter, row, rule_id):
    """Append one audit issue to the audit results list."""

    rule = RULES[rule_id]

    audit_results.append({
        "audit_id": f"AUD-{audit_counter:06d}",
        "document_id": row.get("document_id"),
        "document_title": row.get("document_title"),
        "document_type": row.get("document_type"),
        "business_area": row.get("business_area"),
        "plant": row.get("plant"),
        "owner_id": row.get("owner_id"),
        "status": row.get("status"),
        "rule_id": rule_id,
        "rule_name": rule["rule_name"],
        "severity": rule["severity"],
        "issue_detected": True,
        "issue_description": rule["issue_description"],
        "recommended_action": rule["recommended_action"],
        "target_resolution_days": rule["target_resolution_days"],
    })

    return audit_counter + 1


def run_audit_rules(document_df, owner_df, approval_df):
    """Run all documented data quality audit rules."""

    audit_results = []
    audit_counter = 1

    owner_lookup = owner_df[["owner_id", "active_flag"]].drop_duplicates()

    document_df = document_df.merge(
        owner_lookup,
        how="left",
        on="owner_id"
    )

    approved_history_docs = set(
        approval_df.loc[
            approval_df["approval_result"] == "Approved",
            "document_id"
        ].dropna()
    )

    for _, row in document_df.iterrows():
        status = row.get("status")
        owner_id = row.get("owner_id")
        active_flag = row.get("active_flag")
        approval_status = row.get("approval_status")
        confidentiality_level = row.get("confidentiality_level")

        effective_date = row.get("effective_date")
        expiration_date = row.get("expiration_date")
        next_review_date = row.get("next_review_date")
        created_date = row.get("created_date")

        # DQ-001: Active Document Is Expired
        if (
            status == "Active"
            and pd.notna(expiration_date)
            and expiration_date < REFERENCE_DATE
        ):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-001")

        # DQ-002: Missing Document Owner
        if is_blank(owner_id):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-002")

        # DQ-003: Inactive Owner Assigned
        if not is_blank(owner_id) and active_flag is False:
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-003")

        # DQ-004: Active Document Missing Approval
        if (
            status == "Active"
            and (
                is_blank(approval_status)
                or approval_status in ["Missing", "Pending"]
            )
        ):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-004")

        # DQ-005: Confidential Document Missing Approval
        if (
            confidentiality_level in ["Confidential", "Restricted"]
            and approval_status != "Approved"
        ):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-005")

        # DQ-006: Invalid Date Sequence
        if (
            pd.notna(expiration_date)
            and pd.notna(effective_date)
            and expiration_date < effective_date
        ):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-006")

        # DQ-007: Missing Next Review Date
        if pd.isna(next_review_date):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-007")

        # DQ-008: Review Overdue
        if (
            status == "Active"
            and pd.notna(next_review_date)
            and next_review_date < REFERENCE_DATE
        ):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-008")

        # DQ-009: Missing Version
        if is_blank(row.get("version")):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-009")

        # DQ-010: Missing File Reference
        if is_blank(row.get("file_reference")):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-010")

        # DQ-011: Draft Document Open Too Long
        if (
            status == "Draft"
            and pd.notna(created_date)
            and created_date < REFERENCE_DATE - timedelta(days=60)
        ):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-011")

        # DQ-012: Missing Business Area
        if is_blank(row.get("business_area")):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-012")

        # DQ-013: Missing Plant
        if is_blank(row.get("plant")):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-013")

        # DQ-014: Invalid Approval History
        if (
            approval_status == "Approved"
            and row.get("document_id") not in approved_history_docs
        ):
            audit_counter = add_issue(audit_results, audit_counter, row, "DQ-014")

    audit_df = pd.DataFrame(audit_results)

    return audit_df


def save_audit_results(audit_df):
    """Save audit results to processed folder."""

    audit_df.to_csv(AUDIT_RESULTS_FILE, index=False)

    print("\nAudit results created successfully:")
    print(f"- {AUDIT_RESULTS_FILE}")


def print_audit_summary(audit_df):
    """Print audit result summary."""

    print("\nAudit Summary")
    print("-------------")
    print(f"Total issues detected: {len(audit_df)}")

    if len(audit_df) == 0:
        print("No audit issues detected.")
        return

    print("\nIssues by severity:")
    print(audit_df["severity"].value_counts())

    print("\nTop 10 rules by number of issues:")
    print(audit_df["rule_name"].value_counts().head(10))


def main():
    document_df, owner_df, approval_df = load_clean_data()

    audit_df = run_audit_rules(document_df, owner_df, approval_df)

    save_audit_results(audit_df)
    print_audit_summary(audit_df)


if __name__ == "__main__":
    main()
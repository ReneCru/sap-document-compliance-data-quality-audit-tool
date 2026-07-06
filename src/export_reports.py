import os

import pandas as pd


PROCESSED_DATA_PATH = "data/processed"
REPORTS_PATH = "reports"

DOCUMENT_MASTER_FILE = os.path.join(PROCESSED_DATA_PATH, "cleaned_document_master.csv")
AUDIT_RESULTS_FILE = os.path.join(PROCESSED_DATA_PATH, "audit_results.csv")
QUALITY_SCORES_FILE = os.path.join(PROCESSED_DATA_PATH, "document_quality_scores.csv")

EXECUTIVE_SUMMARY_FILE = os.path.join(REPORTS_PATH, "executive_summary.csv")
EXCEPTION_REPORT_FILE = os.path.join(REPORTS_PATH, "exception_report.csv")
REMEDIATION_BACKLOG_FILE = os.path.join(REPORTS_PATH, "remediation_backlog.csv")


SEVERITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}

RISK_ORDER = {
    "Critical Risk": 1,
    "High Risk": 2,
    "Medium Risk": 3,
    "Low Risk": 4,
    "Healthy": 5,
}


def create_reports_folder():
    """Create reports folder if it does not exist."""
    os.makedirs(REPORTS_PATH, exist_ok=True)


def load_data():
    """Load processed datasets required for reporting."""

    document_df = pd.read_csv(DOCUMENT_MASTER_FILE)
    audit_df = pd.read_csv(AUDIT_RESULTS_FILE)
    score_df = pd.read_csv(QUALITY_SCORES_FILE)

    print("Processed data loaded successfully.")
    print(f"Document master records: {len(document_df)}")
    print(f"Audit issue records: {len(audit_df)}")
    print(f"Document score records: {len(score_df)}")

    return document_df, audit_df, score_df


def create_executive_summary(document_df, audit_df, score_df):
    """Create executive-level summary KPIs."""

    total_documents = len(document_df)
    total_issues = len(audit_df)

    average_score = round(score_df["data_quality_score"].mean(), 2)

    critical_issues = len(audit_df[audit_df["severity"] == "Critical"])
    high_issues = len(audit_df[audit_df["severity"] == "High"])
    medium_issues = len(audit_df[audit_df["severity"] == "Medium"])
    low_issues = len(audit_df[audit_df["severity"] == "Low"])

    critical_risk_documents = len(score_df[score_df["risk_category"] == "Critical Risk"])
    high_risk_documents = len(score_df[score_df["risk_category"] == "High Risk"])
    medium_risk_documents = len(score_df[score_df["risk_category"] == "Medium Risk"])
    low_risk_documents = len(score_df[score_df["risk_category"] == "Low Risk"])
    healthy_documents = len(score_df[score_df["risk_category"] == "Healthy"])

    expired_active_documents = len(
        audit_df[audit_df["rule_id"] == "DQ-001"]["document_id"].unique()
    )

    missing_approval_documents = len(
        audit_df[
            audit_df["rule_id"].isin(["DQ-004", "DQ-005", "DQ-014"])
        ]["document_id"].unique()
    )

    missing_owner_documents = len(
        audit_df[audit_df["rule_id"] == "DQ-002"]["document_id"].unique()
    )

    inactive_owner_documents = len(
        audit_df[audit_df["rule_id"] == "DQ-003"]["document_id"].unique()
    )

    summary_data = [
        {"metric": "Total Documents Audited", "value": total_documents},
        {"metric": "Total Issues Detected", "value": total_issues},
        {"metric": "Average Data Quality Score", "value": average_score},
        {"metric": "Critical Issues", "value": critical_issues},
        {"metric": "High Issues", "value": high_issues},
        {"metric": "Medium Issues", "value": medium_issues},
        {"metric": "Low Issues", "value": low_issues},
        {"metric": "Critical Risk Documents", "value": critical_risk_documents},
        {"metric": "High Risk Documents", "value": high_risk_documents},
        {"metric": "Medium Risk Documents", "value": medium_risk_documents},
        {"metric": "Low Risk Documents", "value": low_risk_documents},
        {"metric": "Healthy Documents", "value": healthy_documents},
        {"metric": "Expired Active Documents", "value": expired_active_documents},
        {"metric": "Missing Approval Documents", "value": missing_approval_documents},
        {"metric": "Missing Owner Documents", "value": missing_owner_documents},
        {"metric": "Inactive Owner Documents", "value": inactive_owner_documents},
    ]

    executive_summary_df = pd.DataFrame(summary_data)

    return executive_summary_df


def create_exception_report(audit_df, score_df):
    """Create detailed exception report combining audit issues with quality scores."""

    exception_df = audit_df.merge(
        score_df[
            [
                "document_id",
                "data_quality_score",
                "risk_category",
                "total_issues",
                "critical_issues",
                "high_issues",
                "medium_issues",
                "low_issues",
            ]
        ],
        how="left",
        on="document_id",
    )

    exception_df["severity_rank"] = exception_df["severity"].map(SEVERITY_ORDER)
    exception_df["risk_rank"] = exception_df["risk_category"].map(RISK_ORDER)

    exception_df = exception_df.sort_values(
        by=[
            "severity_rank",
            "risk_rank",
            "data_quality_score",
            "document_id",
            "rule_id",
        ],
        ascending=[True, True, True, True, True],
    )

    exception_df = exception_df.drop(columns=["severity_rank", "risk_rank"])

    return exception_df


def create_remediation_backlog(exception_df):
    """Create prioritized remediation backlog from exception report."""

    backlog_columns = [
        "severity",
        "document_id",
        "document_title",
        "document_type",
        "business_area",
        "plant",
        "owner_id",
        "status",
        "rule_id",
        "rule_name",
        "issue_description",
        "recommended_action",
        "target_resolution_days",
        "data_quality_score",
        "risk_category",
    ]

    backlog_df = exception_df[backlog_columns].copy()

    backlog_df = backlog_df.rename(
        columns={
            "severity": "priority",
        }
    )

    backlog_df["priority_rank"] = backlog_df["priority"].map(SEVERITY_ORDER)
    backlog_df["risk_rank"] = backlog_df["risk_category"].map(RISK_ORDER)

    backlog_df = backlog_df.sort_values(
        by=[
            "priority_rank",
            "risk_rank",
            "target_resolution_days",
            "data_quality_score",
            "document_id",
        ],
        ascending=[True, True, True, True, True],
    )

    backlog_df = backlog_df.drop(columns=["priority_rank", "risk_rank"])

    return backlog_df


def save_reports(executive_summary_df, exception_df, remediation_backlog_df):
    """Save final reports as CSV files."""

    executive_summary_df.to_csv(EXECUTIVE_SUMMARY_FILE, index=False)
    exception_df.to_csv(EXCEPTION_REPORT_FILE, index=False)
    remediation_backlog_df.to_csv(REMEDIATION_BACKLOG_FILE, index=False)

    print("\nReports created successfully:")
    print(f"- {EXECUTIVE_SUMMARY_FILE}")
    print(f"- {EXCEPTION_REPORT_FILE}")
    print(f"- {REMEDIATION_BACKLOG_FILE}")


def print_report_summary(executive_summary_df, exception_df, remediation_backlog_df):
    """Print summary of generated reports."""

    print("\nExecutive Summary")
    print("-----------------")
    print(executive_summary_df)

    print("\nException Report")
    print("----------------")
    print(f"Total exception records: {len(exception_df)}")

    print("\nRemediation Backlog")
    print("-------------------")
    print(f"Total remediation actions: {len(remediation_backlog_df)}")

    print("\nTop 10 remediation actions:")
    print(
        remediation_backlog_df[
            [
                "priority",
                "document_id",
                "rule_id",
                "rule_name",
                "target_resolution_days",
                "data_quality_score",
                "risk_category",
            ]
        ].head(10)
    )


def main():
    create_reports_folder()

    document_df, audit_df, score_df = load_data()

    executive_summary_df = create_executive_summary(document_df, audit_df, score_df)

    exception_df = create_exception_report(audit_df, score_df)

    remediation_backlog_df = create_remediation_backlog(exception_df)

    save_reports(executive_summary_df, exception_df, remediation_backlog_df)

    print_report_summary(executive_summary_df, exception_df, remediation_backlog_df)


if __name__ == "__main__":
    main()
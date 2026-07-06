import os

import pandas as pd


PROCESSED_DATA_PATH = "data/processed"

DOCUMENT_MASTER_FILE = os.path.join(PROCESSED_DATA_PATH, "cleaned_document_master.csv")
AUDIT_RESULTS_FILE = os.path.join(PROCESSED_DATA_PATH, "audit_results.csv")
QUALITY_SCORES_FILE = os.path.join(PROCESSED_DATA_PATH, "document_quality_scores.csv")


SEVERITY_PENALTIES = {
    "Critical": 30,
    "High": 20,
    "Medium": 10,
    "Low": 5,
}


def load_data():
    """Load cleaned document master data and audit results."""

    document_df = pd.read_csv(DOCUMENT_MASTER_FILE)

    if os.path.exists(AUDIT_RESULTS_FILE):
        audit_df = pd.read_csv(AUDIT_RESULTS_FILE)
    else:
        raise FileNotFoundError(
            f"{AUDIT_RESULTS_FILE} not found. Run src/run_quality_audit.py first."
        )

    print("Data loaded successfully.")
    print(f"Document master records: {len(document_df)}")
    print(f"Audit issues records: {len(audit_df)}")

    return document_df, audit_df


def calculate_issue_counts(audit_df):
    """Calculate issue counts by severity for each document."""

    if audit_df.empty:
        return pd.DataFrame(
            columns=[
                "document_id",
                "total_issues",
                "critical_issues",
                "high_issues",
                "medium_issues",
                "low_issues",
                "total_penalty_points",
            ]
        )

    audit_df["penalty_points"] = audit_df["severity"].map(SEVERITY_PENALTIES).fillna(0)

    issue_counts = audit_df.groupby("document_id").agg(
        total_issues=("audit_id", "count"),
        critical_issues=("severity", lambda x: (x == "Critical").sum()),
        high_issues=("severity", lambda x: (x == "High").sum()),
        medium_issues=("severity", lambda x: (x == "Medium").sum()),
        low_issues=("severity", lambda x: (x == "Low").sum()),
        total_penalty_points=("penalty_points", "sum"),
    ).reset_index()

    return issue_counts


def assign_risk_category(score):
    """Assign risk category based on data quality score."""

    if score >= 90:
        return "Healthy"
    if score >= 75:
        return "Low Risk"
    if score >= 60:
        return "Medium Risk"
    if score >= 40:
        return "High Risk"

    return "Critical Risk"


def calculate_quality_scores(document_df, issue_counts):
    """Calculate final data quality score and risk category."""

    score_df = document_df[
        [
            "document_id",
            "document_title",
            "document_type",
            "business_area",
            "plant",
            "owner_id",
            "status",
            "approval_status",
            "confidentiality_level",
        ]
    ].copy()

    score_df = score_df.merge(
        issue_counts,
        how="left",
        on="document_id"
    )

    count_columns = [
        "total_issues",
        "critical_issues",
        "high_issues",
        "medium_issues",
        "low_issues",
        "total_penalty_points",
    ]

    for column in count_columns:
        score_df[column] = score_df[column].fillna(0).astype(int)

    score_df["data_quality_score"] = 100 - score_df["total_penalty_points"]

    score_df["data_quality_score"] = score_df["data_quality_score"].clip(lower=0)

    score_df["risk_category"] = score_df["data_quality_score"].apply(
        assign_risk_category
    )

    score_df = score_df.sort_values(
        by=[
            "data_quality_score",
            "critical_issues",
            "high_issues",
            "total_issues",
        ],
        ascending=[True, False, False, False],
    )

    return score_df


def save_quality_scores(score_df):
    """Save quality scores to processed folder."""

    score_df.to_csv(QUALITY_SCORES_FILE, index=False)

    print("\nDocument quality scores created successfully:")
    print(f"- {QUALITY_SCORES_FILE}")


def print_score_summary(score_df):
    """Print score and risk summary."""

    print("\nData Quality Score Summary")
    print("--------------------------")
    print(f"Total documents scored: {len(score_df)}")
    print(f"Average data quality score: {score_df['data_quality_score'].mean():.2f}")
    print(f"Lowest data quality score: {score_df['data_quality_score'].min()}")
    print(f"Highest data quality score: {score_df['data_quality_score'].max()}")

    print("\nDocuments by risk category:")
    print(score_df["risk_category"].value_counts())

    print("\nTop 10 highest risk documents:")
    print(
        score_df[
            [
                "document_id",
                "document_type",
                "business_area",
                "status",
                "total_issues",
                "critical_issues",
                "high_issues",
                "data_quality_score",
                "risk_category",
            ]
        ].head(10)
    )


def main():
    document_df, audit_df = load_data()

    issue_counts = calculate_issue_counts(audit_df)

    score_df = calculate_quality_scores(document_df, issue_counts)

    save_quality_scores(score_df)

    print_score_summary(score_df)


if __name__ == "__main__":
    main()
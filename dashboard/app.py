import os

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PROCESSED_DATA_PATH = os.path.join(ROOT_DIR, "data", "processed")
REPORTS_PATH = os.path.join(ROOT_DIR, "reports")

EXECUTIVE_SUMMARY_FILE = os.path.join(REPORTS_PATH, "executive_summary.csv")
EXCEPTION_REPORT_FILE = os.path.join(REPORTS_PATH, "exception_report.csv")
REMEDIATION_BACKLOG_FILE = os.path.join(REPORTS_PATH, "remediation_backlog.csv")
QUALITY_SCORES_FILE = os.path.join(PROCESSED_DATA_PATH, "document_quality_scores.csv")
AUDIT_RESULTS_FILE = os.path.join(PROCESSED_DATA_PATH, "audit_results.csv")


st.set_page_config(
    page_title="SAP Document Compliance Data Quality Audit",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data():
    """Load dashboard datasets."""

    required_files = [
        EXECUTIVE_SUMMARY_FILE,
        EXCEPTION_REPORT_FILE,
        REMEDIATION_BACKLOG_FILE,
        QUALITY_SCORES_FILE,
        AUDIT_RESULTS_FILE,
    ]

    missing_files = [file for file in required_files if not os.path.exists(file)]

    if missing_files:
        return None, None, None, None, None, missing_files

    executive_summary_df = pd.read_csv(EXECUTIVE_SUMMARY_FILE)
    exception_df = pd.read_csv(EXCEPTION_REPORT_FILE)
    remediation_df = pd.read_csv(REMEDIATION_BACKLOG_FILE)
    score_df = pd.read_csv(QUALITY_SCORES_FILE)
    audit_df = pd.read_csv(AUDIT_RESULTS_FILE)

    return (
        executive_summary_df,
        exception_df,
        remediation_df,
        score_df,
        audit_df,
        [],
    )


def get_metric(executive_summary_df, metric_name):
    """Get one metric value from the executive summary table."""

    metric_row = executive_summary_df[
        executive_summary_df["metric"] == metric_name
    ]

    if metric_row.empty:
        return 0

    return metric_row["value"].iloc[0]


def filter_data(score_df, audit_df, exception_df, remediation_df):
    """Apply sidebar filters."""

    st.sidebar.header("Filters")

    business_areas = sorted(score_df["business_area"].dropna().unique().tolist())
    document_types = sorted(score_df["document_type"].dropna().unique().tolist())
    risk_categories = sorted(score_df["risk_category"].dropna().unique().tolist())

    selected_business_area = st.sidebar.selectbox(
        "Business Area",
        ["All"] + business_areas,
    )

    selected_document_type = st.sidebar.selectbox(
        "Document Type",
        ["All"] + document_types,
    )

    selected_risk_category = st.sidebar.selectbox(
        "Risk Category",
        ["All"] + risk_categories,
    )

    filtered_score_df = score_df.copy()
    filtered_audit_df = audit_df.copy()
    filtered_exception_df = exception_df.copy()
    filtered_remediation_df = remediation_df.copy()

    if selected_business_area != "All":
        filtered_score_df = filtered_score_df[
            filtered_score_df["business_area"] == selected_business_area
        ]
        filtered_audit_df = filtered_audit_df[
            filtered_audit_df["business_area"] == selected_business_area
        ]
        filtered_exception_df = filtered_exception_df[
            filtered_exception_df["business_area"] == selected_business_area
        ]
        filtered_remediation_df = filtered_remediation_df[
            filtered_remediation_df["business_area"] == selected_business_area
        ]

    if selected_document_type != "All":
        filtered_score_df = filtered_score_df[
            filtered_score_df["document_type"] == selected_document_type
        ]
        filtered_audit_df = filtered_audit_df[
            filtered_audit_df["document_type"] == selected_document_type
        ]
        filtered_exception_df = filtered_exception_df[
            filtered_exception_df["document_type"] == selected_document_type
        ]
        filtered_remediation_df = filtered_remediation_df[
            filtered_remediation_df["document_type"] == selected_document_type
        ]

    if selected_risk_category != "All":
        filtered_score_df = filtered_score_df[
            filtered_score_df["risk_category"] == selected_risk_category
        ]
        filtered_exception_df = filtered_exception_df[
            filtered_exception_df["risk_category"] == selected_risk_category
        ]
        filtered_remediation_df = filtered_remediation_df[
            filtered_remediation_df["risk_category"] == selected_risk_category
        ]

        valid_document_ids = filtered_score_df["document_id"].unique()
        filtered_audit_df = filtered_audit_df[
            filtered_audit_df["document_id"].isin(valid_document_ids)
        ]

    return (
        filtered_score_df,
        filtered_audit_df,
        filtered_exception_df,
        filtered_remediation_df,
    )


def display_header():
    """Display dashboard title and description."""

    st.title("SAP Document & Compliance Master Data Quality Audit Tool")

    st.markdown(
        """
        This dashboard summarizes data quality issues detected in synthetic SAP-like
        document and compliance master data.

        The audit focuses on document ownership, approvals, expiration dates,
        review cycles, file references, and risk-based remediation priorities.
        """
    )

    st.info(
        "This project uses synthetic data only. It does not use vendor master, "
        "material master, real SAP data, or confidential company information."
    )


def display_kpis(executive_summary_df, score_df, audit_df):
    """Display executive KPI cards."""

    total_documents = len(score_df)
    total_issues = len(audit_df)

    average_score = round(score_df["data_quality_score"].mean(), 2) if total_documents > 0 else 0

    critical_issues = len(audit_df[audit_df["severity"] == "Critical"])
    high_issues = len(audit_df[audit_df["severity"] == "High"])
    high_risk_documents = len(score_df[score_df["risk_category"] == "High Risk"])
    critical_risk_documents = len(score_df[score_df["risk_category"] == "Critical Risk"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Documents Audited", total_documents)
    col2.metric("Total Issues", total_issues)
    col3.metric("Average Quality Score", average_score)
    col4.metric("Critical Issues", critical_issues)

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("High Issues", high_issues)
    col6.metric("Critical Risk Documents", critical_risk_documents)
    col7.metric("High Risk Documents", high_risk_documents)
    col8.metric(
        "Expired Active Documents",
        get_metric(executive_summary_df, "Expired Active Documents"),
    )


def display_charts(score_df, audit_df):
    """Display dashboard charts."""

    st.subheader("Risk and Issue Overview")

    col1, col2 = st.columns(2)

    with col1:
        risk_counts = (
            score_df["risk_category"]
            .value_counts()
            .reset_index()
        )
        risk_counts.columns = ["risk_category", "documents"]

        fig_risk = px.bar(
            risk_counts,
            x="risk_category",
            y="documents",
            title="Documents by Risk Category",
            text="documents",
        )

        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        severity_counts = (
            audit_df["severity"]
            .value_counts()
            .reset_index()
        )
        severity_counts.columns = ["severity", "issues"]

        fig_severity = px.bar(
            severity_counts,
            x="severity",
            y="issues",
            title="Issues by Severity",
            text="issues",
        )

        st.plotly_chart(fig_severity, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        issues_by_rule = (
            audit_df.groupby(["rule_id", "rule_name"])
            .size()
            .reset_index(name="issues")
            .sort_values("issues", ascending=False)
            .head(10)
        )

        issues_by_rule["rule_label"] = (
            issues_by_rule["rule_id"] + " - " + issues_by_rule["rule_name"]
        )

        fig_rules = px.bar(
            issues_by_rule,
            x="issues",
            y="rule_label",
            orientation="h",
            title="Top 10 Audit Rules by Issue Count",
            text="issues",
        )

        st.plotly_chart(fig_rules, use_container_width=True)

    with col4:
        score_by_area = (
            score_df.groupby("business_area", dropna=False)
            .agg(
                average_score=("data_quality_score", "mean"),
                documents=("document_id", "count"),
            )
            .reset_index()
            .sort_values("average_score", ascending=True)
        )

        score_by_area["average_score"] = score_by_area["average_score"].round(2)

        fig_area = px.bar(
            score_by_area,
            x="average_score",
            y="business_area",
            orientation="h",
            title="Average Data Quality Score by Business Area",
            text="average_score",
        )

        st.plotly_chart(fig_area, use_container_width=True)


def display_tables(score_df, exception_df, remediation_df):
    """Display detailed tables."""

    st.subheader("Highest Risk Documents")

    highest_risk_columns = [
        "document_id",
        "document_title",
        "document_type",
        "business_area",
        "status",
        "total_issues",
        "critical_issues",
        "high_issues",
        "data_quality_score",
        "risk_category",
    ]

    highest_risk_df = score_df[highest_risk_columns].sort_values(
        by=[
            "data_quality_score",
            "critical_issues",
            "high_issues",
            "total_issues",
        ],
        ascending=[True, False, False, False],
    )

    st.dataframe(highest_risk_df.head(25), use_container_width=True)

    st.subheader("Remediation Backlog")

    remediation_columns = [
        "priority",
        "document_id",
        "document_title",
        "business_area",
        "owner_id",
        "rule_id",
        "rule_name",
        "recommended_action",
        "target_resolution_days",
        "data_quality_score",
        "risk_category",
    ]

    st.dataframe(
        remediation_df[remediation_columns].head(50),
        use_container_width=True,
    )

    st.subheader("Exception Report")

    exception_columns = [
        "document_id",
        "document_title",
        "business_area",
        "status",
        "rule_id",
        "rule_name",
        "severity",
        "issue_description",
        "recommended_action",
        "data_quality_score",
        "risk_category",
    ]

    st.dataframe(
        exception_df[exception_columns].head(100),
        use_container_width=True,
    )


def main():
    (
        executive_summary_df,
        exception_df,
        remediation_df,
        score_df,
        audit_df,
        missing_files,
    ) = load_data()

    display_header()

    if missing_files:
        st.error("Required files are missing. Run the full pipeline first:")
        st.code("python main.py")

        st.write("Missing files:")
        for file in missing_files:
            st.write(f"- {file}")

        return

    (
        filtered_score_df,
        filtered_audit_df,
        filtered_exception_df,
        filtered_remediation_df,
    ) = filter_data(score_df, audit_df, exception_df, remediation_df)

    display_kpis(executive_summary_df, filtered_score_df, filtered_audit_df)

    display_charts(filtered_score_df, filtered_audit_df)

    display_tables(
        filtered_score_df,
        filtered_exception_df,
        filtered_remediation_df,
    )


if __name__ == "__main__":
    main()
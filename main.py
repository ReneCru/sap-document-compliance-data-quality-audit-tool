import subprocess
import sys


PIPELINE_STEPS = [
    {
        "name": "Generate synthetic SAP-like datasets",
        "command": ["python", "src/generate_sample_data.py"],
    },
    {
        "name": "Clean and standardize raw data",
        "command": ["python", "src/clean_data.py"],
    },
    {
        "name": "Run data quality audit rules",
        "command": ["python", "src/run_quality_audit.py"],
    },
    {
        "name": "Calculate document quality scores",
        "command": ["python", "src/calculate_scores.py"],
    },
    {
        "name": "Export executive reports and remediation backlog",
        "command": ["python", "src/export_reports.py"],
    },
]


def run_step(step_number, step):
    """Run one pipeline step."""

    print("\n" + "=" * 80)
    print(f"Step {step_number}: {step['name']}")
    print("=" * 80)

    result = subprocess.run(step["command"], check=False)

    if result.returncode != 0:
        print(f"\nPipeline failed during step {step_number}: {step['name']}")
        sys.exit(result.returncode)

    print(f"\nStep {step_number} completed successfully.")


def main():
    """Run the complete SAP document compliance data quality audit pipeline."""

    print("\nSAP Document & Compliance Master Data Quality Audit Tool")
    print("Starting full audit pipeline...")

    for index, step in enumerate(PIPELINE_STEPS, start=1):
        run_step(index, step)

    print("\n" + "=" * 80)
    print("Pipeline completed successfully.")
    print("=" * 80)

    print("\nGenerated outputs:")
    print("- data/raw/sap_document_master.csv")
    print("- data/raw/owner_directory.csv")
    print("- data/raw/approval_history.csv")
    print("- data/processed/cleaned_document_master.csv")
    print("- data/processed/cleaned_owner_directory.csv")
    print("- data/processed/cleaned_approval_history.csv")
    print("- data/processed/audit_results.csv")
    print("- data/processed/document_quality_scores.csv")
    print("- reports/executive_summary.csv")
    print("- reports/exception_report.csv")
    print("- reports/remediation_backlog.csv")


if __name__ == "__main__":
    main()
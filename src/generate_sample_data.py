import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# Fixed reference date for reproducible portfolio results
REFERENCE_DATE = datetime(2026, 7, 6)

RAW_DATA_PATH = "data/raw"

random.seed(42)
np.random.seed(42)


def create_output_folder():
    """Create raw data folder if it does not exist."""
    os.makedirs(RAW_DATA_PATH, exist_ok=True)


def random_date(start_date, end_date):
    """Generate a random date between two dates."""
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)


def generate_owner_directory(number_of_owners=50):
    """Generate synthetic document owner directory."""

    first_names = [
        "Maria", "John", "Laura", "Carlos", "Sofia", "Daniel", "Ana",
        "Michael", "Luis", "Jessica", "David", "Patricia", "Robert",
        "Monica", "Jose", "Andrea", "Fernando", "Gabriela", "Mark", "Diana"
    ]

    last_names = [
        "Lopez", "Smith", "Garcia", "Johnson", "Martinez", "Brown",
        "Rodriguez", "Davis", "Hernandez", "Wilson", "Gonzalez",
        "Anderson", "Perez", "Thomas", "Sanchez", "Moore"
    ]

    departments = [
        "Supply Chain", "Quality", "Engineering", "Operations",
        "Finance", "Compliance", "Program Management"
    ]

    roles = [
        "Compliance Analyst", "Document Control Specialist",
        "Quality Engineer", "Supply Chain Analyst",
        "Operations Manager", "Program Manager",
        "Business Systems Analyst"
    ]

    owners = []

    for i in range(1, number_of_owners + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        owner_name = f"{first_name} {last_name}"
        department = random.choice(departments)

        owners.append({
            "owner_id": f"OWN-{i:03d}",
            "owner_name": owner_name,
            "department": department,
            "role": random.choice(roles),
            "active_flag": random.choices([True, False], weights=[85, 15])[0],
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com"
        })

    return pd.DataFrame(owners)


def generate_document_master(owner_df, number_of_documents=1000):
    """Generate synthetic SAP-like document master data."""

    document_types = [
        "NDA", "Contract", "SOP", "Work Instruction",
        "Quality Record", "Compliance Document"
    ]

    business_areas = [
        "Supply Chain", "Quality", "Engineering", "Operations",
        "Finance", "Compliance", "Program Management"
    ]

    plants = ["CHI-01", "CHI-02", "ELP-01", "MTY-01", "QRO-01"]

    statuses = ["Active", "Expired", "Obsolete", "Draft", "Pending Approval"]

    approval_statuses = ["Approved", "Pending", "Rejected", "Missing"]

    confidentiality_levels = ["Public", "Internal", "Confidential", "Restricted"]

    title_templates = {
        "NDA": "Non-Disclosure Agreement",
        "Contract": "Service Contract Agreement",
        "SOP": "Standard Operating Procedure",
        "Work Instruction": "Operational Work Instruction",
        "Quality Record": "Quality Inspection Record",
        "Compliance Document": "Regulatory Compliance Document"
    }

    documents = []

    owner_ids = owner_df["owner_id"].tolist()

    for i in range(1, number_of_documents + 1):
        document_id = f"DOC-{10000 + i}"
        document_type = random.choice(document_types)
        status = random.choices(
            statuses,
            weights=[55, 15, 10, 10, 10]
        )[0]

        created_date = random_date(
            REFERENCE_DATE - timedelta(days=1200),
            REFERENCE_DATE - timedelta(days=30)
        )

        effective_date = created_date + timedelta(days=random.randint(1, 45))

        expiration_date = effective_date + timedelta(days=random.randint(180, 900))

        last_review_date = effective_date + timedelta(days=random.randint(30, 365))

        next_review_date = last_review_date + timedelta(days=random.randint(180, 365))

        owner_id = random.choice(owner_ids)

        approval_status = random.choices(
            approval_statuses,
            weights=[70, 15, 5, 10]
        )[0]

        confidentiality_level = random.choices(
            confidentiality_levels,
            weights=[10, 45, 30, 15]
        )[0]

        version = f"v{random.randint(1, 5)}.{random.randint(0, 9)}"

        file_reference = f"SAP/DOCS/{document_id}.pdf"

        updated_date = created_date + timedelta(days=random.randint(1, 700))

        document = {
            "document_id": document_id,
            "document_type": document_type,
            "document_title": f"{title_templates[document_type]} - {document_id}",
            "business_area": random.choice(business_areas),
            "plant": random.choice(plants),
            "owner_id": owner_id,
            "status": status,
            "version": version,
            "effective_date": effective_date.date(),
            "expiration_date": expiration_date.date(),
            "last_review_date": last_review_date.date(),
            "next_review_date": next_review_date.date(),
            "approval_status": approval_status,
            "confidentiality_level": confidentiality_level,
            "file_reference": file_reference,
            "created_date": created_date.date(),
            "updated_date": updated_date.date()
        }

        documents.append(document)

    document_df = pd.DataFrame(documents)

    document_df = inject_data_quality_issues(document_df)

    return document_df


def inject_data_quality_issues(document_df):
    """
    Intentionally inject realistic data quality issues into the dataset.
    This makes the audit tool meaningful for portfolio demonstration.
    """

    total_rows = len(document_df)

    # Active documents with expired expiration dates
    expired_active_indices = document_df.sample(frac=0.05, random_state=1).index
    document_df.loc[expired_active_indices, "status"] = "Active"
    document_df.loc[expired_active_indices, "expiration_date"] = (
        REFERENCE_DATE - timedelta(days=random.randint(1, 365))
    ).date()

    # Missing owner_id
    missing_owner_indices = document_df.sample(frac=0.04, random_state=2).index
    document_df.loc[missing_owner_indices, "owner_id"] = np.nan

    # Active documents missing approval
    missing_approval_indices = document_df.sample(frac=0.05, random_state=3).index
    document_df.loc[missing_approval_indices, "status"] = "Active"
    document_df.loc[missing_approval_indices, "approval_status"] = "Missing"

    # Confidential or restricted documents missing approval
    confidential_missing_approval_indices = document_df.sample(frac=0.04, random_state=4).index
    document_df.loc[confidential_missing_approval_indices, "confidentiality_level"] = random.choice(
        ["Confidential", "Restricted"]
    )
    document_df.loc[confidential_missing_approval_indices, "approval_status"] = random.choice(
        ["Missing", "Pending"]
    )

    # Invalid date sequence: expiration before effective date
    invalid_date_indices = document_df.sample(frac=0.03, random_state=5).index
    document_df.loc[invalid_date_indices, "expiration_date"] = (
        pd.to_datetime(document_df.loc[invalid_date_indices, "effective_date"]) - pd.to_timedelta(30, unit="D")
    ).dt.date

    # Missing next review date
    missing_review_indices = document_df.sample(frac=0.05, random_state=6).index
    document_df.loc[missing_review_indices, "next_review_date"] = np.nan

    # Review overdue
    review_overdue_indices = document_df.sample(frac=0.06, random_state=7).index
    document_df.loc[review_overdue_indices, "status"] = "Active"
    document_df.loc[review_overdue_indices, "next_review_date"] = (
        REFERENCE_DATE - timedelta(days=random.randint(1, 300))
    ).date()

    # Missing version
    missing_version_indices = document_df.sample(frac=0.04, random_state=8).index
    document_df.loc[missing_version_indices, "version"] = np.nan

    # Missing file reference
    missing_file_indices = document_df.sample(frac=0.04, random_state=9).index
    document_df.loc[missing_file_indices, "file_reference"] = np.nan

    # Draft documents open too long
    old_draft_indices = document_df.sample(frac=0.03, random_state=10).index
    document_df.loc[old_draft_indices, "status"] = "Draft"
    document_df.loc[old_draft_indices, "created_date"] = (
        REFERENCE_DATE - timedelta(days=random.randint(61, 500))
    ).date()

    # Missing business area
    missing_business_area_indices = document_df.sample(frac=0.03, random_state=11).index
    document_df.loc[missing_business_area_indices, "business_area"] = np.nan

    # Missing plant
    missing_plant_indices = document_df.sample(frac=0.03, random_state=12).index
    document_df.loc[missing_plant_indices, "plant"] = np.nan

    print(f"Generated {total_rows} document records with intentional data quality issues.")

    return document_df


def generate_approval_history(document_df):
    """Generate synthetic approval history records."""

    approvers = [
        "John Smith", "Maria Lopez", "Laura Garcia", "Carlos Martinez",
        "Sofia Johnson", "Daniel Brown", "Ana Rodriguez", "Michael Davis",
        "Patricia Wilson", "Robert Anderson"
    ]

    approval_records = []

    approved_documents = document_df[
        document_df["approval_status"] == "Approved"
    ]["document_id"].tolist()

    # Create approval history for most approved documents, but intentionally leave some missing
    documents_with_history = random.sample(
        approved_documents,
        int(len(approved_documents) * 0.90)
    )

    approval_counter = 1

    for document_id in documents_with_history:
        document_row = document_df[document_df["document_id"] == document_id].iloc[0]

        effective_date = pd.to_datetime(document_row["effective_date"])

        approval_date = effective_date - timedelta(days=random.randint(1, 20))

        approval_records.append({
            "approval_id": f"APR-{50000 + approval_counter}",
            "document_id": document_id,
            "approver_name": random.choice(approvers),
            "approval_date": approval_date.date(),
            "approval_result": "Approved",
            "comments": "Approved for controlled use"
        })

        approval_counter += 1

    # Add some rejected and pending approval records
    non_approved_documents = document_df[
        document_df["approval_status"].isin(["Rejected", "Pending"])
    ]["document_id"].tolist()

    sample_size = min(100, len(non_approved_documents))

    for document_id in random.sample(non_approved_documents, sample_size):
        document_row = document_df[document_df["document_id"] == document_id].iloc[0]
        created_date = pd.to_datetime(document_row["created_date"])

        approval_records.append({
            "approval_id": f"APR-{50000 + approval_counter}",
            "document_id": document_id,
            "approver_name": random.choice(approvers),
            "approval_date": (created_date + timedelta(days=random.randint(1, 30))).date(),
            "approval_result": document_row["approval_status"],
            "comments": f"{document_row['approval_status']} during review cycle"
        })

        approval_counter += 1

    return pd.DataFrame(approval_records)


def save_datasets(document_df, owner_df, approval_df):
    """Save generated datasets as CSV files."""

    document_path = os.path.join(RAW_DATA_PATH, "sap_document_master.csv")
    owner_path = os.path.join(RAW_DATA_PATH, "owner_directory.csv")
    approval_path = os.path.join(RAW_DATA_PATH, "approval_history.csv")

    document_df.to_csv(document_path, index=False)
    owner_df.to_csv(owner_path, index=False)
    approval_df.to_csv(approval_path, index=False)

    print("Synthetic datasets created successfully:")
    print(f"- {document_path}")
    print(f"- {owner_path}")
    print(f"- {approval_path}")


def main():
    create_output_folder()

    owner_df = generate_owner_directory()
    document_df = generate_document_master(owner_df)
    approval_df = generate_approval_history(document_df)

    save_datasets(document_df, owner_df, approval_df)


if __name__ == "__main__":
    main()
import os
import pandas as pd


RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"


DOCUMENT_MASTER_FILE = os.path.join(RAW_DATA_PATH, "sap_document_master.csv")
OWNER_DIRECTORY_FILE = os.path.join(RAW_DATA_PATH, "owner_directory.csv")
APPROVAL_HISTORY_FILE = os.path.join(RAW_DATA_PATH, "approval_history.csv")


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


def create_output_folder():
    """Create processed data folder if it does not exist."""
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)


def load_raw_data():
    """Load raw CSV files."""

    document_df = pd.read_csv(DOCUMENT_MASTER_FILE)
    owner_df = pd.read_csv(OWNER_DIRECTORY_FILE)
    approval_df = pd.read_csv(APPROVAL_HISTORY_FILE)

    print("Raw data loaded successfully.")
    print(f"Document master records: {len(document_df)}")
    print(f"Owner directory records: {len(owner_df)}")
    print(f"Approval history records: {len(approval_df)}")

    return document_df, owner_df, approval_df


def strip_text_fields(df):
    """Trim spaces from all text fields."""

    text_columns = df.select_dtypes(include=["object"]).columns

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    return df


def standardize_missing_values(df):
    """Standardize common missing value patterns."""

    missing_patterns = ["", " ", "nan", "NaN", "None", "NULL", "null", "N/A", "n/a"]

    df = df.replace(missing_patterns, pd.NA)

    return df


def standardize_document_master(document_df):
    """Clean and standardize document master data."""

    document_df = strip_text_fields(document_df)
    document_df = standardize_missing_values(document_df)

    # Standardize document type values
    document_type_map = {
        "NDA": "NDA",
        "Contract": "Contract",
        "SOP": "SOP",
        "Work Instruction": "Work Instruction",
        "Quality Record": "Quality Record",
        "Compliance Document": "Compliance Document",
    }

    document_df["document_type"] = document_df["document_type"].map(document_type_map).fillna(
        document_df["document_type"]
    )

    # Standardize status values
    status_map = {
        "Active": "Active",
        "Expired": "Expired",
        "Obsolete": "Obsolete",
        "Draft": "Draft",
        "Pending Approval": "Pending Approval",
    }

    document_df["status"] = document_df["status"].map(status_map).fillna(
        document_df["status"]
    )

    # Standardize approval status values
    approval_status_map = {
        "Approved": "Approved",
        "Pending": "Pending",
        "Rejected": "Rejected",
        "Missing": "Missing",
    }

    document_df["approval_status"] = document_df["approval_status"].map(
        approval_status_map
    ).fillna(document_df["approval_status"])

    # Standardize confidentiality levels
    confidentiality_map = {
        "Public": "Public",
        "Internal": "Internal",
        "Confidential": "Confidential",
        "Restricted": "Restricted",
    }

    document_df["confidentiality_level"] = document_df["confidentiality_level"].map(
        confidentiality_map
    ).fillna(document_df["confidentiality_level"])

    # Convert date columns
    for column in DATE_COLUMNS_DOCUMENT_MASTER:
        document_df[column] = pd.to_datetime(document_df[column], errors="coerce")

    # Remove duplicate document records if any exist
    document_df = document_df.drop_duplicates(subset=["document_id"], keep="first")

    return document_df


def standardize_owner_directory(owner_df):
    """Clean and standardize owner directory data."""

    owner_df = strip_text_fields(owner_df)
    owner_df = standardize_missing_values(owner_df)

    # Convert active_flag to boolean
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

    owner_df = owner_df.drop_duplicates(subset=["owner_id"], keep="first")

    return owner_df


def standardize_approval_history(approval_df):
    """Clean and standardize approval history data."""

    approval_df = strip_text_fields(approval_df)
    approval_df = standardize_missing_values(approval_df)

    for column in DATE_COLUMNS_APPROVAL_HISTORY:
        approval_df[column] = pd.to_datetime(approval_df[column], errors="coerce")

    # Standardize approval result values
    approval_result_map = {
        "Approved": "Approved",
        "Pending": "Pending",
        "Rejected": "Rejected",
        "Missing": "Missing",
    }

    approval_df["approval_result"] = approval_df["approval_result"].map(
        approval_result_map
    ).fillna(approval_df["approval_result"])

    approval_df = approval_df.drop_duplicates(subset=["approval_id"], keep="first")

    return approval_df


def save_clean_data(document_df, owner_df, approval_df):
    """Save cleaned datasets."""

    document_output_path = os.path.join(
        PROCESSED_DATA_PATH, "cleaned_document_master.csv"
    )
    owner_output_path = os.path.join(
        PROCESSED_DATA_PATH, "cleaned_owner_directory.csv"
    )
    approval_output_path = os.path.join(
        PROCESSED_DATA_PATH, "cleaned_approval_history.csv"
    )

    document_df.to_csv(document_output_path, index=False)
    owner_df.to_csv(owner_output_path, index=False)
    approval_df.to_csv(approval_output_path, index=False)

    print("Cleaned datasets created successfully:")
    print(f"- {document_output_path}")
    print(f"- {owner_output_path}")
    print(f"- {approval_output_path}")


def print_data_quality_summary(document_df, owner_df, approval_df):
    """Print a basic summary after cleaning."""

    print("\nData Quality Summary")
    print("--------------------")
    print(f"Document master records: {len(document_df)}")
    print(f"Owner directory records: {len(owner_df)}")
    print(f"Approval history records: {len(approval_df)}")

    print("\nMissing values in document master:")
    print(document_df.isna().sum())

    print("\nMissing values in owner directory:")
    print(owner_df.isna().sum())

    print("\nMissing values in approval history:")
    print(approval_df.isna().sum())


def main():
    create_output_folder()

    document_df, owner_df, approval_df = load_raw_data()

    document_df = standardize_document_master(document_df)
    owner_df = standardize_owner_directory(owner_df)
    approval_df = standardize_approval_history(approval_df)

    save_clean_data(document_df, owner_df, approval_df)
    print_data_quality_summary(document_df, owner_df, approval_df)


if __name__ == "__main__":
    main()
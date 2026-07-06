# SAP Document & Compliance Master Data Quality Audit Tool

## Overview

This project simulates a SAP-like master data quality audit process focused on document and compliance records.

The tool is designed to identify data quality issues such as expired active documents, missing approvals, inactive owners, invalid dates, missing review cycles, and incomplete document references.

## Business Problem

In regulated industries such as aerospace, manufacturing, and supply chain, poor data quality in document and compliance records can create audit exposure, missed renewals, unclear ownership, obsolete documentation, and delayed corrective actions.

Companies often rely on SAP exports, spreadsheets, and manual reviews to monitor these records. This project demonstrates how that process can be automated using Python, SQL, and a risk-based scoring model.

## Objective

Build an automated data quality audit tool that reviews SAP-like document master data, applies validation rules, calculates a risk score, and generates exception reports and remediation backlogs.

## Scope

This project focuses on document and compliance master data, including:

* NDAs
* Contracts
* Standard Operating Procedures
* Work Instructions
* Quality Records
* Compliance Documents
* Approval Records
* Document Owners
* Expiration Dates
* Review Cycles

## Out of Scope

This project does not include:

* Vendor Master
* Material Master
* Real SAP data
* Confidential company data
* Live SAP system integration

## Tools Used

* Python
* Pandas
* SQL
* PostgreSQL
* Streamlit
* CSV files
* GitHub

## Planned Features

* Synthetic SAP-like dataset generation
* Data cleaning and standardization
* Automated data quality rules
* Risk-based scoring model
* Exception report generation
* Remediation backlog
* Executive dashboard
* SQL quality checks

## Why Synthetic Data?

Real SAP and compliance data cannot be shared publicly due to confidentiality. This project uses synthetic data designed to reflect realistic business issues found in enterprise document control and compliance environments.

## Business Value

This tool helps compliance, supply chain, quality, and operations teams identify risky records before audits, prioritize corrective actions, and improve data governance.

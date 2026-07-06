-- ============================================================
-- SAP Document & Compliance Master Data Quality Audit Tool
-- Script: 01_create_tables.sql
-- Purpose: Create database tables for SAP-like document audit data
-- ============================================================

DROP TABLE IF EXISTS document_quality_scores;
DROP TABLE IF EXISTS audit_results;
DROP TABLE IF EXISTS approval_history;
DROP TABLE IF EXISTS owner_directory;
DROP TABLE IF EXISTS sap_document_master;

CREATE TABLE sap_document_master (
    document_id VARCHAR(20) PRIMARY KEY,
    document_type VARCHAR(50),
    document_title VARCHAR(255),
    business_area VARCHAR(100),
    plant VARCHAR(50),
    owner_id VARCHAR(20),
    status VARCHAR(50),
    version VARCHAR(20),
    effective_date DATE,
    expiration_date DATE,
    last_review_date DATE,
    next_review_date DATE,
    approval_status VARCHAR(50),
    confidentiality_level VARCHAR(50),
    file_reference VARCHAR(255),
    created_date DATE,
    updated_date DATE
);

CREATE TABLE owner_directory (
    owner_id VARCHAR(20) PRIMARY KEY,
    owner_name VARCHAR(150),
    department VARCHAR(100),
    role VARCHAR(100),
    active_flag BOOLEAN,
    email VARCHAR(150)
);

CREATE TABLE approval_history (
    approval_id VARCHAR(20) PRIMARY KEY,
    document_id VARCHAR(20),
    approver_name VARCHAR(150),
    approval_date DATE,
    approval_result VARCHAR(50),
    comments TEXT,
    FOREIGN KEY (document_id) REFERENCES sap_document_master(document_id)
);

CREATE TABLE audit_results (
    audit_id VARCHAR(20) PRIMARY KEY,
    document_id VARCHAR(20),
    document_title VARCHAR(255),
    document_type VARCHAR(50),
    business_area VARCHAR(100),
    plant VARCHAR(50),
    owner_id VARCHAR(20),
    status VARCHAR(50),
    rule_id VARCHAR(20),
    rule_name VARCHAR(150),
    severity VARCHAR(50),
    issue_detected BOOLEAN,
    issue_description TEXT,
    recommended_action TEXT,
    target_resolution_days INTEGER,
    FOREIGN KEY (document_id) REFERENCES sap_document_master(document_id)
);

CREATE TABLE document_quality_scores (
    document_id VARCHAR(20) PRIMARY KEY,
    document_title VARCHAR(255),
    document_type VARCHAR(50),
    business_area VARCHAR(100),
    plant VARCHAR(50),
    owner_id VARCHAR(20),
    status VARCHAR(50),
    approval_status VARCHAR(50),
    confidentiality_level VARCHAR(50),
    total_issues INTEGER,
    critical_issues INTEGER,
    high_issues INTEGER,
    medium_issues INTEGER,
    low_issues INTEGER,
    total_penalty_points INTEGER,
    data_quality_score INTEGER,
    risk_category VARCHAR(50),
    FOREIGN KEY (document_id) REFERENCES sap_document_master(document_id)
);

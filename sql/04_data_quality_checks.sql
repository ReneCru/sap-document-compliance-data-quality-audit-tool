-- ============================================================
-- Script: 04_data_quality_checks.sql
-- Purpose: SQL validation checks matching documented audit rules
-- ============================================================

-- DQ-001: Active Document Is Expired
SELECT
    document_id,
    document_title,
    status,
    expiration_date
FROM sap_document_master
WHERE status = 'Active'
  AND expiration_date < CURRENT_DATE;

-- DQ-002: Missing Document Owner
SELECT
    document_id,
    document_title,
    owner_id
FROM sap_document_master
WHERE owner_id IS NULL
   OR TRIM(owner_id) = '';

-- DQ-003: Inactive Owner Assigned
SELECT
    sdm.document_id,
    sdm.document_title,
    sdm.owner_id,
    od.owner_name,
    od.active_flag
FROM sap_document_master sdm
LEFT JOIN owner_directory od
    ON sdm.owner_id = od.owner_id
WHERE od.active_flag = FALSE;

-- DQ-004: Active Document Missing Approval
SELECT
    document_id,
    document_title,
    status,
    approval_status
FROM sap_document_master
WHERE status = 'Active'
  AND (
      approval_status IS NULL
      OR approval_status IN ('Missing', 'Pending')
  );

-- DQ-005: Confidential Document Missing Approval
SELECT
    document_id,
    document_title,
    confidentiality_level,
    approval_status
FROM sap_document_master
WHERE confidentiality_level IN ('Confidential', 'Restricted')
  AND approval_status <> 'Approved';

-- DQ-006: Invalid Date Sequence
SELECT
    document_id,
    document_title,
    effective_date,
    expiration_date
FROM sap_document_master
WHERE expiration_date < effective_date;

-- DQ-007: Missing Next Review Date
SELECT
    document_id,
    document_title,
    next_review_date
FROM sap_document_master
WHERE next_review_date IS NULL;

-- DQ-008: Review Overdue
SELECT
    document_id,
    document_title,
    status,
    next_review_date
FROM sap_document_master
WHERE status = 'Active'
  AND next_review_date < CURRENT_DATE;

-- DQ-009: Missing Version
SELECT
    document_id,
    document_title,
    version
FROM sap_document_master
WHERE version IS NULL
   OR TRIM(version) = '';

-- DQ-010: Missing File Reference
SELECT
    document_id,
    document_title,
    file_reference
FROM sap_document_master
WHERE file_reference IS NULL
   OR TRIM(file_reference) = '';

-- DQ-011: Draft Document Open Too Long
SELECT
    document_id,
    document_title,
    status,
    created_date
FROM sap_document_master
WHERE status = 'Draft'
  AND created_date < CURRENT_DATE - INTERVAL '60 days';

-- DQ-012: Missing Business Area
SELECT
    document_id,
    document_title,
    business_area
FROM sap_document_master
WHERE business_area IS NULL
   OR TRIM(business_area) = '';

-- DQ-013: Missing Plant
SELECT
    document_id,
    document_title,
    plant
FROM sap_document_master
WHERE plant IS NULL
   OR TRIM(plant) = '';

-- DQ-014: Invalid Approval History
SELECT
    sdm.document_id,
    sdm.document_title,
    sdm.approval_status
FROM sap_document_master sdm
LEFT JOIN approval_history ah
    ON sdm.document_id = ah.document_id
    AND ah.approval_result = 'Approved'
WHERE sdm.approval_status = 'Approved'
  AND ah.document_id IS NULL;

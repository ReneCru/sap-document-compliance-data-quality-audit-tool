-- ============================================================
-- Script: 02_quality_views.sql
-- Purpose: Create SQL views for dashboard and analysis
-- ============================================================

DROP VIEW IF EXISTS vw_issues_by_severity;
DROP VIEW IF EXISTS vw_issues_by_rule;
DROP VIEW IF EXISTS vw_risk_by_business_area;
DROP VIEW IF EXISTS vw_document_quality_overview;
DROP VIEW IF EXISTS vw_high_risk_documents;

CREATE VIEW vw_issues_by_severity AS
SELECT
    severity,
    COUNT(*) AS issue_count
FROM audit_results
GROUP BY severity;

CREATE VIEW vw_issues_by_rule AS
SELECT
    rule_id,
    rule_name,
    severity,
    COUNT(*) AS issue_count
FROM audit_results
GROUP BY rule_id, rule_name, severity
ORDER BY issue_count DESC;

CREATE VIEW vw_risk_by_business_area AS
SELECT
    business_area,
    COUNT(document_id) AS total_documents,
    ROUND(AVG(data_quality_score), 2) AS average_quality_score,
    SUM(CASE WHEN risk_category = 'Critical Risk' THEN 1 ELSE 0 END) AS critical_risk_documents,
    SUM(CASE WHEN risk_category = 'High Risk' THEN 1 ELSE 0 END) AS high_risk_documents,
    SUM(CASE WHEN risk_category = 'Medium Risk' THEN 1 ELSE 0 END) AS medium_risk_documents,
    SUM(CASE WHEN risk_category = 'Low Risk' THEN 1 ELSE 0 END) AS low_risk_documents,
    SUM(CASE WHEN risk_category = 'Healthy' THEN 1 ELSE 0 END) AS healthy_documents
FROM document_quality_scores
GROUP BY business_area
ORDER BY average_quality_score ASC;

CREATE VIEW vw_document_quality_overview AS
SELECT
    dqs.document_id,
    dqs.document_title,
    dqs.document_type,
    dqs.business_area,
    dqs.plant,
    dqs.owner_id,
    od.owner_name,
    od.department AS owner_department,
    od.active_flag AS owner_active_flag,
    dqs.status,
    dqs.approval_status,
    dqs.confidentiality_level,
    dqs.total_issues,
    dqs.critical_issues,
    dqs.high_issues,
    dqs.medium_issues,
    dqs.low_issues,
    dqs.data_quality_score,
    dqs.risk_category
FROM document_quality_scores dqs
LEFT JOIN owner_directory od
    ON dqs.owner_id = od.owner_id;

CREATE VIEW vw_high_risk_documents AS
SELECT
    document_id,
    document_title,
    document_type,
    business_area,
    plant,
    owner_id,
    status,
    total_issues,
    critical_issues,
    high_issues,
    data_quality_score,
    risk_category
FROM document_quality_scores
WHERE risk_category IN ('Critical Risk', 'High Risk')
ORDER BY data_quality_score ASC, critical_issues DESC, high_issues DESC;

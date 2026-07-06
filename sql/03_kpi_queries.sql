-- ============================================================
-- Script: 03_kpi_queries.sql
-- Purpose: Executive KPI queries for SAP-like data quality audit
-- ============================================================

-- Total documents audited
SELECT
    COUNT(*) AS total_documents_audited
FROM sap_document_master;

-- Total issues detected
SELECT
    COUNT(*) AS total_issues_detected
FROM audit_results;

-- Average data quality score
SELECT
    ROUND(AVG(data_quality_score), 2) AS average_data_quality_score
FROM document_quality_scores;

-- Issues by severity
SELECT
    severity,
    COUNT(*) AS issue_count
FROM audit_results
GROUP BY severity
ORDER BY
    CASE severity
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
        ELSE 5
    END;

-- Documents by risk category
SELECT
    risk_category,
    COUNT(*) AS document_count
FROM document_quality_scores
GROUP BY risk_category
ORDER BY
    CASE risk_category
        WHEN 'Critical Risk' THEN 1
        WHEN 'High Risk' THEN 2
        WHEN 'Medium Risk' THEN 3
        WHEN 'Low Risk' THEN 4
        WHEN 'Healthy' THEN 5
        ELSE 6
    END;

-- Top audit rules by issue count
SELECT
    rule_id,
    rule_name,
    severity,
    COUNT(*) AS issue_count
FROM audit_results
GROUP BY rule_id, rule_name, severity
ORDER BY issue_count DESC;

-- Average quality score by business area
SELECT
    business_area,
    COUNT(document_id) AS total_documents,
    ROUND(AVG(data_quality_score), 2) AS average_quality_score
FROM document_quality_scores
GROUP BY business_area
ORDER BY average_quality_score ASC;

-- Highest risk documents
SELECT
    document_id,
    document_title,
    document_type,
    business_area,
    status,
    total_issues,
    critical_issues,
    high_issues,
    data_quality_score,
    risk_category
FROM document_quality_scores
ORDER BY data_quality_score ASC, critical_issues DESC, high_issues DESC
LIMIT 25;

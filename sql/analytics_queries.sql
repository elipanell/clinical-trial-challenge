------------------------------------------------------------
-- Clinical Trial Analytics Queries
-- Dataset excludes withheld records unless otherwise noted.
------------------------------------------------------------


------------------------------------------------------------
-- 1. Number of trials by study type and phase
------------------------------------------------------------

SELECT
    study_type,
    phases,
    COUNT(*) AS total_trials
FROM studies
WHERE is_withheld = FALSE
GROUP BY
    study_type,
    phases
ORDER BY total_trials DESC;


------------------------------------------------------------
-- 2. Most common medical conditions studied
------------------------------------------------------------

SELECT
    conditions,
    COUNT(*) AS total_trials
FROM studies
WHERE
    is_withheld = FALSE
    AND conditions IS NOT NULL
GROUP BY conditions
ORDER BY total_trials DESC
LIMIT 20;


------------------------------------------------------------
-- 3. Interventions with the highest completion rates
------------------------------------------------------------

SELECT
    interventions,
    COUNT(*) AS total_trials,

    SUM(
        CASE
            WHEN overall_status = 'COMPLETED'
            THEN 1
            ELSE 0
        END
    ) AS completed_trials,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN overall_status = 'COMPLETED'
                THEN 1
                ELSE 0
            END
        ) /
        COUNT(*),
        2
    ) AS completion_rate_percent

FROM studies

WHERE
    is_withheld = FALSE
    AND interventions IS NOT NULL

GROUP BY interventions

HAVING COUNT(*) >= 5

ORDER BY completion_rate_percent DESC,
         total_trials DESC;


------------------------------------------------------------
-- 4. Trial status distribution
------------------------------------------------------------

SELECT
    overall_status,
    COUNT(*) AS total_trials
FROM studies
WHERE is_withheld = FALSE
GROUP BY overall_status
ORDER BY total_trials DESC;


------------------------------------------------------------
-- 5. Timeline of study starts
------------------------------------------------------------

SELECT
    DATE_TRUNC('year', start_date) AS study_year,
    COUNT(*) AS total_trials
FROM studies
WHERE
    is_withheld = FALSE
    AND start_date IS NOT NULL
GROUP BY study_year
ORDER BY study_year;


------------------------------------------------------------
-- 6. Top sponsoring organizations
------------------------------------------------------------

SELECT
    organization_full_name,
    COUNT(*) AS total_trials
FROM studies
WHERE
    is_withheld = FALSE
    AND organization_full_name IS NOT NULL
GROUP BY organization_full_name
ORDER BY total_trials DESC
LIMIT 20;


------------------------------------------------------------
-- 7. Responsible party breakdown
------------------------------------------------------------

SELECT
    responsible_party,
    COUNT(*) AS total_trials
FROM studies
WHERE is_withheld = FALSE
GROUP BY responsible_party
ORDER BY total_trials DESC;


------------------------------------------------------------
-- 8. Study type distribution
------------------------------------------------------------

SELECT
    study_type,
    COUNT(*) AS total_trials
FROM studies
WHERE is_withheld = FALSE
GROUP BY study_type
ORDER BY total_trials DESC;


------------------------------------------------------------
-- Notes
------------------------------------------------------------

-- Geographic distribution was requested in the challenge.
-- The selected dataset does not contain structured
-- location/site/country information.
--
-- A production implementation would ingest the locations
-- dataset (or ClinicalTrials.gov API locations endpoint)
-- and model study sites as a separate relational table.
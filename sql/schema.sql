CREATE TABLE IF NOT EXISTS studies (

    study_id SERIAL PRIMARY KEY,

    organization_full_name TEXT,
    organization_class TEXT,
    responsible_party TEXT,

    brief_title TEXT,
    full_title TEXT,

    overall_status TEXT,
    start_date DATE,

    standard_age TEXT,

    conditions TEXT,

    primary_purpose TEXT,

    interventions TEXT,
    intervention_description TEXT,

    study_type TEXT,

    phases TEXT,

    outcome_measure TEXT,

    medical_subject_headings TEXT,

    is_withheld BOOLEAN NOT NULL

);

CREATE INDEX idx_studies_overall_status
ON studies(overall_status);

CREATE INDEX idx_studies_start_date
ON studies(start_date);

CREATE INDEX idx_studies_study_type_phase
ON studies(study_type, phases);

CREATE INDEX idx_studies_organization
ON studies(organization_full_name);
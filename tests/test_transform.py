import pandas as pd
import pytest

from src.transform import transform


@pytest.fixture
def sample_df():
    """
    Small synthetic dataset covering:
    - duplicate studies
    - withheld studies
    - nullable fields
    """
    return pd.DataFrame(
        [
            {
                "Organization Full Name": "Hospital A",
                "Organization Class": "OTHER",
                "Responsible Party": "SPONSOR",
                "Brief Title": "Study A",
                "Full Title": "Study A Full",
                "Overall Status": "COMPLETED",
                "Start Date": "2023-01",
                "Standard Age": "ADULT",
                "Conditions": "Condition A",
                "Primary Purpose": "TREATMENT",
                "Interventions": "Drug A",
                "Intervention Description": "Description",
                "Study Type": "INTERVENTIONAL",
                "Phases": "Phase 2",
                "Outcome Measure": "Outcome",
                "Medical Subject Headings": "Heading",
            },
            # Exact duplicate (should be removed)
            {
                "Organization Full Name": "Hospital A",
                "Organization Class": "OTHER",
                "Responsible Party": "SPONSOR",
                "Brief Title": "Study A",
                "Full Title": "Study A Full",
                "Overall Status": "COMPLETED",
                "Start Date": "2023-01",
                "Standard Age": "ADULT",
                "Conditions": "Condition A",
                "Primary Purpose": "TREATMENT",
                "Interventions": "Drug A",
                "Intervention Description": "Description",
                "Study Type": "INTERVENTIONAL",
                "Phases": "Phase 2",
                "Outcome Measure": "Outcome",
                "Medical Subject Headings": "Heading",
            },
            # Withheld study
            {
                "Organization Full Name": "[Redacted]",
                "Organization Class": pd.NA,
                "Responsible Party": pd.NA,
                "Brief Title": pd.NA,
                "Full Title": pd.NA,
                "Overall Status": pd.NA,
                "Start Date": pd.NA,
                "Standard Age": pd.NA,
                "Conditions": pd.NA,
                "Primary Purpose": pd.NA,
                "Interventions": pd.NA,
                "Intervention Description": pd.NA,
                "Study Type": pd.NA,
                "Phases": pd.NA,
                "Outcome Measure": pd.NA,
                "Medical Subject Headings": pd.NA,
            },
            # Second withheld study (should NOT be removed)
            {
                "Organization Full Name": "[Redacted]",
                "Organization Class": pd.NA,
                "Responsible Party": pd.NA,
                "Brief Title": pd.NA,
                "Full Title": pd.NA,
                "Overall Status": pd.NA,
                "Start Date": pd.NA,
                "Standard Age": pd.NA,
                "Conditions": pd.NA,
                "Primary Purpose": pd.NA,
                "Interventions": pd.NA,
                "Intervention Description": pd.NA,
                "Study Type": pd.NA,
                "Phases": pd.NA,
                "Outcome Measure": pd.NA,
                "Medical Subject Headings": pd.NA,
            },
            # Row with nullable fields
            {
                "Organization Full Name": "Hospital B",
                "Organization Class": "OTHER",
                "Responsible Party": "SPONSOR",
                "Brief Title": "Study B",
                "Full Title": "Study B Full",
                "Overall Status": "RECRUITING",
                "Start Date": "2022-05",
                "Standard Age": pd.NA,
                "Conditions": "Condition B",
                "Primary Purpose": "PREVENTION",
                "Interventions": "Drug B",
                "Intervention Description": "Description",
                "Study Type": "INTERVENTIONAL",
                "Phases": pd.NA,
                "Outcome Measure": "Outcome",
                "Medical Subject Headings": "Heading",
            },
        ]
    )


def test_transform_pipeline(sample_df):
    """
    End-to-end transformation behaves as expected.
    """
    result = transform(sample_df)

    # 5 input rows
    # -1 duplicate
    # = 4 output rows
    assert len(result) == 4

    assert "is_withheld" in result.columns

    assert result["is_withheld"].sum() == 2

    assert "organization_full_name" in result.columns

    assert "Organization Full Name" not in result.columns

    assert pd.api.types.is_datetime64_any_dtype(result["start_date"])


def test_duplicate_rows_removed(sample_df):
    """
    Exact duplicate studies should be removed.
    """
    result = transform(sample_df)

    non_withheld = result[result["is_withheld"] == False]

    assert len(non_withheld) == 2


def test_withheld_rows_preserved(sample_df):
    """
    All withheld studies should be preserved and flagged.
    """
    result = transform(sample_df)

    withheld = result[result["is_withheld"]]

    assert len(withheld) == 2

    assert withheld["organization_full_name"].eq("[Redacted]").all()


def test_nullable_fields_allowed(sample_df):
    """
    Nullable columns should not cause transformation failure.
    """
    result = transform(sample_df)

    hospital_b = result[
        result["organization_full_name"] == "Hospital B"
    ]

    assert len(hospital_b) == 1


def test_missing_required_columns():
    """
    Missing required columns should raise an error.
    """
    bad_df = pd.DataFrame(
        {
            "Organization Full Name": ["Hospital A"]
        }
    )

    with pytest.raises(ValueError):
        transform(bad_df)
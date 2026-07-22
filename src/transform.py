import pandas as pd


REQUIRED_COLUMNS = [
    "Organization Full Name",
    "Start Date",
    "Brief Title",
    "Full Title",
]


STRING_COLUMNS = [
    "Organization Full Name",
    "Organization Class",
    "Responsible Party",
    "Brief Title",
    "Full Title",
    "Overall Status",
    "Standard Age",
    "Conditions",
    "Primary Purpose",
    "Interventions",
    "Intervention Description",
    "Study Type",
    "Phases",
    "Outcome Measure",
    "Medical Subject Headings",
]

COLUMN_MAPPING = {
    "Organization Full Name": "organization_full_name",
    "Organization Class": "organization_class",
    "Responsible Party": "responsible_party",
    "Brief Title": "brief_title",
    "Full Title": "full_title",
    "Overall Status": "overall_status",
    "Start Date": "start_date",
    "Standard Age": "standard_age",
    "Conditions": "conditions",
    "Primary Purpose": "primary_purpose",
    "Interventions": "interventions",
    "Intervention Description": "intervention_description",
    "Study Type": "study_type",
    "Phases": "phases",
    "Outcome Measure": "outcome_measure",
    "Medical Subject Headings": "medical_subject_headings",
}

def validate_columns(df):
    """
    Validate that required columns exist before transformation.
    """
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df


def drop_index_column(df):
    """
    Remove any unnamed index columns created during CSV export.
    """
    df = df.copy()

    unnamed_cols = [
        col for col in df.columns
        if col.startswith("Unnamed")
    ]

    return df.drop(columns=unnamed_cols)


def cast_column_types(df):
    """
    Cast columns to the data types expected downstream.
    """
    df = df.copy()

    if "Start Date" in df.columns:
        df["Start Date"] = pd.to_datetime(
            df["Start Date"],
            format="%Y-%m",
            errors="coerce"
        )

    existing_string_columns = [
        col for col in STRING_COLUMNS
        if col in df.columns
    ]

    df[existing_string_columns] = (
        df[existing_string_columns]
        .astype("string")
    )

    return df


def separate_withheld_rows(df):
    """
    Separate redacted studies from non-redacted studies.
    """
    if "Organization Full Name" not in df.columns:
        raise ValueError(
            "Organization Full Name column required to identify withheld rows"
        )

    withheld_mask = (
        df["Organization Full Name"]
        .str.strip()
        .eq("[Redacted]")
    )

    clean_df = df.loc[~withheld_mask].copy()
    withheld_df = df.loc[withheld_mask].copy()

    return clean_df, withheld_df


def remove_duplicate_studies(df):
    """
    Remove exact duplicate study records.
    """
    return df.drop_duplicates(
        ignore_index=True
    )


def add_withheld_flag(clean_df, withheld_df):
    """
    Add a flag identifying withheld studies and recombine datasets.
    """
    clean_df = clean_df.copy()
    withheld_df = withheld_df.copy()

    clean_df["is_withheld"] = False
    withheld_df["is_withheld"] = True

    return pd.concat(
        [
            clean_df,
            withheld_df
        ],
        ignore_index=True
    )


def validate_output(df):
    """
    Validate transformed dataframe before loading downstream.
    """
    if "is_withheld" not in df.columns:
        raise ValueError(
            "Transformation failed: is_withheld column missing"
        )

    if df.duplicated().sum() > 0:
        raise ValueError(
            "Transformation failed: duplicate rows remain"
        )

    return df

def rename_columns(df):
    """
    Rename columns to match the PostgreSQL schema.
    """
    return df.rename(columns=COLUMN_MAPPING)

def transform(df):
    """
    Execute the complete transformation pipeline.
    """

    df = validate_columns(df)

    df = drop_index_column(df)

    df = cast_column_types(df)

    clean_df, withheld_df = separate_withheld_rows(df)

    clean_df = remove_duplicate_studies(clean_df)

    ## for now unsure if these will get unredacted for the end user, will deduplicate to avoid problems mvp
    # df = add_withheld_flag(
    #     clean_df,
    #     withheld_df
    # )

    withheld_df = remove_duplicate_studies(withheld_df) ## removing duplicated redacted, would discuss with DG on visibility of data

    df = add_withheld_flag(
        clean_df,
        withheld_df
    )

    df = rename_columns(df)

    df = validate_output(df)

    return df
import pandas as pd


def process_uploaded_file(uploaded_file):
    """
    Read an uploaded CSV, Excel, or TXT file
    and convert it into a standard DataFrame.
    """

    file_name = uploaded_file.name.lower()

    # CSV file
    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    # Excel file
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    # Text file
    elif file_name.endswith(".txt"):
        content = uploaded_file.read().decode("utf-8")

        reviews = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        df = pd.DataFrame({
            "review": reviews
        })

    else:
        raise ValueError(
            "Unsupported file type. "
            "Please upload CSV, XLSX, or TXT."
        )

    return clean_feedback(df)


def clean_feedback(df):
    """
    Clean and standardize the feedback dataset.
    """

    # Create a copy so we don't modify the original
    df = df.copy()

    # Normalize column names
    df.columns = [
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        for column in df.columns
    ]

    # Possible names for the customer feedback column
    possible_columns = [
        "review",
        "reviews",
        "feedback",
        "comment",
        "comments",
        "text",
        "content"
    ]

    review_column = None

    # Find the feedback column
    for column in possible_columns:

        if column in df.columns:
            review_column = column
            break

    # If no feedback column exists
    if review_column is None:

        raise ValueError(
            "Could not find a feedback column. "
            "Expected a column such as "
            "'review', 'feedback', 'comment', or 'text'."
        )

    # Standardize the column name
    df = df.rename(
        columns={
            review_column: "review"
        }
    )

    # Handle missing values
    df["review"] = (
        df["review"]
        .fillna("")
        .astype(str)
    )

    # Remove unnecessary spaces
    df["review"] = df["review"].str.strip()

    # Remove empty reviews
    df = df[df["review"] != ""]

    # Remove duplicate reviews
    df = df.drop_duplicates(
        subset=["review"]
    )

    # Reset row numbers
    df = df.reset_index(drop=True)

    return df
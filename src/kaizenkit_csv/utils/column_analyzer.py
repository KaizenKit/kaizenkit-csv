def analyze_columns(df):
    """
    CSV列分析

    戻り値:

    [
        {
            "no": 1,
            "column": "name",
            "dtype": "object",
            "missing": 0,
            "unique": 5000
        }
    ]

    """

    result = []


    for index, column in enumerate(df.columns, start=1):

        result.append(
            {
                "no": index,
                "column": column,
                "dtype": str(df[column].dtype),
                "missing": int(df[column].isnull().sum()),
                "unique": int(df[column].nunique()),
            }
        )


    return result
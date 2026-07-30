import pandas as pd


def analyze_data_types(df):
    """
    CSV列のデータ型情報を取得する

    戻り値:
    [
        {
            "column": 列名,
            "dtype": 型,
            "count": 件数
        }
    ]
    """

    result = []


    for column in df.columns:

        result.append(
            {
                "column": column,
                "dtype": str(df[column].dtype),
                "count": int(df[column].count())
            }
        )


    return result
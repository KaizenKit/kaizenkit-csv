import pandas as pd


def analyze_numeric_columns(df):
    """
    数値列の統計情報を取得する

    戻り値:
    {
        列名: {
            min: 最小値,
            max: 最大値,
            mean: 平均値,
            median: 中央値
        }
    }
    """

    result = {}

    numeric_df = df.select_dtypes(
        include="number"
    )


    for column in numeric_df.columns:

        result[column] = {
            "min": numeric_df[column].min(),
            "max": numeric_df[column].max(),
            "mean": round(
                numeric_df[column].mean(),
                2
            ),
            "median": numeric_df[column].median(),
        }


    return result
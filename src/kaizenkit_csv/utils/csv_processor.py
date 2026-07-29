import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    重複行を削除する
    """
    return df.drop_duplicates()
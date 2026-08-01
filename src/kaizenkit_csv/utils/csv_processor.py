import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    重複行を削除する
    """

    try:
        return df.drop_duplicates()

    except Exception as e:
        raise Exception(
            f"重複削除処理でエラーが発生しました: {e}"
        )
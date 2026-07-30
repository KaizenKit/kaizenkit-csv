def analyze_missing(df):
    """
    欠損セル数を取得
    """
    return int(df.isnull().sum().sum())


def analyze_duplicates(df):
    """
    重複行数を取得
    """
    return int(df.duplicated().sum())
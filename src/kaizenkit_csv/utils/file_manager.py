import pandas as pd
from PySide6.QtWidgets import QFileDialog


def open_csv(parent=None):
    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        "CSVファイルを選択",
        "",
        "CSV Files (*.csv);;All Files (*)",
    )

    if not file_path:
        return None

    try:
        return pd.read_csv(file_path)

    except Exception:
        return None


def save_csv(parent, df):
    file_path, _ = QFileDialog.getSaveFileName(
        parent,
        "CSVを保存",
        "",
        "CSV Files (*.csv);;All Files (*)",
    )

    if not file_path:
        return False

    try:
        df.to_csv(
            file_path,
            index=False,
            encoding="utf-8-sig",
        )

        return True

    except Exception:
        return False
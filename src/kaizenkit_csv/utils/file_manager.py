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
        return None, None

    try:
        df = pd.read_csv(file_path)

        return df, file_path

    except Exception:
        return None, None
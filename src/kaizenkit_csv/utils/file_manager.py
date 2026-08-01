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
        return None, None, "ファイルが選択されていません"


    try:
        df = pd.read_csv(
            file_path,
            encoding="utf-8"
        )

        return df, file_path, None


    except UnicodeDecodeError:

        try:
            df = pd.read_csv(
                file_path,
                encoding="cp932"
            )

            return df, file_path, None


        except Exception as e:
            return None, None, str(e)


    except Exception as e:

        return None, None, str(e)
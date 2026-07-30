import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)

from kaizenkit_csv.config.app_info import APP_NAME, VERSION
from kaizenkit_csv.utils.file_manager import open_csv


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(1000, 700)

        self.df = None

        layout = QVBoxLayout()

        # タイトル
        title = QLabel(APP_NAME)
        version = QLabel(f"Version {VERSION}")

        # ボタン
        self.open_button = QPushButton("CSVを開く")
        self.remove_button = QPushButton("重複削除")
        self.save_button = QPushButton("CSV保存")

        # CSV情報
        info_title = QLabel("CSV情報")

        self.file_name_label = QLabel(
            "ファイル名：-"
        )

        self.row_count_label = QLabel(
            "行数：-"
        )

        self.column_count_label = QLabel(
            "列数：-"
        )

        # テーブル
        self.table = QTableWidget()

        # 配置
        layout.addWidget(title)
        layout.addWidget(version)

        layout.addWidget(self.open_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.save_button)

        layout.addWidget(info_title)
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.row_count_label)
        layout.addWidget(self.column_count_label)

        layout.addWidget(self.table)

        self.setLayout(layout)


        # イベント接続
        self.open_button.clicked.connect(
            self.open_csv_file
        )


    def open_csv_file(self):

        df, file_path = open_csv(self)


        if df is None:

            QMessageBox.warning(
                self,
                "読み込みエラー",
                "CSVファイルを読み込めませんでした。"
            )

            return


        self.df = df


        # CSV情報更新

        self.file_name_label.setText(
            f"ファイル名：{os.path.basename(file_path)}"
        )


        self.row_count_label.setText(
            f"行数：{len(df)}"
        )


        self.column_count_label.setText(
            f"列数：{len(df.columns)}"
        )


        # テーブル表示

        self.table.setRowCount(
            len(df)
        )

        self.table.setColumnCount(
            len(df.columns)
        )


        self.table.setHorizontalHeaderLabels(
            df.columns.tolist()
        )


        for row in range(len(df)):

            for col in range(len(df.columns)):

                item = QTableWidgetItem(
                    str(df.iat[row, col])
                )

                self.table.setItem(
                    row,
                    col,
                    item
                )
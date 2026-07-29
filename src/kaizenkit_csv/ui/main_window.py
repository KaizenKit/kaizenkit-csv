from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
)

from kaizenkit_csv.utils.file_manager import open_csv
from kaizenkit_csv.utils.csv_processor import remove_duplicates


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.df = None

        self.setWindowTitle("KaizenKit CSV")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("KaizenKit CSV")
        layout.addWidget(title)

        # CSV読み込みボタン
        self.open_button = QPushButton("CSVを開く")
        layout.addWidget(self.open_button)

        # 重複削除ボタン
        self.remove_button = QPushButton("重複削除")
        layout.addWidget(self.remove_button)

        # CSV表示テーブル
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # ボタン接続
        self.open_button.clicked.connect(self.open_csv_file)
        self.remove_button.clicked.connect(self.remove_duplicates)

    def open_csv_file(self):
        self.df = open_csv(self)

        if self.df is None:
            return

        self.display_dataframe()

    def remove_duplicates(self):
        if self.df is None:
            return

        self.df = remove_duplicates(self.df)

        self.display_dataframe()

    def display_dataframe(self):
        self.table.setRowCount(len(self.df))
        self.table.setColumnCount(len(self.df.columns))

        self.table.setHorizontalHeaderLabels(
            self.df.columns.tolist()
        )

        for row in range(len(self.df)):
            for col in range(len(self.df.columns)):
                item = QTableWidgetItem(
                    str(self.df.iat[row, col])
                )
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
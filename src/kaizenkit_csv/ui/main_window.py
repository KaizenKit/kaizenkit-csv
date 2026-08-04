import os
import webbrowser

from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)

from PySide6.QtGui import QIcon

from kaizenkit_csv.config.app_info import (
    APP_NAME,
    APP_VERSION,
    APP_AUTHOR,
    APP_DESCRIPTION,
)

from kaizenkit_csv.utils.file_manager import (
    open_csv,
)

from kaizenkit_csv.utils.data_analyzer import (
    analyze_missing,
    analyze_duplicates,
)

from kaizenkit_csv.utils.csv_processor import (
    remove_duplicates,
)

from kaizenkit_csv.utils.statistics import (
    analyze_numeric_columns,
)

from kaizenkit_csv.utils.column_analyzer import (
    analyze_columns,
)

from kaizenkit_csv.utils.report_generator import (
    generate_html_report,
    create_report_path,
)



class MainWindow(QWidget):


    def __init__(self):

        super().__init__()

        icon_path = (
        Path(__file__).resolve().parents[3]
        / "assets"
        / "icon.ico"
        )

        self.setWindowIcon(
        QIcon(str(icon_path))
        )

        self.setWindowTitle(
            APP_NAME
        )


        self.resize(
            1100,
            900
        )


        self.df = None

        self.current_file_path = None


        layout = QVBoxLayout()



        # --------------------
        # タイトル
        # --------------------

        title = QLabel(
            APP_NAME
        )


        version = QLabel(
            f"Version {APP_VERSION}"
        )



        # --------------------
        # ボタン
        # --------------------

        self.open_button = QPushButton(
            "CSVを開く"
        )


        self.remove_button = QPushButton(
            "重複削除"
        )


        self.save_button = QPushButton(
            "CSV保存"
        )


        self.report_button = QPushButton(
            "品質レポート出力"
        )

        self.about_button = QPushButton(
            "About"
        )



        # --------------------
        # CSV情報
        # --------------------

        info_title = QLabel(
            "CSV情報"
        )


        self.file_name_label = QLabel(
            "ファイル名：-"
        )


        self.row_count_label = QLabel(
            "行数：-"
        )


        self.column_count_label = QLabel(
            "列数：-"
        )



        # --------------------
        # データ品質
        # --------------------

        quality_title = QLabel(
            "データ品質"
        )


        self.missing_label = QLabel(
            "欠損セル数：-"
        )


        self.duplicate_label = QLabel(
            "重複行数：-"
        )



        # --------------------
        # 列分析
        # --------------------

        column_title = QLabel(
            "列分析"
        )


        self.column_table = QTableWidget()


        self.column_table.setColumnCount(
            5
        )


        self.column_table.setHorizontalHeaderLabels(
            [
                "No",
                "列名",
                "データ型",
                "欠損数",
                "ユニーク数",
            ]
        )
                # --------------------
        # 数値統計
        # --------------------

        statistics_title = QLabel(
            "数値統計"
        )


        self.statistics_table = QTableWidget()


        self.statistics_table.setColumnCount(
            5
        )


        self.statistics_table.setHorizontalHeaderLabels(
            [
                "列名",
                "最小値",
                "最大値",
                "平均値",
                "中央値",
            ]
        )



        # --------------------
        # CSV表示
        # --------------------

        self.table = QTableWidget()



        # --------------------
        # レイアウト配置
        # --------------------

        widgets = [

            title,

            version,


            self.open_button,

            self.remove_button,

            self.save_button,

            self.report_button,

            self.about_button,


            info_title,

            self.file_name_label,

            self.row_count_label,

            self.column_count_label,


            quality_title,

            self.missing_label,

            self.duplicate_label,


            column_title,

            self.column_table,


            statistics_title,

            self.statistics_table,


            self.table,

        ]


        for widget in widgets:

            layout.addWidget(
                widget
            )


        self.setLayout(
            layout
        )



        # --------------------
        # イベント設定
        # --------------------

        self.open_button.clicked.connect(
            self.open_csv_file
        )


        self.report_button.clicked.connect(
            self.export_report
        )

        self.about_button.clicked.connect(
        self.show_about
        )

        self.remove_button.clicked.connect(
        self.remove_duplicate_rows
        )

    def update_table(self, df):

        self.table.clear()

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

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(df.iat[row, col])
                    )
                )

        self.table.resizeColumnsToContents()

    def open_csv_file(self):

        df, file_path, error= open_csv(
            self
        )


        if error:

            QMessageBox.warning(
            self,
            "読み込みエラー",
            error
        )

            return



        self.df = df

        self.current_file_path = file_path



        # --------------------
        # CSV情報
        # --------------------

        self.file_name_label.setText(
            f"ファイル名：{os.path.basename(file_path)}"
        )


        self.row_count_label.setText(
            f"行数：{len(df)}"
        )


        self.column_count_label.setText(
            f"列数：{len(df.columns)}"
        )



        # --------------------
        # データ品質
        # --------------------

        self.missing_label.setText(
            f"欠損セル数：{analyze_missing(df)}"
        )


        self.duplicate_label.setText(
            f"重複行数：{analyze_duplicates(df)}"
        )



        # --------------------
        # 列分析
        # --------------------

        columns = analyze_columns(
            df
        )


        self.column_table.clearContents()


        self.column_table.setRowCount(
            len(columns)
        )


        for row, item in enumerate(columns):

            values = [

                item["no"],

                item["column"],

                item["dtype"],

                item["missing"],

                item["unique"],

            ]


            for col, value in enumerate(values):

                self.column_table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )



        self.column_table.resizeColumnsToContents()



        # --------------------
        # 数値統計
        # --------------------

        statistics = analyze_numeric_columns(
            df
        )


        self.statistics_table.clearContents()


        self.statistics_table.setRowCount(
            len(statistics)
        )


        for row, (column, value) in enumerate(statistics.items()):

            values = [

                column,

                value["min"],

                value["max"],

                value["mean"],

                value["median"],

            ]


            for col, item in enumerate(values):

                self.statistics_table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(item)
                    )
                )



        self.statistics_table.resizeColumnsToContents()



        # --------------------
        # CSV表表示
        # --------------------

        self.table.clear()


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

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(df.iat[row, col])
                    )
                )



        self.table.resizeColumnsToContents()


    def export_report(self):

        if self.df is None:

            QMessageBox.warning(
                self,
                "エラー",
                "先にCSVを開いてください。"
            )

            return


        output_path = create_report_path(
            self.current_file_path
        )


        columns = analyze_columns(
            self.df
        )


        statistics = analyze_numeric_columns(
            self.df
        )


        try:

            generate_html_report(
                self.df,
                os.path.basename(
                    self.current_file_path
                ),
                columns,
                analyze_missing(
                    self.df
                ),
                analyze_duplicates(
                    self.df
                ),
                statistics,
                output_path,
            )

        except Exception as e:

            QMessageBox.warning(
                self,
                "レポート生成エラー",
                f"レポート作成中にエラーが発生しました。\n\n{e}"
            )

            return


        try:

            webbrowser.open(
                output_path
            )

        except Exception:

            pass


        QMessageBox.information(
            self,
            "完了",
            f"品質レポートを出力しました。\n\n{output_path}"
        ) 

    def remove_duplicate_rows(self):

        if self.df is None:

            QMessageBox.warning(
                self,
                "エラー",
                "先にCSVを開いてください。"
            )

            return


        before = len(self.df)


        try:

            self.df = remove_duplicates(
                self.df
            )

            self.update_table(
                 self.df
            )

        except Exception as e:

            QMessageBox.warning(
                self,
                "削除エラー",
                str(e)
            )

            return


        after = len(self.df)


        self.row_count_label.setText(
            f"行数：{after}"
        )


        self.duplicate_label.setText(
            f"重複行数：0"
        )

        self.update_table(
            self.df
        )


        QMessageBox.information(
            self,
            "完了",
            f"重複削除しました。\n\n"
            f"削除前：{before}行\n"
            f"削除後：{after}行\n"
            f"削除数：{before-after}行"
        )

    def show_about(self):

        QMessageBox.information(
            self,
            "About",
            f"""
{APP_NAME}

Version {APP_VERSION}

{APP_DESCRIPTION}

Developed by {APP_AUTHOR}
"""
        )
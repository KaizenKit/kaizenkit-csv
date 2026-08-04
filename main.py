import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from kaizenkit_csv.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    icon_path = (
        Path(__file__).parent
        / "assets"
        / "icon.ico"
    )

    app.setWindowIcon(
        QIcon(str(icon_path))
    )

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
import sys
from PyQt6.QtWidgets import QApplication, QWidget


def main():
    application = QApplication(sys.argv)
    widget = QWidget()
    widget.setWindowTitle("BallGame")
    widget.show()
    sys.exit(application.exec())


if __name__ == "__main__":
    main()

import sys
from PyQt5.QtWidgets import QWidget, QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setWindowTitle("Test Window")
    widget.show()
    sys.exit(app.exec_())

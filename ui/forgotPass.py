import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton
)
from PyQt5.QtGui import QPixmap
from forgotPass2 import ForgotPass2Form
from ui.complaintAdmin import ComplaintAdminForm


class ForgotPassForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Form")
        self.setGeometry(100, 100, 400, 600)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/forgotPass.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()

        input_style = """
            QLineEdit {
                background-color: rgba(255, 255, 255, 200);
                padding: 8px;
                border-radius: 10px;
                font-size: 16px;
            }
        """
        button_style = """
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """

        # Admin Mail Label ve Input


        self.admin_mail = QLineEdit(self)
        self.admin_mail.setPlaceholderText("")
        self.admin_mail.setGeometry(160, 240, 160, 40)
        self.admin_mail.setStyleSheet(input_style)



        self.password = QLineEdit(self)
        self.password.setPlaceholderText("")
        self.password.setGeometry(230, 355, 80, 40)
        self.password.setStyleSheet(input_style)

        # Admin Login Button
        self.admin_btn = QPushButton("Admin Login", self)
        self.admin_btn.setGeometry(100, 430, 200, 50)
        self.admin_btn.setStyleSheet(button_style)
        self.admin_btn.clicked.connect(self.open_forgotPass2)

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    def open_forgotPass2(self):
        self.forgotp2_window = ForgotPass2Form()
        self.forgotp2_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ForgotPassForm()
    window.show()
    sys.exit(app.exec_())

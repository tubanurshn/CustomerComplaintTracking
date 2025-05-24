import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton
)
from PyQt5.QtGui import QPixmap



class ForgotPass2Form(QWidget):
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


        self.newPassword = QLineEdit(self)
        self.newPassword.setPlaceholderText("")
        self.newPassword.setGeometry(160, 240, 160, 40)
        self.newPassword.setStyleSheet(input_style)



        self.newPasswordAgain = QLineEdit(self)
        self.newPasswordAgain.setPlaceholderText("")
        self.newPasswordAgain.setGeometry(230, 355, 80, 40)
        self.newPasswordAgain.setStyleSheet(input_style)

        # Admin Login Button
        self.guncellePassword = QPushButton("Admin Login", self)
        self.guncellePassword.setGeometry(100, 430, 200, 50)
        self.guncellePassword.setStyleSheet(button_style)


    def resizeEvent(self, event):
        self.background_label.resize(self.size())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ForgotPass2Form()
    window.show()
    sys.exit(app.exec_())

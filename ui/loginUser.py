import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

from db.db_connection import check_student_login


class StudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Form")
        self.setGeometry(100, 100, 400, 600)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/loginUser.jpg"))
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

        # Student No Label ve Input
        self.label_student_no = QLabel("Student No:", self)
        self.label_student_no.setGeometry(60, 305, 80, 30)
        self.label_student_no.setStyleSheet("font-size: 16px; color: black;")

        self.student_no = QLineEdit(self)
        self.student_no.setPlaceholderText("Student No")
        self.student_no.setGeometry(160, 300, 180, 40)
        self.student_no.setStyleSheet(input_style)

        # Password Label ve Input
        self.label_password = QLabel("Password:", self)
        self.label_password.setGeometry(60, 365, 80, 30)
        self.label_password.setStyleSheet("font-size: 16px; color: black;")

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(160, 360, 180, 40)
        self.password.setStyleSheet(input_style)

        # User Login Button
        self.admin_btn = QPushButton("User Login", self)
        self.admin_btn.setGeometry(100, 430, 200, 50)
        self.admin_btn.setStyleSheet(button_style)
        self.admin_btn.clicked.connect(self.try_login)

        # "Don't have an account? Click here"
        self.register_label = QLabel(self)
        self.register_label.setText(
            '<a href="#">Don\'t have an account? Click here</a>'
        )
        self.register_label.setGeometry(100, 490, 250, 30)
        self.register_label.setStyleSheet("font-size: 14px; color: blue;")
        self.register_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.register_label.setOpenExternalLinks(False)
        self.register_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_label.linkActivated.connect(self.open_register)

        # "Forgot your password? Click here"
        self.forgot_label = QLabel(self)
        self.forgot_label.setText(
            '<a href="#">Forgot your password? Click here</a>'
        )
        self.forgot_label.setGeometry(100, 520, 250, 30)
        self.forgot_label.setStyleSheet("font-size: 14px; color: blue;")
        self.forgot_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.forgot_label.setOpenExternalLinks(False)
        self.forgot_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.forgot_label.linkActivated.connect(self.open_forgot_password)

    def try_login(self):
        student_no = self.student_no.text()
        password = self.password.text()

        if not student_no or not password:
            QMessageBox.warning(self, "Missing Information", "Please enter both student number and password.")
            return

        # Veritabanı kontrolü
        if check_student_login(student_no, password):
            QMessageBox.information(self, "Success", "Login successful!")
            # Giriş sonrası yapmak istediğin işlemler
            # Örnek: admin login penceresini açma kısmı buraya
            # subprocess.Popen([sys.executable, "sikayetFrame.py"]) gibi
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Student number or password is incorrect!")


    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    def open_admin_login(self):
        student_no = self.student_no.text()
        password = self.password.text()
        print(f"Student No: {student_no}, Password: {password}")
        subprocess.Popen([sys.executable, "loginAdmin.py"])
        self.close()

    def open_register(self):
        subprocess.Popen([sys.executable, "register.py"])
        self.close()

    def open_forgot_password(self):
        subprocess.Popen([sys.executable, "forgot_password.py"])
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())

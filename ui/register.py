import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton
)
from PyQt5.QtGui import QPixmap

class StudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Form")
        self.setGeometry(100, 100, 400, 600)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/registerr.jpg"))
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
        self.user_name = QLineEdit(self)
        self.user_name.setText("")  # Boş bırakıyoruz
        self.user_name.setPlaceholderText("")  # Placeholder'ı da boş yapıyoruz
        self.user_name.setGeometry(195, 214, 150, 40)
        self.user_name.setStyleSheet(input_style)
        # Admin Mail Label ve Input


        self.student_no = QLineEdit(self)
        self.student_no.setText("")  # Boş bırakıyoruz
        self.student_no.setPlaceholderText("")  # Placeholder'ı da boş yapıyoruz
        self.student_no.setGeometry(160, 280, 180, 40)
        self.student_no.setStyleSheet(input_style)

        # Password Label ve Input


        self.password = QLineEdit(self)
        self.password.setText("")  # Boş bırakıyoruz
        self.password.setPlaceholderText("")  # Placeholder'ı da boş yapıyoruz
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(160, 340, 180, 40)
        self.password.setStyleSheet(input_style)


        self.user_mail = QLineEdit(self)
        self.user_mail .setText("")  # Boş bırakıyoruz
        self.user_mail .setPlaceholderText("")  # Placeholder'ı da boş yapıyoruz
        self.user_mail .setEchoMode(QLineEdit.Password)
        self.user_mail .setGeometry(160, 410, 180, 40)
        self.user_mail .setStyleSheet(input_style)

        # Sign Up Button
        self.signup_btn = QPushButton("Sign Up", self)
        self.signup_btn.setGeometry(100, 490, 200, 50)
        self.signup_btn.setStyleSheet(button_style)
        self.signup_btn.clicked.connect(self.open_admin_login)

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    def open_admin_login(self):
        admin_mail = self.student_no.text()
        password = self.password.text()
        print(f"Admin mail: {admin_mail}, Password: {password}")

        subprocess.Popen([sys.executable, "loginAdmin.py"])
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())


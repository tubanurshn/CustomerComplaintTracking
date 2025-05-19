import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap
from db.db_connection import addUserToDatabase, isUserExist



class StudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Form")
        self.setGeometry(100, 100, 400, 600)

        self.background_label = QLabel(self)
        #self.background_label.setPixmap(QPixmap("../assets/images/registerr.jpg"))
        self.background_label.setPixmap(QPixmap())
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
<<<<<<< Updated upstream
        self.signup_btn.clicked.connect(self.register_user)
=======
        self.signup_btn.clicked.connect(self.open_user_login)
>>>>>>> Stashed changes

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

<<<<<<< Updated upstream
    def register_user(self):
        full_name = self.user_name.text().strip()
        student_number = self.student_no.text().strip()
        password = self.password.text().strip()
        email = self.user_mail.text().strip()

        # Basit kontroller
        if not full_name or not student_number or not password or not email:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        # Kullanıcı zaten varsa uyar
        if isUserExist(student_number, email):
            QMessageBox.warning(self, "Uyarı", "Bu öğrenci numarası veya e-posta zaten kayıtlı.")
            return

        # Kullanıcıyı ekle
        if addUserToDatabase(full_name, student_number, password, email):
            QMessageBox.information(self, "Başarılı", "Kayıt başarılı.")
            self.open_user_login()
        else:
            QMessageBox.critical(self, "Hata", "Kayıt sırasında bir hata oluştu.")

=======
>>>>>>> Stashed changes
    def open_user_login(self):
        subprocess.Popen([sys.executable, "loginUser.py"])
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Test Window")
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())

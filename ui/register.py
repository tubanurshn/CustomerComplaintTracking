import sys
import subprocess
import re
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap
from database.db_connection import addUserToDatabase, isUserExist  # Bu fonksiyonlar doğru tanımlanmalı

class StudentForm(QWidget):
    def __init__(self):  # <-- HATA DÜZELTİLDİ
        super().__init__()
        self.setWindowTitle("Register Form")
        self.setGeometry(100, 100, 400, 600)

        # Arka plan görseli
        self.background_label = QLabel(self)
        image_path = os.path.join(os.path.dirname(__file__), "../assets/images/registerr.jpg")
        self.background_label.setPixmap(QPixmap(image_path))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()

        # Stil ayarları
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

        # Kullanıcı adı
        self.user_name = QLineEdit(self)
        self.user_name.setPlaceholderText("Ad Soyad")
        self.user_name.setGeometry(195, 214, 150, 40)
        self.user_name.setStyleSheet(input_style)

        # Öğrenci numarası
        self.student_no = QLineEdit(self)
        self.student_no.setPlaceholderText("Öğrenci No")
        self.student_no.setGeometry(160, 280, 180, 40)
        self.student_no.setStyleSheet(input_style)

        # Şifre
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Şifre")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(160, 340, 180, 40)
        self.password.setStyleSheet(input_style)

        # E-posta
        self.user_mail = QLineEdit(self)
        self.user_mail.setPlaceholderText("E-Posta")
        self.user_mail.setGeometry(160, 410, 180, 40)
        self.user_mail.setStyleSheet(input_style)

        # Kayıt ol butonu
        self.signup_btn = QPushButton("Sign Up", self)
        self.signup_btn.setGeometry(100, 490, 200, 50)
        self.signup_btn.setStyleSheet(button_style)
        self.signup_btn.clicked.connect(self.register_user)

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    import re  # <-- regex için ekledik

    def register_user(self):
        full_name = self.user_name.text().strip()
        student_number = self.student_no.text().strip()
        password = self.password.text().strip()
        email = self.user_mail.text().strip()

        if not full_name or not student_number or not password or not email:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        # Öğrenci numarası kontrolü: sadece rakam içermeli
        if not student_number.isdigit():
            QMessageBox.warning(self, "Uyarı", "Öğrenci numarası sadece rakamlardan oluşmalıdır.")
            return

        # Şifre uzunluğu kontrolü
        if len(password) < 8 or len(password) > 15:
            QMessageBox.warning(self, "Uyarı", "Şifre 8 ile 15 karakter arasında olmalıdır.")
            return

        # E-posta formatı kontrolü
        email_regex = r'^[\w\.-]+@[\w\.-]+\.(com|net|edu|org)$'
        if not re.match(email_regex, email):
            QMessageBox.warning(self, "Uyarı", "Geçerli bir e-posta adresi giriniz. (.com, .net, .edu, .org)")
            return

        if isUserExist(student_number, email):
            QMessageBox.warning(self, "Uyarı", "Bu öğrenci numarası veya e-posta zaten kayıtlı.")
            return

        if addUserToDatabase(full_name, student_number, password, email):
            QMessageBox.information(self, "Başarılı", "Kayıt başarılı.")
            self.open_user_login()
        else:
            QMessageBox.critical(self, "Hata", "Kayıt sırasında bir hata oluştu.")

    def open_user_login(self):
        subprocess.Popen([sys.executable, "loginUser.py"])
        self.close()

# --- PROGRAMI BAŞLATAN KISIM ---
if __name__ == "__main__":  # <-- HATA DÜZELTİLDİ
    app = QApplication(sys.argv)
    form = StudentForm()
    form.show()
    sys.exit(app.exec_())

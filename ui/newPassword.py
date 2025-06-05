import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap
import mysql.connector
from database.db_connection import config

# Giriş ekranlarını import ediyoruz
from loginAdmin import LoginAdminForm
from loginUser import LoginUserForm

class NewPassword(QWidget):
    def __init__(self, role, user_id):
        super().__init__()
        self.role = role  # "admin" veya "student"
        self.user_id = user_id

        self.setWindowTitle("Yeni Şifre Belirleme")
        self.setGeometry(100, 100, 400, 600)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/re_password.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()

        input_style = """
            QLineEdit {
                background-color: rgba(255, 255, 255, 200);
                color: black;                   /* Metin rengi siyah */
                padding: 8px;
                border-radius: 10px;
                font-size: 16px;
            }
        """
        button_style = """
            QPushButton {
                background-color: white;
                color: black;                  /* Buton yazısı siyah */
                border-radius: 10px;
                font-size: 16px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Yeni şifre")
        self.password_input.setGeometry(160, 240, 160, 40)
        self.password_input.setStyleSheet(input_style)

        self.confirm_input = QLineEdit(self)
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText("Şifreyi tekrar girin")
        self.confirm_input.setGeometry(190, 350, 130, 40)
        self.confirm_input.setStyleSheet(input_style)

        self.ok_btn = QPushButton("Go", self)
        self.ok_btn.setGeometry(100, 470, 200, 50)
        self.ok_btn.setStyleSheet(button_style)
        self.ok_btn.clicked.connect(self.reset_password)

        # ---------- Geri Butonu ----------
        self.geri_btn = QPushButton("🔙", self)
        self.geri_btn.setGeometry(340, 540, 50, 50)
        self.geri_btn.setStyleSheet(button_style)
        self.geri_btn.clicked.connect(self.open_back)

    def open_back(self):
        from ui.loginUser import LoginUserForm

        self.login_user_window = LoginUserForm()
        self.login_user_window.show()
        self.close()

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    def reset_password(self):
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if password != confirm:
            QMessageBox.warning(self, "Hata", "Şifreler eşleşmiyor.")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Hata", "Şifre en az 8 karakter olmalıdır.")
            return

        table = "ogrenciler" if self.role == "student" else "adminler"

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            query = f"UPDATE {table} SET password = %s WHERE id = %s"
            cursor.execute(query, (password, self.user_id))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Şifreniz başarıyla güncellendi.")
            self.open_login_screen()
            self.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def open_login_screen(self):
        if self.role == "admin":
            self.login_form = LoginAdminForm()
        else:
            self.login_form = LoginUserForm()
        self.login_form.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewPassword("student", 1)  # test örneği
    window.show()
    sys.exit(app.exec_())

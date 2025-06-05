import sys
import subprocess
import os
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from database.db_connection import addAdminToDatabase, isAdminExist


class AdminRegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Register")
        self.setGeometry(100, 100, 400, 600)

        # Arka plan resmi
        self.background_label = QLabel(self)
        image_path = os.path.join(os.path.dirname(__file__), "../assets/images/admin_register.jpg")
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

        # İsim Soyisim
        self.full_name = QLineEdit(self)
        self.full_name.setPlaceholderText("Full Name")
        self.full_name.setGeometry(150, 250, 180, 30)
        self.full_name.setStyleSheet(input_style)

        # E-posta
        self.email = QLineEdit(self)
        self.email.setPlaceholderText("Email")
        self.email.setGeometry(150, 300, 180, 30)
        self.email.setStyleSheet(input_style)

        # Şifre
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(150, 350, 180, 30)
        self.password.setStyleSheet(input_style)

        # Kategori
        self.category = QComboBox(self)
        self.category.setGeometry(150, 400, 180, 30)
        self.category.addItems(["Select Category", "Cleanliness", "Security", "Education", "Other"])
        self.category.setStyleSheet(input_style)
        self.category.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: pink;
                border: 1.5px solid #ccc;
                border-radius: 10px;
                padding: 6px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #007ACC;
            }
        """)

        # Kayıt Butonu
        self.register_btn = QPushButton("Register", self)
        self.register_btn.setGeometry(100, 480, 200, 50)
        self.register_btn.setStyleSheet(button_style)
        self.register_btn.clicked.connect(self.register_admin)

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    def register_admin(self):
        full_name = self.full_name.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        category = self.category.currentText()

        if not full_name or not email or not password or category == "Select Category":
            QMessageBox.warning(self, "Warning", "Please fill all fields.")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Warning", "Password must be at least 8 characters.")
            return

        if '@' not in email:
            QMessageBox.warning(self, "Warning", "Please enter a valid email address.")
            return

        if isAdminExist(email):
            QMessageBox.warning(self, "Warning", "This admin is already registered.")
            return

        if addAdminToDatabase(full_name, email, password, category):
            QMessageBox.information(self, "Success", "Admin registered successfully.")
            subprocess.Popen([sys.executable, "loginAdmin.py"])
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Error occurred during registration.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = AdminRegisterForm()
    form.show()
    sys.exit(app.exec_())

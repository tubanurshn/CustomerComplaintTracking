import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton
)
from PyQt5.QtGui import QPixmap

from ui.complaintAdmin import ComplaintAdminForm
from admin_register import AdminRegisterForm

class LoginAdminForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Form")
        self.setGeometry(100, 100, 400, 600)

        # ---------- Arka plan ----------
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/loginAdmin.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()

        # ---------- Stil ----------
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

        # ---------- Mail ----------
        self.label_admin_mail = QLabel("Admin Mail:", self)
        self.label_admin_mail.setGeometry(60, 305, 100, 30)
        self.label_admin_mail.setStyleSheet("font-size: 16px; color: black;")

        self.admin_mail = QLineEdit(self)
        self.admin_mail.setPlaceholderText("Admin mail")
        self.admin_mail.setGeometry(160, 300, 180, 40)
        self.admin_mail.setStyleSheet(input_style)

        # ---------- Şifre ----------
        self.label_password = QLabel("Password:", self)
        self.label_password.setGeometry(60, 365, 100, 30)
        self.label_password.setStyleSheet("font-size: 16px; color: black;")

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(160, 360, 180, 40)
        self.password.setStyleSheet(input_style)

        # ---------- Giriş Butonu ----------
        self.admin_btn = QPushButton("Admin Login", self)
        self.admin_btn.setGeometry(100, 430, 200, 50)
        self.admin_btn.setStyleSheet(button_style)
        self.admin_btn.clicked.connect(self.open_complaint_admin)

        # ---------- Register Butonu ----------
        self.register_btn = QPushButton("Register", self)
        self.register_btn.setGeometry(100, 490, 200, 40)
        self.register_btn.setStyleSheet(button_style)
        self.register_btn.clicked.connect(self.open_admin_register)

    # --------- Arka plan pencere yeniden boyutlandırılırken ----------
    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    # --------- Giriş sonrası şikâyet yönetimi ekranı ----------
    def open_complaint_admin(self):
        #subprocess.Popen([sys.executable, "complaintAdmin.py"])
        self.compAdmin_window=ComplaintAdminForm()
        self.compAdmin_window.show()
        self.close()

    # --------- Register butonu: admin_register.py ekranını aç ----------
    def open_admin_register(self):
        #subprocess.Popen([sys.executable, "admin_register.py"])
        self.adminReg_window=AdminRegisterForm()
        self.adminReg_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginAdminForm()
    window.show()
    sys.exit(app.exec_())


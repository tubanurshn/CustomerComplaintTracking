import sys
import subprocess
from unicodedata import category

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

from ui.complaintAdmin import ComplaintAdminForm
from admin_register import AdminRegisterForm
from ui.forgotEmail import forgotEmailForm



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
        self.admin_btn.setGeometry(130, 410, 150, 50)
        self.admin_btn.setStyleSheet(button_style)
        self.admin_btn.clicked.connect(self.open_complaint_admin)

        # ---------- Geri Butonu ----------
        self.geri_btn = QPushButton("🔙", self)
        self.geri_btn.setGeometry(340, 540, 50, 50)
        self.geri_btn.setStyleSheet(button_style)
        self.geri_btn.clicked.connect(self.open_main)

        # ---------- Register Butonu ----------
        self.register_btn = QPushButton("Register", self)
        self.register_btn.setGeometry(130, 470, 150, 40)
        self.register_btn.setStyleSheet(button_style)
        self.register_btn.clicked.connect(self.open_admin_register)

    # --------- Arka plan pencere yeniden boyutlandırılırken ----------

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

    def open_forgot_password(self):
        #subprocess.Popen([sys.executable, "forgot_password.py"])
        self.forgotPass_window=forgotEmailForm("admin")
        self.forgotPass_window.show()
        self.close()



    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    # --------- Giriş sonrası şikâyet yönetimi ekranı ----------
    def open_complaint_admin(self):
        #subprocess.Popen([sys.executable, "complaintAdmin.py"])
        admin_mail = self.admin_mail.text()
        self.compAdmin_window=ComplaintAdminForm(admin_mail)
        self.compAdmin_window.show()
        self.close()

    def open_main(self):
        from ui.startFrame import StartFrameForm

        self.main_window = StartFrameForm()
        self.main_window.show()
        self.close()
    # --------- Register butonu: admin_register.py ekranını aç ----------
    def open_admin_register(self):

        self.adminReg_window=AdminRegisterForm()
        self.adminReg_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginAdminForm()
    window.show()
    sys.exit(app.exec_())


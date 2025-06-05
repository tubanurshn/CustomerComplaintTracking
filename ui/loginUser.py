import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox, QVBoxLayout
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt


from database.db_connection import check_student_login
from database.db_connection import get_student_by_login

from complaintUser import ComplaintUserForm
from ui.forgotEmail import forgotEmailForm



class LoginUserForm(QWidget):
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
                color: black; /* Yazı rengi siyah */
            }
        """

        button_style = """
            QPushButton {
                background-color: white;
                color: black; /* Yazı rengi siyah */
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

        # ---------- Geri Butonu ----------
        self.geri_btn = QPushButton("🔙", self)
        self.geri_btn.setGeometry(340, 540, 50, 50)
        self.geri_btn.setStyleSheet(button_style)
        self.geri_btn.clicked.connect(self.open_back)

    # def try_login(self):
    #     student_no = self.student_no.text()
    #     password = self.password.text()
    #
    #     if not student_no or not password:
    #         QMessageBox.warning(self, "Missing Information", "Please enter both student number and password.")
    #         return
    #
    #
    #     # Veritabanı kontrolü
    #    if check_student_login(student_no, password):
    #         #subprocess.Popen([sys.executable, "complaintUser.py"])
    #         #self.close()
    #         QMessageBox.information(self, "Success", "Login successful!")
    #         #BURADA GERÇEK STU NUMBERI ALIYOR SU ANDA
    #         self.complaint_window = ComplaintUserForm(student_number=student_no)
    #         self.complaint_window.show()
    #         self.close()
    #     else:
    #         QMessageBox.warning(self, "Error", "Student number or password is incorrect!")

    def try_login(self):
        student_no = self.student_no.text().strip()
        password = self.password.text().strip()

        if not student_no or not password:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen öğrenci numarası ve şifre girin.")
            return

        # Giriş yapan öğrencinin idsine falan ulaşıyoruz ki bu idyi kaydedelim ve complimentte bunu kullanalım
        student_data = get_student_by_login(student_no, password)

        if check_student_login(student_no, password):  # Eğer giriş başarılıysa
            student_id = student_data[0]  # ogrenciler.id
            student_number = student_data[1]  # ogrenciler.student_number

            QMessageBox.information(self, "Başarılı", "Giriş başarılı!")

            # Şikayet ekranını açarken hem id hem student_number geçiyoruz
            self.complaint_window = ComplaintUserForm(ogrenci_id=student_id, student_number=student_number)
            self.complaint_window.show()
            self.close()

        else:
            QMessageBox.warning(self, "Hata", "Öğrenci numarası veya şifre yanlış!")

    def resizeEvent(self, event):
        self.background_label.resize(self.size())
#BEN BU FONKSİYON KARDEŞİM NE ALAKAAAAA TR A0
    # def open_admin_login(self):
    #     student_no = self.student_no.text()
    #     password = self.password.text()
    #     print(f"Student No: {student_no}, Password: {password}")
    #     #subprocess.Popen([sys.executable, "loginAdmin.py"])
    #     from loginAdmin import LoginAdminForm
    #
    #     self.logAdin_window=LoginAdminForm()
    #     self.logAdin_window.show()
    #     self.close()

    def open_register(self):
        #subprocess.Popen([sys.executable, "register.py"])
        from ui.register import RegisterForm

        self.reg_window=RegisterForm()
        self.reg_window.show()
        self.close()

    def open_back(self):
        from ui.startFrame import StartFrameForm
        self.main_window=StartFrameForm()
        self.main_window.show()
        self.close()

    def open_forgot_password(self):
        #subprocess.Popen([sys.executable, "forgot_password.py"])
        self.forgotPass_window=forgotEmailForm("student")
        self.forgotPass_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginUserForm()
    window.show()
    sys.exit(app.exec_())

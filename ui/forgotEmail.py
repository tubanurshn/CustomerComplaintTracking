import sys
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPixmap
from database.db_connection import get_user_id_by_email
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException



class forgotEmailForm(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role  # 'admin' veya 'student'
        self.setWindowTitle("Şifre Sıfırlama")
        self.setGeometry(100, 100, 400, 600)

        self.user_id = None
        self.verification_code = None
        self.remaining_attempts = 3

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

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("E-posta adresiniz")
        self.email_input.setGeometry(120, 270, 160, 40)
        self.email_input.setStyleSheet(input_style)

        self.send_btn = QPushButton("Doğrulama Kodu Gönder", self)
        self.send_btn.setGeometry(100, 400, 200, 50)
        self.send_btn.setStyleSheet(button_style)
        self.send_btn.clicked.connect(self.send_verification_code)


        # ---------- Geri Butonu ----------
        self.geri_btn = QPushButton("🔙", self)
        self.geri_btn.setGeometry(340, 540, 50, 50)
        self.geri_btn.setStyleSheet(button_style)
        self.geri_btn.clicked.connect(self.open_back)

    def open_back(self):
        from ui.loginUser import LoginUserForm

        self.login_user_window=LoginUserForm()
        self.login_user_window.show()
        self.close()

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    def send_verification_code(self):
        from startFrame import StartFrameForm
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, "Hata", "Lütfen bir e-posta adresi girin.")
            return

        self.user_id = get_user_id_by_email(email, self.role)

        if not self.user_id:
            QMessageBox.critical(self, "Hata", "Bu e-posta sistemde kayıtlı değil.")
            return

        self.verification_code = self.generate_verification_code()
        try:
            self.send_email(email, self.verification_code)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))
            return

        code, ok = QInputDialog.getText(self, "Doğrulama", "E-postanıza gelen doğrulama kodunu girin:")
        while ok and code != self.verification_code:
            self.remaining_attempts -= 1
            if self.remaining_attempts <= 0:
                QMessageBox.critical(self, "Hata", "3 kez yanlış kod girildi. Başlangıç ekranına dönülüyor.")
                self.returning_window=StartFrameForm()
                self.returning_window.show()
                self.close()
                return
            code, ok = QInputDialog.getText(
                self, "Hatalı Kod",
                f"Kod yanlış. Kalan hakkınız: {self.remaining_attempts}\nTekrar deneyin:"
            )

        if ok and code == self.verification_code:
            QMessageBox.information(self, "Başarılı",
                                    "Doğrulama başarılı. Şifre belirleme ekranına yönlendiriliyorsunuz.")
            # Burada yeni şifre ekranını aç
            from newPassword import NewPassword
            self.new_pass = NewPassword(self.role, self.user_id)
            self.new_pass.show()
            self.close()

    def generate_verification_code(self):
        return ''.join(random.choices(string.digits, k=6))

    def send_email(self, to_email, code):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = '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'

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        send_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            subject="Şifre Sıfırlama Kodu",
            html_content=f"<html><body><h3>Doğrulama Kodunuz: <strong>{code}</strong></h3></body></html>",
            sender={"name": "Destek", "email": "beyza.koc@stu.fsm.edu.tr"}
        )

        try:
            api_instance.send_transac_email(send_email)
        except ApiException as e:
            raise Exception("E-posta gönderimi başarısız: " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = forgotEmailForm("admin")  # "student" için de kullanılabilir
    window.show()
    sys.exit(app.exec_())

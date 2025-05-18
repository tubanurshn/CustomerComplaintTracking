import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QVBoxLayout, QPushButton
)
from PyQt5.QtGui import QPixmap

class StudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Form")
        self.setGeometry(100, 100, 1000, 600)  # Pencere boyutu

        # --- Arka plan QLabel ---
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/registerUser.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()  # Arka plana al

        # --- Form içeriği ---
        self.student_no = QLineEdit()
        self.mail = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        # Input style (şeffaf ve köşeli)
        line_edit_style = """
            QLineEdit {
                background-color: rgba(255, 255, 255, 200);
                padding: 8px;
                border-radius: 10px;
                font-size: 16px;
            }
        """
        self.student_no.setStyleSheet(line_edit_style)
        self.mail.setStyleSheet(line_edit_style)
        self.password.setStyleSheet(line_edit_style)

        # Butonlar için stil (beyaz arka plan, siyah yazı)
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

        self.student_btn = QPushButton("Student Login", self)
        self.student_btn.setGeometry(220, 170, 190, 80)
        self.student_btn.setStyleSheet(button_style)
        self.student_btn.clicked.connect(self.open_student_login)

        self.admin_btn = QPushButton("Admin Login", self)
        self.admin_btn.setGeometry(220, 450, 190, 80)
        self.admin_btn.setStyleSheet(button_style)
        self.admin_btn.clicked.connect(self.open_admin_login)

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addStretch()
        main_layout.addStretch()

        self.setLayout(main_layout)

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    def open_student_login(self):
        # loginUser.py yi çalıştır
        subprocess.Popen([sys.executable, "loginUser.py"])
        self.close()  # Mevcut pencereyi kapat

    def open_admin_login(self):
        # loginAdmin.py yi çalıştır
        subprocess.Popen([sys.executable, "loginAdmin.py"])
        self.close()  # Mevcut pencereyi kapat


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QTextEdit, QRadioButton, QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont

from database.db_connection import addComplaintToDatabase, get_complaints_by_student,get_all_public_complaints


class ComplaintUserForm(QWidget):
    def __init__(self,ogrenci_id=None, student_number=None):
        super().__init__()
        self.student_number = student_number
        self.ogrenci_id = ogrenci_id
        self.setWindowTitle("Student Form")
        self.setGeometry(100, 100, 1500, 1000)

        # --- Background ---
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/mainAdmin.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()

        # --- Table Style ---
        table_style = """
            QTableWidget {
                background-color: #bed9e6 ;
                color: #003366;
                font-weight: bold;
                gridline-color: #8c9fa9;
            }
            QHeaderView::section {
                background-color: #bbc8cf;
                color: #003366;
                font-weight: bold;
            }
        """

        # --- Complaints Table (for student) ---
        self.userCompTable = QTableWidget(self)
        self.userCompTable.setGeometry(5, 385, 650, 350)
        self.userCompTable.setColumnCount(6)
        self.userCompTable.setHorizontalHeaderLabels(["Student No", "Status", "Complaint", "Privacy", "Answer", "Category"])
        self.userCompTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.userCompTable.verticalHeader().setVisible(True)
        self.userCompTable.setColumnWidth(2, 400)  # Wider column for complaint text
        self.userCompTable.verticalHeader().setDefaultSectionSize(60)
        self.userCompTable.setStyleSheet(table_style)

        # --- Public Complaints Table ---
        self.allPublicCompTable = QTableWidget(self)
        self.allPublicCompTable.setGeometry(770, 20, 650, 650)
        self.allPublicCompTable.setColumnCount(6)
        self.allPublicCompTable.setHorizontalHeaderLabels(
            ["Student No", "Status", "Complaint", "Privacy", "Answer", "Category"])
        self.allPublicCompTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.allPublicCompTable.verticalHeader().setVisible(True)
        self.allPublicCompTable.setColumnWidth(2, 300)
        self.allPublicCompTable.verticalHeader().setDefaultSectionSize(50)
        self.allPublicCompTable.setStyleSheet(table_style)


        # --- Complaint Entry Section ---
        self.complaint_label = QLabel("Enter Your Complaint:", self)
        self.complaint_label.setFont(QFont("Arial", 15))
        self.complaint_label.setGeometry(45, 65, 200, 30)
        self.complaint_label.setStyleSheet("color: #003366;")

        self.complaint_text = QTextEdit(self)
        self.complaint_text.setGeometry(200, 40, 400, 150)
        self.complaint_text.setStyleSheet("""
            QTextEdit {
                background-color:#bed9e6 ;
                color: #003366;
                font-size: 14px;
                font-family: Arial;
                border: 1px solid #999;
            }
        """)

        self.radio_public = QRadioButton("Public", self)
        self.radio_public.setGeometry(220, 190, 100, 30)
        self.radio_public.setStyleSheet("color: #003366;")
        self.radio_private = QRadioButton("Private", self)
        self.radio_private.setGeometry(330, 190, 100, 30)
        self.radio_private.setStyleSheet("color: #003366;")
        self.radio_public.setChecked(True)

        self.category_combo = QComboBox(self)
        self.category_combo.setGeometry(210, 230, 300, 30)
        self.category_combo.addItems(["Select Category", "Service", "Product", "Staff", "Other"])
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color:#bed9e6;
                color: #003366;
                font-weight: bold;
            }
            QComboBox QAbstractItemView {
                background-color: #c5dde6;
                color: #003366;
                selection-background-color: #B2EBF2;
                selection-color: #f4f9fc;
            }
        """)

        self.complaint_btn = QPushButton("Submit", self)
        self.complaint_btn.setGeometry(250, 270, 150, 40)
        self.complaint_btn.setStyleSheet("""
            QPushButton {
                background-color: #bed9e6;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005F9E;
            }
        """)
        self.complaint_btn.clicked.connect(self.complaint_user)

        # Load data on init
        self.load_user_complaints()
        self.load_public_complaints()

    # def complaint_user(self):
    #     student_number = self.student_number
    #     status = "işleniyor"
    #     answer = ""
    #     complaint = self.complaint_text.toPlainText().strip()
    #     category = self.category_combo.currentText().strip()
    #
    #     if self.radio_public.isChecked():
    #         privacy = "public"
    #     elif self.radio_private.isChecked():
    #         privacy = "private"
    #     else:
    #         QMessageBox.warning(self, "Uyarı", "Lütfen gizlilik tercihini seçin.")
    #         return
    #
    #     if not complaint or category == "Select Category":
    #         QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
    #         return
    #
    #     if len(complaint) < 10:
    #         QMessageBox.warning(self, "Uyarı", "Lütfen şikayetinizi en az 10 karakter olacak şekilde girin.")
    #         return
    #
    #     if addComplaintToDatabase(student_number, status, complaint, privacy, answer, category):
    #         QMessageBox.information(self, "Başarılı", "Kayıt başarılı.")
    #         self.load_user_complaints()
    #         self.complaint_text.clear()
    #     else:
    #         QMessageBox.critical(self, "Hata", "Kayıt sırasında bir hata oluştu.")

    def complaint_user(self):
        ogrenci_id = self.ogrenci_id  # Girişte alınan id
        student_number = self.student_number
        status = "işleniyor"
        answer = ""
        complaint = self.complaint_text.toPlainText().strip()
        category = self.category_combo.currentText().strip()

        if self.radio_public.isChecked():
            privacy = "public"
        elif self.radio_private.isChecked():
            privacy = "private"
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen gizlilik tercihini seçin.")
            return

        if not complaint or category == "Select Category":
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        if len(complaint) < 10:
            QMessageBox.warning(self, "Uyarı", "Lütfen şikayetinizi en az 10 karakter olacak şekilde girin.")
            return

        if addComplaintToDatabase(ogrenci_id, student_number, status, complaint, privacy, answer, category):
            QMessageBox.information(self, "Başarılı", "Kayıt başarılı.")
            self.load_user_complaints()
            self.complaint_text.clear()
        else:
            QMessageBox.critical(self, "Hata", "Kayıt sırasında bir hata oluştu.")

    def load_user_complaints(self):
        complaints = get_complaints_by_student(self.ogrenci_id)
        self.userCompTable.setRowCount(0) #tabloyu sıfırlıyor

        for i, row in enumerate(complaints):
            self.userCompTable.insertRow(i)
            for j, cell in enumerate(row):
                self.userCompTable.setItem(i, j, QTableWidgetItem(str(cell)))

    def load_public_complaints(self):
        public_complaints = get_all_public_complaints()  # artık tüm public şikayetler
        self.allPublicCompTable.setRowCount(0)
        for i, row in enumerate(public_complaints):
            self.allPublicCompTable.insertRow(i)
            for j, cell in enumerate(row):
                self.allPublicCompTable.setItem(i, j, QTableWidgetItem(str(cell)))

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

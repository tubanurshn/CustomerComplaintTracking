from PyQt5.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QTextEdit, QRadioButton, QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap

from database.db_connection import addComplaintToDatabase, get_complaints_by_student, get_all_public_complaints


class ComplaintUserForm(QWidget):
    def __init__(self, ogrenci_id=None, student_number=None):
        super().__init__()
        self.student_number = student_number
        self.ogrenci_id = ogrenci_id
        self.setWindowTitle("Student Complaint Form")
        self.setGeometry(100, 100, 1500, 1000)

        # Background
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/common.png"))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()

        # Title Style
        title_style = """
            color: #004a99;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 20px;
            font-weight: 700;
            padding-bottom: 6px;
            border-bottom: 3px solid #007ACC;
            background-color: rgba(240, 248, 255, 0.6);
        """

        # --- Section Titles ---
        self.complaint_title = QLabel("Enter Your Complaint", self)
        self.complaint_title.setGeometry(40, 10, 400, 40)
        self.complaint_title.setStyleSheet(title_style)

        self.user_complaints_title = QLabel("All Your Complaints", self)
        self.user_complaints_title.setGeometry(10, 340, 400, 40)
        self.user_complaints_title.setStyleSheet(title_style)

        self.public_complaints_title = QLabel("All Complaints", self)
        self.public_complaints_title.setGeometry(770, -10, 400, 40)
        self.public_complaints_title.setStyleSheet(title_style)

        # --- Complaints Table (for student) ---
        self.userCompTable = QTableWidget(self)
        self.userCompTable.setGeometry(5, 385, 650, 350)
        self.userCompTable.setColumnCount(6)
        self.userCompTable.setHorizontalHeaderLabels(["Student No", "Status", "Complaint", "Privacy", "Answer", "Category"])
        self.userCompTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.userCompTable.verticalHeader().setVisible(True)
        self.userCompTable.setColumnWidth(2, 400)
        self.userCompTable.verticalHeader().setDefaultSectionSize(60)

        # --- Public Complaints Table ---
        self.allPublicCompTable = QTableWidget(self)
        self.allPublicCompTable.setGeometry(770, 40, 650, 650)
        self.allPublicCompTable.setColumnCount(6)
        self.allPublicCompTable.setHorizontalHeaderLabels(
            ["Student No", "Status", "Complaint", "Privacy", "Answer", "Category"])
        self.allPublicCompTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.allPublicCompTable.verticalHeader().setVisible(True)
        self.allPublicCompTable.setColumnWidth(2, 300)
        self.allPublicCompTable.verticalHeader().setDefaultSectionSize(50)

        # Table style
        table_style = """
            QTableWidget {
                background-color: white;
                border-radius: 15px;
                gridline-color: #eee;
                font-weight: bold;
                color: #003366;
            }
            QTableWidget::item:selected {
                background-color: #007ACC;
                color: white;
            }
            QHeaderView::section {
                background-color: #007ACC;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: none;
            }
        """
        self.userCompTable.setStyleSheet(table_style)
        self.allPublicCompTable.setStyleSheet(table_style)

        # --- Complaint Entry Section ---
        self.complaint_text = QTextEdit(self)
        self.complaint_text.setGeometry(20, 60, 400, 250)
        self.complaint_text.setPlaceholderText("Enter your complaint here...")

        # Style for inputs
        input_style = """
            QTextEdit, QComboBox {
                background-color: white;
                border: 1.5px solid #ccc;
                border-radius: 10px;
                padding: 6px;
                font-size: 14px;
                color: #003366;
            }
            QTextEdit:focus, QComboBox:focus {
                border: 2px solid #007ACC;
            }
        """
        self.complaint_text.setStyleSheet(input_style)

        self.radio_public = QRadioButton("Public", self)
        self.radio_public.setGeometry(430, 100, 100, 30)
        self.radio_public.setStyleSheet("color: #003366; font-weight: bold;")
        self.radio_private = QRadioButton("Private", self)
        self.radio_private.setGeometry(510, 100, 100, 30)
        self.radio_private.setStyleSheet("color: #003366; font-weight: bold;")
        self.radio_public.setChecked(True)

        self.category_combo = QComboBox(self)
        self.category_combo.setGeometry(450, 160, 200, 30)
        self.category_combo.addItems(["Select Category", "Cleanliness", "Security", "Education", "Other"])
        self.category_combo.setStyleSheet(input_style)

        self.complaint_btn = QPushButton("Submit", self)
        self.complaint_btn.setGeometry(450, 200, 150, 40)
        self.complaint_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """)
        self.complaint_btn.clicked.connect(self.complaint_user)

        # Exit Button
        self.exit_btn = QPushButton("🚪 Çıkış Yap", self)
        self.exit_btn.setGeometry(130, 900, 120, 40)
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #bed9e6;
                color: #003366;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #005F9E;
                color: white;
            }
        """)


        # Şikayetleri yükle
        self.load_user_complaints()
        self.load_public_complaints()

        self.exit_btn.clicked.connect(self.exit_to_startframe)

    def exit_to_startframe(self):
        from ui.startFrame import StartFrameForm
        self.start_frame = StartFrameForm()
        self.start_frame.show()
        self.close()


    def complaint_user(self):
        ogrenci_id = self.ogrenci_id  # Girişte alınan id
        student_number = self.student_number
        status = "Process"
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

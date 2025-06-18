from PyQt5.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QTextEdit, QRadioButton, QComboBox, QPushButton, QMessageBox, QLineEdit
)
from PyQt5.QtGui import QPixmap

from database.db_connection import get_complaints_by_student,update_reject_text


class MyComplaintsForm(QWidget):
    def __init__(self, ogrenci_id=None, student_number=None):
        super().__init__()
        self.student_number = student_number
        self.ogrenci_id = ogrenci_id


        self.setWindowTitle("Student Complaint Form")
        self.setGeometry(100, 100, 750, 1000)

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
        self.complaint_title = QLabel("File an appeal", self)
        self.complaint_title.setGeometry(40, 10, 400, 40)
        self.complaint_title.setStyleSheet(title_style)

        self.user_complaints_title = QLabel("All Your Complaints", self)
        self.user_complaints_title.setGeometry(10, 320, 400, 40)
        self.user_complaints_title.setStyleSheet(title_style)

        # --- Complaint Entry Section ---
        self.reject_text = QTextEdit(self)
        self.reject_text.setGeometry(20, 60, 400, 250)
        self.reject_text.setPlaceholderText("Enter your reasons here...")

        self.complaint_id_input = QLineEdit(self)
        self.complaint_id_input.setGeometry(460, 60, 120, 30)
        self.complaint_id_input.setPlaceholderText("Complaint ID")
        self.complaint_id_input.setStyleSheet("""
            background-color: white;
            border: 1.5px solid #ccc;
            border-radius: 10px;
            padding: 6px;
            font-size: 14px;
            color: #003366;
        """)

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
        self.reject_text.setStyleSheet(input_style)

        # Submit Button
        self.complaint_btn = QPushButton("Submit", self)
        self.complaint_btn.setGeometry(450, 150, 150, 40)
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
        self.complaint_btn.clicked.connect(self.update_reject_text)

        # --- Complaints Table (for student) ---
        self.userCompTable = QTableWidget(self)
        self.userCompTable.setGeometry(5, 365, 700, 280)
        self.userCompTable.setColumnCount(7)
        self.userCompTable.setHorizontalHeaderLabels(["Complaint Id", "Student No", "Status", "Complaint", "Privacy", "Answer", "Category"])
        self.userCompTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.userCompTable.verticalHeader().setVisible(True)
        self.userCompTable.setColumnWidth(2, 400)
        self.userCompTable.verticalHeader().setDefaultSectionSize(60)

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

        # Exit Button
        self.exit_btn = QPushButton("🚪 Back", self)
        self.exit_btn.setGeometry(590, 660, 120, 40)
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
        self.exit_btn.clicked.connect(self.go_to_menuUser)

        # Load complaints AFTER table is defined
        self.load_user_complaints()

    def go_to_menuUser(self):
        from menuUser import MenuUserForm
        self.menu_user_window = MenuUserForm(
            ogrenci_id=self.ogrenci_id,
            student_number=self.student_number
        )
        self.menu_user_window.show()
        self.close()

    def exit_to_startframe(self):
        from ui.startFrame import StartFrameForm
        self.start_frame = StartFrameForm()
        self.start_frame.show()
        self.close()

    def update_reject_text(self):
        complaint_id = self.complaint_id_input.text().strip()
        reject_message = self.reject_text.toPlainText().strip()

        if not complaint_id or not reject_message:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen hem Complaint ID hem de red nedenini girin.")
            return

        try:
            success = update_reject_text(complaint_id, reject_message)
            if success:
                QMessageBox.information(self, "Başarılı", "Red açıklaması güncellendi.")
                self.load_user_complaints()
            else:
                QMessageBox.critical(self, "Hata", "Red açıklaması güncellenemedi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu:\n{str(e)}")

    def load_user_complaints(self):
        complaints = get_complaints_by_student(self.ogrenci_id)
        self.userCompTable.setRowCount(0)

        for i, row in enumerate(complaints):
            self.userCompTable.insertRow(i)
            for j, cell in enumerate(row):
                self.userCompTable.setItem(i, j, QTableWidgetItem(str(cell)))

    def resizeEvent(self, event):
        self.background_label.resize(self.size())
        super().resizeEvent(event)

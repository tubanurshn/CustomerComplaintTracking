import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QTextEdit, QRadioButton, QComboBox, QPushButton
)
from PyQt5.QtGui import QPixmap, QFont

class StudentForm(QWidget):
    def __init__(self):
        super().__init__()
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
                background-color: #69a2be ;
                color: #003366;
                font-weight: bold;
                gridline-color: #8ec0da;
            }
            QHeaderView::section {
                background-color: #B2EBF2;
                color: #003366;
                font-weight: bold;
            }
        """

        # --- Table 1 ---
        self.table1 = QTableWidget(self)
        self.table1.setGeometry(5, 350, 650, 350)
        self.table1.setColumnCount(3)
        self.table1.setHorizontalHeaderLabels(["First Name", "Last Name", "Company"])
        self.table1.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table1.verticalHeader().setVisible(True)
        self.table1.setColumnWidth(2, 150)
        self.table1.verticalHeader().setDefaultSectionSize(160)
        self.table1.setStyleSheet(table_style)

        for i in range(10):
            self.table1.insertRow(i)
            self.table1.setItem(i, 0, QTableWidgetItem(f"Name {i+1}"))
            self.table1.setItem(i, 1, QTableWidgetItem(f"Surname {i+1}"))
            self.table1.setItem(i, 2, QTableWidgetItem("Kusha Engineering"))

        # --- Table 2 ---
        self.table2 = QTableWidget(self)
        self.table2.setGeometry(750, 30, 650, 600)
        self.table2.setColumnCount(3)
        self.table2.setHorizontalHeaderLabels(["First Name", "Last Name", "Company"])
        self.table2.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table2.verticalHeader().setVisible(True)
        self.table2.setColumnWidth(2, 150)
        self.table2.verticalHeader().setDefaultSectionSize(160)
        self.table2.setStyleSheet(table_style)

        for i in range(10):
            self.table2.insertRow(i)
            self.table2.setItem(i, 0, QTableWidgetItem(f"Name {i+11}"))
            self.table2.setItem(i, 1, QTableWidgetItem(f"Surname {i+11}"))
            self.table2.setItem(i, 2, QTableWidgetItem("Kusha Engineering"))

        # --- Complaint Section ---

        # Label: "Enter your complaint"
        self.complaint_label = QLabel("Enter Your Complaint:", self)
        self.complaint_label.setFont(QFont("Arial", 15))
        self.complaint_label.setGeometry(45, 65, 200, 30)
        self.complaint_label.setStyleSheet("color: #003366;")

        # Text area (baby blue background, dark blue text)
        self.complaint_text = QTextEdit(self)
        self.complaint_text.setGeometry(200, 40, 400, 150)
        self.complaint_text.setStyleSheet("""
            QTextEdit {
                background-color: #69a2be ;
                color: #003366;
                font-size: 14px;
                font-family: Arial;
                border: 1px solid #999;
            }
        """)

        # Radio Buttons
        self.radio_public = QRadioButton("Public", self)
        self.radio_public.setGeometry(220, 190, 100, 30)
        self.radio_public.setStyleSheet("color: #003366;")
        self.radio_private = QRadioButton("Private", self)
        self.radio_private.setGeometry(330, 190, 100, 30)
        self.radio_private.setStyleSheet("color: #003366 ;")
        self.radio_public.setChecked(True)

        # ComboBox
        self.category_combo = QComboBox(self)
        self.category_combo.setGeometry(210, 230, 300, 30)
        self.category_combo.addItems(["Select Category", "Service", "Product", "Staff", "Other"])
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: #69a2be   ;
                color: #003366;
                font-weight: bold;
            }
             QComboBox QAbstractItemView {  
                 background-color: #E0F7FA;
                 color: #003366;
                 selection-background-color: #B2EBF2;
                 selection-color: #003366;
              }
        """)

        # Submit Button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setGeometry(250, 270, 150, 40)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005F9E;
            }
        """)

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())

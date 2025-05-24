import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ComplaintAdminForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Form")
        self.setGeometry(100, 100, 1500, 1000)

        # Arka plan resmi
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/mainAdmin.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()

        # --- Sol Üst: TableWidget ---
        self.table = QTableWidget(self)
        self.table.setGeometry(50, 50, 600, 300)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Ad", "Soyad", "Şirket"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(True)
        self.table.setColumnWidth(2, 150)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #E0F7FA;
                color: #003366;
                font-weight: bold;
                gridline-color: #B0BEC5;
            }
            QHeaderView::section {
                background-color: #B2EBF2;
                color: #003366;
                font-weight: bold;
            }
        """)
        for i in range(10):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(f"Ad {i + 1}"))
            self.table.setItem(i, 1, QTableWidgetItem(f"Soyad {i + 1}"))
            self.table.setItem(i, 2, QTableWidgetItem("Kusha Engineering"))

        # --- Sol Alt: LineEdit + TextEdit + ComboBox + Button ---
        self.comment_input = QLineEdit(self)
        self.comment_input.setPlaceholderText("Student Id:")
        #self.comment_input.setGeometry(50, 380, 400, 30)
        self.comment_input.setGeometry(70,480,400,30)


        self.comment_area = QTextEdit(self)
        self.comment_area.setGeometry(70, 560, 400, 200)
        self.comment_area.setPlaceholderText("Answer to the request from student:")

        self.combo = QComboBox(self)
        self.combo.setGeometry(470, 820, 120, 30)
        self.combo.addItems(["İşlem Seçin", "Reddet", "İşleme Al"])

        self.send_btn = QPushButton("Gönder", self)
        self.send_btn.setGeometry(470, 470, 120, 30)

        # --- Sağ Panel: Sabit boyutlu TextEdit ---
        self.right_text_area = QTextEdit(self)
        self.right_text_area.setGeometry(890, 90, 400, 770)
        self.right_text_area.setPlaceholderText("Detayları buraya yazın...")
        self.right_text_area.setReadOnly(False)

        # Stil ayarları
        self.comment_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 230);
                padding: 6px;
                border-radius: 10px;
                font-size: 14px;
            }
        """)
        self.comment_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 230);
                border-radius: 10px;
                font-size: 14px;
            }
        """)
        self.right_text_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 230);
                border-radius: 10px;
                font-size: 14px;
            }
        """)
        self.combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 10px;
                font-size: 14px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

    def resizeEvent(self, event):
        self.background_label.resize(self.size())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComplaintAdminForm()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPixmap

class StudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Form")
        self.setGeometry(100, 100, 1500, 1000)  # Pencere boyutu daha küçük

        # --- Arka plan QLabel ---
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/mainAdmin.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()  # Arka plana al

        # --- QTableWidget oluştur ---
        self.table = QTableWidget(self)  # parent = self
        self.table.setGeometry(5, 350, 650, 350)  # konum ve boyut
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Ad", "Soyad", "Şirket"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(True)
        self.table.setColumnWidth(2, 150)  # "Şirket" kolonu için genişlik
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #E0F7FA; /* buz mavisi */
                color: #003366; /* koyu lacivert yazı */
                font-weight: bold;
                gridline-color: #B0BEC5;
            }
            QHeaderView::section {
                background-color: #B2EBF2; /* başlık daha açık mavi */
                color: #003366;
                font-weight: bold;
            }
        """)
        # Scroll için örnek veriler
        for i in range(10):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(f"Ad {i+1}"))
            self.table.setItem(i, 1, QTableWidgetItem(f"Soyad {i+1}"))
            self.table.setItem(i, 2, QTableWidgetItem("Kusha Engineering"))

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())

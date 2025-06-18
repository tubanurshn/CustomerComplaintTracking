import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtGui import QPixmap

from database.db_connection import get_complaints_by_category_and_status, update_complaint_answer_and_status, \
    get_all_complaints_by_category,get_all_complaints
# burası reply sınıfı

class ReplyComplaintForm(QWidget):
    def __init__(self, email=None):
        super().__init__()
        self.email = email
        self.setWindowTitle("Student Form")
        self.setGeometry(100, 100, 750, 1000)

        # Arka plan resmi
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("../assets/images/common.png"))
        self.background_label.setScaledContents(True)
        self.background_label.resize(self.size())
        self.background_label.lower()

        # --- Başlıklar ---
        title_style = """
            color: #004a99;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 20px;
            font-weight: 700;
            padding-bottom: 6px;
            border-bottom: 3px solid #007ACC;
            background-color: rgba(240, 248, 255, 0.6);
        """

        self.label_new_complaints = QLabel("New Complaints", self)
        self.label_new_complaints.setGeometry(50, 5, 400, 40)
        self.label_new_complaints.setStyleSheet(title_style)

        self.label_reply = QLabel("Reply", self)
        self.label_reply.setGeometry(50, 360, 400, 35)
        # Reply başlığı için biraz daha küçük ve ince border
        reply_style = title_style.replace("20px", "18px").replace("3px", "2px")
        self.label_reply.setStyleSheet(reply_style)


        # --- Sol Üst: TableWidget ---
        self.newComp = QTableWidget(self)
        self.newComp.setGeometry(50, 50, 600, 300)
        self.newComp.setColumnCount(7)
        self.newComp.setHorizontalHeaderLabels(["Complaint Id","Student No", "Status", "Complaint", "Privacy", "Answer", "Category"])
        self.newComp.setEditTriggers(QTableWidget.NoEditTriggers)
        self.newComp.verticalHeader().setVisible(True)
        self.newComp.setColumnWidth(2, 150)


        self.newComp.setStyleSheet("""
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
        """)
        self.newComp.verticalHeader().setDefaultSectionSize(35)

        # --- Sol Alt: LineEdit + TextEdit + ComboBox + Button ---
        self.comment_input = QLineEdit(self)
        self.comment_input.setPlaceholderText("Complaint Id:")
        self.comment_input.setGeometry(50, 400, 400, 30)

        self.comment_area = QTextEdit(self)
        self.comment_area.setGeometry(50, 440, 400, 200)
        self.comment_area.setPlaceholderText("Answer to the request from student:")

        self.combo = QComboBox(self)
        self.combo.setGeometry(470, 450, 120, 30)
        self.combo.addItems(["Choose Action", "Reject", "Concluded"])

        self.send_btn = QPushButton("Send", self)
        self.send_btn.setGeometry(470, 530, 120, 30)
        self.send_btn.clicked.connect(self.send_reply)


        widget_style = """
            QLineEdit, QTextEdit, QComboBox {
                background-color: white;
                border: 1.5px solid #ccc;
                border-radius: 10px;
                padding: 6px;
                font-size: 14px;
                color: #003366;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #007ACC;
            }
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
        """
        self.comment_input.setStyleSheet(widget_style)
        self.comment_area.setStyleSheet(widget_style)
        self.combo.setStyleSheet(widget_style)
        self.send_btn.setStyleSheet(widget_style)

        self.load_user_complaints()

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

    def resizeEvent(self, event):
        self.background_label.resize(self.size())

    def load_user_complaints(self):
        category = get_complaints_by_category_and_status(self.email)
        self.newComp.setRowCount(0)

        for i, row in enumerate(category):
            self.newComp.insertRow(i)
            for j, cell in enumerate(row):
                self.newComp.setItem(i, j, QTableWidgetItem(str(cell)))


    def load_all_complaints(self):
        if self.category == "General Manager":
            all_complaints = get_all_complaints()  # tüm şikayetleri çek
        else:
            all_complaints = get_all_complaints_by_category(self.email)
        self.allComp.setRowCount(0)
        print("Gelen tüm şikayetler:", all_complaints)
        for i, row in enumerate(all_complaints):
            self.allComp.insertRow(i)
            for j, cell in enumerate(row):
                self.allComp.setItem(i, j, QTableWidgetItem(str(cell)))


    def go_to_menuUser(self):
        from menuAdmin import MenuAdminForm
        self.menu_user_window = MenuAdminForm(
            email=self.email,
        )
        self.menu_user_window.show()
        self.close()


    def send_reply(self):
        complaint_id = self.comment_input.text().strip()
        answer_text = self.comment_area.toPlainText().strip()
        selected_action = self.combo.currentText()

        if not complaint_id.isdigit():
            QMessageBox.warning(self, "Uyarı", "Geçerli bir Complaint ID giriniz.")
            return

        if not answer_text:
            QMessageBox.warning(self, "Uyarı", "Cevap alanı boş olamaz.")
            return

        if selected_action not in ["Reject", "Concluded"]:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir durum seçin (Reject / Concluded).")
            return

        result = update_complaint_answer_and_status(int(complaint_id), answer_text, selected_action)

        if result == 1:
            QMessageBox.information(self, "Başarılı", "Cevap ve durum başarıyla güncellendi.")
            self.comment_input.clear()
            self.comment_area.clear()
            self.combo.setCurrentIndex(0)
            self.load_user_complaints()

        elif result == 0:
            QMessageBox.warning(self, "Hata", "Belirtilen ID ile eşleşen bir şikayet bulunamadı.")
        else:
            QMessageBox.critical(self, "Hata", "Veritabanı işlemi sırasında hata oluştu.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReplyComplaintForm()
    window.show()
    sys.exit(app.exec_())

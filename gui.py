import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QMessageBox, QFormLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

class TossStyleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discord RPC")
        self.setFixedSize(400, 650)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QLineEdit {
                border: 1px solid #e1e1e1;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #3182f6;
            }
            QComboBox {
                border: 1px solid #e1e1e1;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: #333333;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QPushButton {
                background-color: #3182f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2c74db;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("DISCORD RPC")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #333333; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        main_layout.addLayout(form_layout)

        self.fields = {
            "Client ID": QLineEdit(),
            "내용 1": QLineEdit(),
            "내용 2": QLineEdit(),
            "이미지 이름": QLineEdit(),
            "이미지 내용": QLineEdit(),
            "버튼1 제목": QLineEdit(),
            "버튼1 URL": QLineEdit(),
            "버튼2 제목": QLineEdit(),
            "버튼2 URL": QLineEdit()
        }

        for label, widget in self.fields.items():
            form_layout.addRow(QLabel(label), widget)

        self.button_count = QComboBox()
        self.button_count.addItems(["0", "1", "2"])
        form_layout.addRow(QLabel("버튼 개수"), self.button_count)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        update_button = QPushButton("업데이트")
        update_button.clicked.connect(self.update)
        main_layout.addWidget(update_button)

        start_button = QPushButton("실행하기")
        start_button.clicked.connect(self.start)
        main_layout.addWidget(start_button)

    def update(self):
        client_id = self.fields["Client ID"].text()
        state = self.fields["내용 2"].text()
        details = self.fields["내용 1"].text()
        large_image = self.fields["이미지 이름"].text()
        large_text = self.fields["이미지 내용"].text()
        button_count = int(self.button_count.currentText())
        button_name1 = self.fields["버튼1 제목"].text()
        button_url1 = self.fields["버튼1 URL"].text()
        button_name2 = self.fields["버튼2 제목"].text()
        button_url2 = self.fields["버튼2 URL"].text()

        if not all([client_id, state, details]):
            self.show_message("오류", "빈칸이 있습니다")
            return

        if button_count == 1 and not all([button_name1, button_url1]):
            self.show_message("오류", "버튼 개수 1을 선택하였습니다\n버튼1 제목,URL을 입력하셔야 합니다")
            return

        if button_count == 2 and not all([button_name1, button_url1, button_name2, button_url2]):
            self.show_message("오류", "버튼 개수 2를 선택하였습니다\n버튼1 제목,URL 와 버튼2 제목,URL을 입력하셔야 합니다")
            return

        with open("discord_rpc.txt", 'w') as f:
            f.write(f"{client_id},{state},{details},{large_image},{large_text},{button_count},{button_name1},{button_url1},{button_name2},{button_url2}")

        self.show_message("알림", "업데이트가 완료되었습니다")

    def start(self):
        try:
            with open("discord_rpc.txt", 'r') as f:
                line = f.readline().split(",")

            # Here you would typically start the Discord RPC
            # For demonstration, we'll just show a success message
            self.show_message("알림", "Discord RPC가 시작되었습니다")
        except Exception as e:
            self.show_message("오류", f"실행에 실패했습니다: {str(e)}")

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #333333;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #3182f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #2c74db;
            }
        """)
        msg_box.exec_()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '확인', '정말 프로그램을 종료하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TossStyleApp()
    window.show()
    sys.exit(app.exec_())

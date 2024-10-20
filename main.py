import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QMessageBox, QFormLayout, QSpacerItem, QSizePolicy,
                             QDialog, QProgressBar)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer
from pypresence import Presence
import tempfile
import os
import time

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("로딩 중...")
        self.setFixedSize(300, 100)
        layout = QVBoxLayout(self)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("초기화 중...", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QProgressBar {
                border: 2px solid #3182f6;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3182f6;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
        """)

    def update_progress(self, value, status):
        self.progress_bar.setValue(value)
        self.status_label.setText(status)


class TossStyleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discord RPC")
        self.setFixedSize(500, 750)
        self.setStyleSheet("""
            * {
                font-weight: bold;
            }              
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                padding: 8px;
                color: #333333;
            }
            QLineEdit {
                border: 1px solid #e1e1e1;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                color: #333333;
                font-weight: normal;
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
                background-color: white;
            }
            QComboBox::drop-down {
                width: 40px;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #3182f6;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #3182f6;
                selection-color: white;
                padding: 5px;
                font-weight: bold;
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
        
        self.file_number = QComboBox()
        self.file_number.addItems([str(i) for i in range(1, 11)])
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_number)
        load_button = QPushButton("불러오기")
        load_button.clicked.connect(self.load_file)
        file_layout.addWidget(load_button)
        form_layout.addRow(QLabel("파일 번호"), file_layout)
        

        try:
                with open(f"{tempfile.gettempdir()}\\discord_rpc_1.txt", 'r', encoding="utf-8") as f:
                        line = f.readline().split(",")
                        
                self.fields = {
                    "Client ID": QLineEdit(line[0]),
                    "내용 1": QLineEdit(line[1]),
                    "내용 2": QLineEdit(line[2]),
                    "이미지 이름": QLineEdit(line[3]),
                    "이미지 내용": QLineEdit(line[4]),
                    "버튼1 제목": QLineEdit(line[6]),
                    "버튼1 URL": QLineEdit(line[7]),
                    "버튼2 제목": QLineEdit(line[8]),
                    "버튼2 URL": QLineEdit(line[9])
                }
                button_count = int(line[5])
        except:
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
                button_count = 0

        for label, widget in self.fields.items():
            form_layout.addRow(QLabel(label), widget)

        self.button_count = QComboBox()
        self.button_count.addItems(["0", "1", "2"])
        self.button_count.setCurrentIndex(button_count)
        form_layout.addRow(QLabel("버튼 개수"), self.button_count)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        update_button = QPushButton("저장하기")
        update_button.clicked.connect(self.update)
        main_layout.addWidget(update_button)

        start_button = QPushButton("실행하기")
        start_button.clicked.connect(self.start)
        main_layout.addWidget(start_button)
        
    def load_file(self):
        file_number = self.file_number.currentText()
        file_path = f"{tempfile.gettempdir()}\\discord_rpc_{file_number}.txt"
        
        if not os.path.exists(file_path):
            self.show_error("오류", f"파일 {file_number}이(가) 존재하지 않습니다.")
            return

        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                line = f.readline().split(",")
            
            for i, (key, widget) in enumerate(self.fields.items()):
                if i < len(line):
                    widget.setText(line[i])
                else:
                    widget.setText("")
            
            try:
                self.button_count.setCurrentText(line[9])
            except:
                self.button_count.setCurrentText("0")
            
            self.show_message("알림", f"파일 {file_number}번에서 설정을 불러왔습니다.")
        except Exception as e:
            self.show_error("오류", f"파일 {file_number}번을 불러오는 중 오류가 발생했습니다: {str(e)}")

    def update(self):
        file_number = self.file_number.currentText()
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
        
        if button_count == 0 and button_name1 != "" and button_url1 != "":
            self.show_warning("주의", "버튼 개수 0을 선택하였습니다.\n버튼1 제목,URL의 내용은 무시됩니다.")
        elif button_count == 0 and (button_name2 != "" or button_url2 != ""):
            self.show_warning("주의", "버튼 개수 0을 선택하였습니다.\n버튼2 제목,URL의 내용은 무시됩니다.")
        elif button_count == 0 and (button_name1 != "" or button_url1 != "") and (button_name2 != "" or button_url2 != ""):
            self.show_warning("주의", "버튼 개수 0을 선택하였습니다.\n버튼1,2 제목,URL의 내용은 무시됩니다.")
        elif button_count == 1 and (button_name2 != "" or button_url2 != ""):
            self.show_warning("주의", "버튼 개수 1을 선택하였습니다.\n버튼2 제목,URL의 내용은 무시됩니다.")
        

        if not all([client_id, state, details]):
            self.show_error("오류", "빈칸이 있습니다")
            return

        if button_count == 1 and not all([button_name1, button_url1]):
            self.show_error("오류", "버튼 개수 1을 선택하였습니다\n버튼1 제목,URL을 입력하셔야 합니다")
            return

        if button_count == 2 and not all([button_name1, button_url1, button_name2, button_url2]):
            self.show_error("오류", "버튼 개수 2를 선택하였습니다\n버튼1 제목,URL 와 버튼2 제목,URL을 입력하셔야 합니다")
            return

        
        with open(f"{tempfile.gettempdir()}\\discord_rpc_{file_number}.txt", 'w', encoding="utf-8") as f:
            f.write(f"{client_id},{state},{details},{large_image},{large_text},{button_count},{button_name1},{button_url1},{button_name2},{button_url2}")

        self.show_message("알림", "저장 완료되었습니다")

    def start(self):
        try:
            loading_dialog = LoadingDialog(self)
            loading_dialog.show()

            def update_progress(value, status):
                loading_dialog.update_progress(value, status)
                QApplication.processEvents()
            
            update_progress(0, "설정 파일 불러오는 중...")
            file_number = self.file_number.currentText()

            update_progress(2, "설정 파일 읽는 중...")
            with open(f"{tempfile.gettempdir()}\\discord_rpc_{file_number}.txt", 'r', encoding="utf-8") as f:
                line = f.readline().split(",")

            update_progress(4, "Discord RPC 연결 중...")
            time.sleep(0.1)
            update_progress(16, "Discord RPC 연결 중...")
            time.sleep(0.1)
            update_progress(20, "Discord RPC 연결 중...")
            client_id = line[0]
            RPC = Presence(client_id)
            RPC.connect()
            
            update_progress(30, "RPC 상태 업데이트 중...")
            time.sleep(0.2)
            update_progress(40, "RPC 상태 업데이트 중...")
            time.sleep(0.3)
            if line[5] == '1':
                update_progress(60, "RPC 상태 업데이트 중...")
                time.sleep(0.1)
                if line[3] == "":
                    update_progress(80, "RPC 상태 업데이트 중...")
                    RPC.update(state=line[1], details=line[2], buttons=[{"label": line[6], "url": line[7]}])
                else:
                    update_progress(80, "RPC 상태 업데이트 중...")
                    RPC.update(state=line[1], details=line[2], large_image=line[3], large_text=line[4], buttons=[{"label": line[6], "url": line[7]}])
            elif line[5] == '2':
                time.sleep(0.1)
                update_progress(60, "RPC 상태 업데이트 중...")
                if line[3] == "":
                    update_progress(80, "RPC 상태 업데이트 중...")
                    RPC.update(state=line[1], details=line[2], buttons=[{"label": line[6], "url": line[7]}, {"label": line[8], "url": line[9]}])
                else:
                    update_progress(80, "RPC 상태 업데이트 중...")
                    RPC.update(state=line[1], details=line[2], large_image=line[3], large_text=line[4], buttons=[{"label": line[6], "url": line[7]}, {"label": line[8], "url": line[9]}])
            else:
                time.sleep(0.1)
                update_progress(60, "RPC 상태 업데이트 중...")
                if line[3] == "":
                    update_progress(80, "RPC 상태 업데이트 중...")
                    RPC.update(state=line[1], details=line[2])
                else:
                    update_progress(80, "RPC 상태 업데이트 중...")
                    RPC.update(state=line[1], details=line[2], large_image=line[3], large_text=line[4])
                    
            time.sleep(0.4)
                    
            update_progress(100, "완료!")
            QTimer.singleShot(500, loading_dialog.close)  # 0.5초 후 로딩 창 닫기
            self.show_message("알림", "Discord RPC가 시작되었습니다")
            
        except Exception as e:
            self.show_error("오류", f"실행에 실패했습니다: {str(e)}")

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
        
    def show_warning(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
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

    def show_error(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
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

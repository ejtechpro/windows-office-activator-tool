import sys
import qtawesome as qta
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout,
    QTextEdit, QPushButton, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtCore import Qt, QPoint

from resource_path import resource_path
from threads.internet_thread import InternetCheckThread
from threads.process_thread import ProcessThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows & Office Activator")
        self.setFixedSize(400, 250)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.CustomizeWindowHint)
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

        self.dragging = False
        self.offset = QPoint()
        self.internet_available = False 
        self.init_ui()
        self.apply_styles()
        self.start_internet_monitor()

    def init_ui(self):
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

        # --- Custom Title Bar ---
        self.title_bar = QWidget()
        self.title_bar.setObjectName("TitleBar")
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(8, 4, 8, 4)

        # Icon & Title
        self.icon_label = QLabel()
        self.icon_label.setPixmap(qta.icon("fa5s.terminal", color="#bbbbbb").pixmap(16, 16))
        title_text = QLabel("Windows & Office Activator v1.0")
        title_text.setObjectName("TitleLabel")

        # Minimize & Close
        btn_min = QPushButton(qta.icon("fa5s.minus", color="#cccccc"), "")
        btn_min.setObjectName("TitleBtn")
        btn_min.clicked.connect(self.showMinimized)

        btn_close = QPushButton(qta.icon("fa5s.times", color="#cccccc"), "")
        btn_close.setObjectName("TitleBtn")
        btn_close.clicked.connect(self.close)

        title_layout.addWidget(self.icon_label)
        title_layout.addWidget(title_text)
        title_layout.addStretch()
        title_layout.addWidget(btn_min)
        title_layout.addWidget(btn_close)

        # Info Area
        self.body = QTextEdit()
        self.body.setReadOnly(True)
        self.body.setPlainText(
            "─────────────────────────────\n"
            "   Application Information   \n"
            "─────────────────────────────\n"
            f"Version     :  1.0\n"
            f"Release     :  August 10, 2025\n"
            f"Compiler    :  Delphi 7.3 Lite\n"
            f"Developer   :  ejtechpro\n"
        )


        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.start_btn = QPushButton("Start")
        self.close_btn = QPushButton("Close")
        self.close_btn.setObjectName("CloseButton")

        self.start_btn.clicked.connect(self.start_process)
        self.close_btn.clicked.connect(self.close)

        btn_layout.addStretch()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.close_btn)
        btn_layout.addStretch()

        # Assemble Layout
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.body)
        main_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        main_layout.addLayout(btn_layout)

        self.setCentralWidget(container)

    # ---- Internet Monitor ----
    def start_internet_monitor(self):
        self.net_thread = InternetCheckThread()
        self.net_thread.internet_status.connect(self.update_internet_status)
        self.net_thread.start()

    def update_internet_status(self, status):
        if status != self.internet_available:  # Only log if status changed
            if status:
                self.icon_label.setPixmap(qta.icon("fa5s.check-circle", color="green").pixmap(16, 16))
                self.body.append("\n✅ Internet Connected.")
            else:
                self.icon_label.setPixmap(qta.icon("fa5s.times-circle", color="red").pixmap(16, 16))
                self.body.append("\n⚠ No Internet Connection Detected!")
            self.scrollToView()
        self.internet_available = status

    # ---- Start Button ----
    def start_process(self):
        if not self.internet_available:
            self.body.append("\n⚠ Please connect to the internet before starting.")
            self.scrollToView()
            return

        self.body.append("\nProcessing...")
        self.start_btn.setEnabled(False) 
        self.close_btn.setEnabled(False) 

        self.process_thread = ProcessThread()
        self.process_thread.process_done.connect(self.process_finished)
        self.process_thread.start()

    def process_finished(self, success, message):
        self.body.append("\n" + message)
        self.start_btn.setEnabled(True) 
        self.close_btn.setEnabled(True) 

    # ---- Dragging Logic ----
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.is_in_title_bar(event.pos()):
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.move(event.globalPos() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging = False

    def is_in_title_bar(self, pos):
        return self.title_bar.geometry().contains(pos)
    
    def closeEvent(self, event):
        if hasattr(self, "net_thread") and self.net_thread.isRunning():
            self.net_thread.stop()
            self.net_thread.wait()
        super().closeEvent(event)
    
    def scrollToView(self):
        cursor = self.body.textCursor()
        cursor.movePosition(cursor.End)
        self.body.setTextCursor(cursor)
        
    
    def apply_styles(self):
        try:
            qss_path = resource_path("styles.qss")
            with open(qss_path, "r", encoding="utf-8") as f:
                style = f.read()
                self.setStyleSheet(style)
        except Exception as e:
            self.body.append(f"\nError: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

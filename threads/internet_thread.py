from PySide6.QtCore import QThread, Signal
import socket

class InternetCheckThread(QThread):
    internet_status = Signal(bool)

    def __init__(self):
        super().__init__()
        self._running = True  # flag to control loop

    def run(self):
        while self._running:
            status = self.check_internet()
            self.internet_status.emit(status)
            # Sleep in small chunks so stop() is responsive
            for _ in range(10):
                if not self._running:
                    break

    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def stop(self):
        """Request the thread to stop."""
        self._running = False

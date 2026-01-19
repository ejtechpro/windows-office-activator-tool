from PySide6.QtCore import QThread, Signal
import subprocess

class ProcessThread(QThread):
    process_done = Signal(bool, str)  # success, message

    def run(self):
        try:
            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy", "Bypass",
                    "-Command",
                    "irm https://get.activated.win | iex"
                ],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.process_done.emit(True, "✅ Process completed.")
        except subprocess.CalledProcessError as e:
            self.process_done.emit(False, f"❌ Error: {e}")
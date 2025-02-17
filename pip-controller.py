import sys
import ctypes
import pyautogui
import time
import threading
import win32gui
import win32con
import win32process
import win32api
import psutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QFontDatabase, QPalette, QColor, QIcon

class YouTubePiPController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.monitoring = False
        self.setWindowTitle("YouTube PiP Controller")
        self.setGeometry(100, 100, 600, 400)  # Define size and position of the window

        # Set a semi-transparent grey background
        self.set_background_color()

        # Load Google Fonts (Poppins or Roboto)
        self.load_fonts()

        # UI elements setup
        self.setup_ui()
        self.user32 = ctypes.windll.user32

        # Tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icons/tray_icon.png"))
        self.tray_icon.setVisible(True)

        # Tray icon menu
        tray_menu = QMenu(self)
        minimize_action = QAction("Minimize", self)
        minimize_action.triggered.connect(self.minimize_to_tray)
        tray_menu.addAction(minimize_action)

        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        restore_action = QAction("Restore", self)
        restore_action.triggered.connect(self.restore_from_tray)
        tray_menu.addAction(restore_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        # Make window resizable (optional)
        self.setWindowFlags(QtCore.Qt.Widget)  # Allow window resizing
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)  # Set window to opaque

        self.is_pip_active = False
        self.monitoring = False

    def set_background_color(self):
        """Set a semi-transparent grey background."""
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(50, 50, 50, 240))  # RGB + Alpha for transparency
        self.setPalette(palette)

    def load_fonts(self):
        """Load Google Fonts (Poppins or Roboto) from files."""
        font_id = QFontDatabase.addApplicationFont("fonts/Poppins-Regular.ttf")  # Add the Poppins font
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            QtGui.QFontDatabase.addApplicationFont(font_family)  # Register the font

    def set_font(self, font_name):
        """Sets Google Font for the UI elements."""
        font = QtGui.QFont(font_name)
        self.setFont(font)

    def setup_ui(self):
        """Sets up the UI with a sleek, modern look."""
        # Main layout
        main_layout = QVBoxLayout()

        # Title Label (This is the title bar now)
        title_label = QLabel("YouTube PiP Controller", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; padding: 20px;")
        main_layout.addWidget(title_label)

        # Status Label
        self.status_label = QLabel("Status: Stopped", self)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: #BBBBBB; padding: 10px;")
        main_layout.addWidget(self.status_label)

        # Start Button
        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet("background-color: #1A73E8; color: white; font-size: 16px; padding: 10px; border-radius: 8px;")
        self.start_button.clicked.connect(self.start_monitoring)
        main_layout.addWidget(self.start_button)

        # Stop Button
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet("background-color: #EA4335; color: white; font-size: 16px; padding: 10px; border-radius: 8px;")
        self.stop_button.clicked.connect(self.stop_monitoring)
        main_layout.addWidget(self.stop_button)

        # Console (Log Textbox)
        self.console_text = QTextEdit(self)
        self.console_text.setStyleSheet("background-color: #1C1C1C; color: white; font-size: 12px; padding: 10px; border-radius: 8px;")
        self.console_text.setReadOnly(True)
        main_layout.addWidget(self.console_text)

        # Command Input
        self.command_input = QLineEdit(self)
        self.command_input.setStyleSheet("background-color: #333333; color: white; font-size: 14px; padding: 10px; border-radius: 8px;")
        self.command_input.setPlaceholderText("Enter command...")
        main_layout.addWidget(self.command_input)

        # Setting main widget and layout
        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Set rounded corners for the window
        self.setStyleSheet("QMainWindow { border-radius: 15px; }")

    def minimize_to_tray(self):
        """Minimizes the application to the system tray."""
        self.hide()

    def restore_from_tray(self):
        """Restores the application from the tray."""
        self.show()

    def quit_application(self):
        """Closes the application."""
        QApplication.quit()

    def log_message(self, message):
        """Logs a message to the UI console."""
        self.console_text.append(f"{time.strftime('%H:%M:%S')} - {message}")

    def get_chrome_tabs(self):
        """Gets all Chrome windows and their associated URLs."""
        def enum_window_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if " - Google Chrome" in window_text:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    windows.append((hwnd, window_text, pid))
            return True

        windows = []
        win32gui.EnumWindows(enum_window_callback, windows)
        return windows

    def is_youtube_url(self, title):
        """Checks if the window title contains a YouTube video."""
        return "YouTube" in title and not "Picture in Picture" in title

    def get_active_youtube_window(self):
        """Finds an active YouTube window."""
        chrome_windows = self.get_chrome_tabs()
        foreground_hwnd = win32gui.GetForegroundWindow()
        
        for hwnd, title, pid in chrome_windows:
            if hwnd == foreground_hwnd and self.is_youtube_url(title):
                return hwnd, title
        return None, None

    def activate_pip(self):
        """Activates PiP mode on YouTube by pressing Alt + P."""
        try:
            # Ensure the YouTube window is active
            hwnd, title = self.get_active_youtube_window()
            if hwnd:
                # Check if PiP is already activated (based on window title)
                if "Picture in Picture" in title and not self.is_pip_active:
                    self.log_message("PiP mode is already active.")
                    return  # PiP is already active, do nothing
                
                # Set the window to foreground
                win32gui.SetForegroundWindow(hwnd)

                # Press the PiP shortcut (Alt + P)
                pyautogui.hotkey('alt', 'p')

                # Mark PiP as active
                self.is_pip_active = True
                self.log_message("PiP mode activated.")

            else:
                self.log_message("No active YouTube video detected.")

        except Exception as e:
            self.log_message(f"Error activating PiP: {str(e)}")

    def monitor_youtube(self):
        """Monitors for active YouTube videos."""
        while self.monitoring:
            try:
                hwnd, title = self.get_active_youtube_window()
                if hwnd:
                    if self.is_pip_active:
                        continue  # Skip activating PiP if it's already active
                    else:
                        self.activate_pip()
                        self.stop_monitoring()
                        break
            except Exception as e:
                self.log_message(f"Error during monitoring: {str(e)}")
            time.sleep(2)

    def start_monitoring(self):
        """Starts the monitoring process."""
        if not self.monitoring:
            self.monitoring = True
            self.thread = threading.Thread(target=self.monitor_youtube, daemon=True)
            self.thread.start()
            self.status_label.setText("Status: Monitoring...")
            self.log_message("Started monitoring")

    def stop_monitoring(self):
        """Stops the monitoring process."""
        self.monitoring = False
        self.is_pip_active = False  # Reset PiP flag when stopping
        self.status_label.setText("Status: Stopped")
        self.log_message("Stopped monitoring")
    
    def run(self):
        """Starts the application."""
        self.show()

    def closeEvent(self, event):
        """Overrides the close event to minimize the window to the tray instead of closing."""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("YouTube PiP Controller", "The app is running in the system tray.", QSystemTrayIcon.
        Information, 3000)
    
    def quit(self):
        """Exit the application."""
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = YouTubePiPController()
    controller.run()
    sys.exit(app.exec_())

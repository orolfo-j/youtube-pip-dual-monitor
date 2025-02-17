import time
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import win32gui
import win32con
import win32process
import win32api
import psutil
from urllib.parse import urlparse
import pyautogui
import ctypes

class YouTubePiPController:
    def __init__(self):
        self.monitoring = False
        self.setup_gui()
        self.user32 = ctypes.windll.user32
        
    def log_message(self, message):
        """Logs a message to the UI console."""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)
        print(message)

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

    def get_monitor_info(self):
        """Gets information about all connected monitors."""
        # Get primary monitor info
        primary_width = win32api.GetSystemMetrics(0)  # SM_CXSCREEN
        primary_height = win32api.GetSystemMetrics(1)  # SM_CYSCREEN
        
        # Get virtual screen info (all monitors)
        virtual_left = win32api.GetSystemMetrics(76)   # SM_XVIRTUALSCREEN
        virtual_top = win32api.GetSystemMetrics(77)    # SM_YVIRTUALSCREEN
        virtual_width = win32api.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
        virtual_height = win32api.GetSystemMetrics(79) # SM_CYVIRTUALSCREEN
        
        self.log_message(f"Primary monitor: {primary_width}x{primary_height}")
        self.log_message(f"Virtual screen: {virtual_width}x{virtual_height} at ({virtual_left},{virtual_top})")
        
        # Calculate second monitor position
        second_monitor_x = primary_width
        second_monitor_width = virtual_width - primary_width
        
        if second_monitor_width > 0:
            return {
                'primary': (0, 0, primary_width, primary_height),
                'secondary': (second_monitor_x, 0, second_monitor_x + second_monitor_width, virtual_height)
            }
        return None

    def find_pip_window(self):
        """Finds the Picture-in-Picture window."""
        def callback(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                self.log_message(f"Checking window: '{title}'")
                
                if title.lower() == 'picture in picture':
                    ctx.append((hwnd, title))
                    return False
            return True

        pip_windows = []
        win32gui.EnumWindows(callback, pip_windows)
        
        if pip_windows:
            self.log_message(f"Found PiP window: {pip_windows[0][1]}")
            return pip_windows[0][0]
        else:
            self.log_message("No PiP window found among visible windows")
            return None

    def force_window_foreground(self, hwnd):
        """Forces a window to the foreground."""
        # Get the current foreground window
        curr_fore = win32gui.GetForegroundWindow()
        
        # Get current thread ID
        curr_thread = win32api.GetCurrentThreadId()
        
        # Get thread ID of the window we want to bring to foreground
        window_thread = win32process.GetWindowThreadProcessId(hwnd)[0]
        
        # Attach the threads
        win32process.AttachThreadInput(window_thread, curr_thread, True)
        
        # Force the window to foreground
        win32gui.SetForegroundWindow(hwnd)
        win32gui.BringWindowToTop(hwnd)
        
        # Detach the threads
        win32process.AttachThreadInput(window_thread, curr_thread, False)

    def move_to_second_monitor(self, hwnd):
        """Moves and resizes PiP window to the second monitor."""
        monitors = self.get_monitor_info()
        if not monitors:
            self.log_message("Second monitor not detected")
            return False

        # Get second monitor dimensions
        second_monitor = monitors['secondary']
        monitor_x = second_monitor[0]
        monitor_width = second_monitor[2] - second_monitor[0]
        monitor_height = second_monitor[3] - second_monitor[1]

        # Calculate new window size (25% of monitor size)
        new_width = int(monitor_width * 0.25)
        new_height = int(monitor_height * 0.25)
        new_x = monitor_x + (monitor_width - new_width) // 2
        new_y = (monitor_height - new_height) // 2

        self.log_message(f"Moving window to: x={new_x}, y={new_y}, width={new_width}, height={new_height}")

        try:
            # Remove the window from the taskbar
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                                 style | win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_TOPMOST)

            # Move and resize the window
            flags = win32con.SWP_SHOWWINDOW | win32con.SWP_FRAMECHANGED
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                                new_x, new_y, new_width, new_height, flags)
            
            # Force the window to foreground
            self.force_window_foreground(hwnd)
            
            self.log_message("Successfully moved and resized window")
            return True
            
        except Exception as e:
            self.log_message(f"Error moving window: {str(e)}")
            return False

    def activate_pip(self):
        """Activates PiP mode and moves window to second monitor."""
        hwnd, title = self.get_active_youtube_window()
        if not hwnd:
            self.log_message("No active YouTube video detected")
            return False

        # Activate PiP mode
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'p')
        self.log_message("Activated PiP mode")

        # Wait longer for PiP window to appear and stabilize
        for attempt in range(5):
            self.log_message(f"Attempting to find PiP window (attempt {attempt + 1}/5)")
            time.sleep(1)
            pip_hwnd = self.find_pip_window()
            if pip_hwnd:
                if self.move_to_second_monitor(pip_hwnd):
                    self.log_message("Successfully moved PiP to second monitor")
                    return True
                break
        
        self.log_message("Failed to find PiP window after multiple attempts")
        return False

    def monitor_youtube(self):
        """Monitors for active YouTube videos."""
        while self.monitoring:
            try:
                hwnd, title = self.get_active_youtube_window()
                if hwnd:
                    if self.activate_pip():
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
            self.status_label.config(text="Status: Monitoring...")
            self.log_message("Started monitoring")

    def stop_monitoring(self):
        """Stops the monitoring process."""
        self.monitoring = False
        self.status_label.config(text="Status: Stopped")
        self.log_message("Stopped monitoring")

    def setup_gui(self):
        """Sets up the GUI interface."""
        self.root = tk.Tk()
        self.root.title("YouTube PiP Controller")
        self.root.geometry("800x600")

        self.status_label = tk.Label(self.root, text="Status: Stopped", font=("Arial", 12))
        self.status_label.pack(pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Start", font=("Arial", 12), 
                 command=self.start_monitoring).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Stop", font=("Arial", 12), 
                 command=self.stop_monitoring).pack(side=tk.LEFT, padx=5)

        self.console_text = ScrolledText(self.root, height=30, width=80, state=tk.DISABLED)
        self.console_text.pack(pady=10)

    def run(self):
        """Starts the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = YouTubePiPController()
    app.run()
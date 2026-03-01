import win32gui
import win32process
import win32con
import psutil

class ProcessBlock:
    def __init__(self, blocked_apps):
        self.blocked_apps = blocked_apps
    def minimize_pid(self, pid):
        def callback(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd):
                return
            _, window_proc_id = win32process.GetWindowThreadProcessId(hwnd)
            if window_proc_id == pid:
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        win32gui.EnumWindows(callback, None)
    def check_processes(self):
        count = 0
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                name = proc.info["name"].lower()
                pid = proc.info["pid"]

                if name in self.blocked_apps:
                    self.minimize_pid(pid)
                    count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return count
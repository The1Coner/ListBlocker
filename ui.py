import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pystray
from PIL import Image, ImageDraw
import threading
from config import load_block_list, save_block_list
from blocker import ProcessBlock

INTERVAL = 1000

class AppBlocker:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.blocked_apps = load_block_list()

        style = ttk.Style()
        style.configure("Big.TButton", font=("Arial", 34, "bold"), padding=10)
        style.configure("Status.TLabel", font=("Arial", 14))

        self.build_ui()
        self.setup_tray()
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)
        self.blocker = ProcessBlock(self.blocked_apps)
    # ui

    def build_ui(self):
        self.root.title("ListBlocker")
        self.root.geometry("360x220")
        self.root.minsize(360, 220)
        # self.root.resizable(False, False)
        frame = tk.Frame(self.root)
        frame.pack(expand=True, padx=30, pady=30)

        self.status_label = ttk.Label(frame, text="Stopped", style="Status.TLabel")
        self.status_label.pack(pady=5)
        self.toggle_btn = ttk.Button(
            frame,
            text="Start",
            command=self.toggle,
            style="Big.TButton"
        )
        self.toggle_btn.pack(pady=15, ipadx=40, ipady=15)
        self.config_btn = ttk.Button(
            self.root,
            text="Configure",
            command=self.open_config
        )
        self.config_btn.place(relx=1.0, rely=0.0, anchor="ne")

    def toggle(self):
        if self.running and not messagebox.askyesno("Confirm", "Stop blocker?"):
            return
        # if self.running:
        # self.minimized_pids.clear()
        self.running = not self.running

        if self.running:
            self.status_label.config(text="Running")
            self.toggle_btn.config(text="Stop")
            self.check_loop()
        else:
            self.status_label.config(text="Stopped")
            self.toggle_btn.config(text="Start")

    def check_loop(self):
        if not self.running:
            return

        count = self.blocker.check_processes()
        self.status_label.config(text=f"Running, blocked {count} processes")

        # schedule next check without freezing GUI
        self.root.after(INTERVAL, self.check_loop)

    def open_config(self):
        if hasattr(self, "config_window") and self.config_window.winfo_exists():
            self.config_window.deiconify()
            self.config_window.lift()
            self.config_window.focus_force()
            return

        self.config_window = tk.Toplevel(self.root)
        self.config_window.title("Configuration")
        self.config_window.geometry("400x300")
        listbox = tk.Listbox(self.config_window)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        for app in self.blocked_apps:
            listbox.insert("end", app)

        entry = tk.Entry(self.config_window)
        entry.pack(fill="x", padx=10, pady=(0, 5))

        def add_app():
            name = entry.get().strip()
            if not name:
                return

            if name.lower() not in self.blocked_apps:
                self.blocked_apps.append(name.lower())
            listbox.insert("end", name)
            entry.delete(0, "end")
            save_block_list(self.blocked_apps)

        def remove_selected():
            selection = listbox.curselection()
            if not selection:
                return

            index = selection[0]

            listbox.delete(index)
            self.blocked_apps.pop(index)
            save_block_list(self.blocked_apps)

        btn_frame = tk.Frame(self.config_window)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add", command=add_app).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Remove Selected", command=remove_selected).pack(side="left", padx=5)

    def create_tray_image(self):
        # simple square icon (no external file needed)
        img = Image.new("RGB", (64, 64), "black")
        d = ImageDraw.Draw(img)
        d.rectangle((16, 16, 48, 48), fill="white")
        return img

    def setup_tray(self):
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.tray_show),
            pystray.MenuItem("Start/Stop", self.tray_toggle),
            pystray.MenuItem("Quit", self.tray_quit),
        )

        self.tray_icon = pystray.Icon(
            "ListBlocker",
            self.create_tray_image(),
            "ListBlocker",
            menu
        )

        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def tray_show(self, icon=None, item=None):
        self.root.after(0, self.root.deiconify)
        self.root.after(0, self.root.lift)

    def tray_toggle(self, icon, item):
        self.root.after(0, self.toggle)

    def tray_quit(self, icon, item):
        icon.stop()
        self.root.after(0, self.root.destroy)
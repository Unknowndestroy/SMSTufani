import os
import sys
import urllib.request
import json
import subprocess
import requests
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import threading
import pythoncom
from win32com.client import Dispatch

# === YAPILANDIRMA AYARLARI ===
GITHUB_REPO = 'https://api.github.com/repos/Unknowndestroy/SMSTufani-Source/contents/'
BRANCH = 'main'
STARTUP_NAME = 'SMSTufani-Updater.lnk'

# === SİSTEM YOLLARI ===
script_path = os.path.abspath(sys.argv[0])
script_dir = os.path.dirname(script_path)
startup_dir = Path(os.getenv('APPDATA')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'


# === AKILLI GÜNCELLEYİCİ SINIFI ===
class AutoUpdater:
    def __init__(self):
        self.total_files = 0
        self.updated_files = 0
        self.running = True

    def fetch_file_list(self):
        try:
            with urllib.request.urlopen(f"{GITHUB_REPO}?ref={BRANCH}") as response:
                return json.load(response)
        except Exception as e:
            print(f"API hatası: {str(e)}")
            return []

    def compare_files(self, file):
        local_path = os.path.join(script_dir, file['name'])
        if not os.path.exists(local_path):
            return True
            
        with open(local_path, 'rb') as f:
            local_content = f.read()
            
        with urllib.request.urlopen(file['download_url']) as response:
            remote_content = response.read()
            
        return local_content != remote_content

    def download_file(self, file):
        try:
            local_path = os.path.join(script_dir, file['name'])
            with urllib.request.urlopen(file['download_url']) as response:
                with open(local_path, 'wb') as f:
                    f.write(response.read())
            return True
        except Exception as e:
            print(f"İndirme hatası: {str(e)}")
            return False

    def full_update(self, progress_callback, status_callback):
        try:
            files = self.fetch_file_list()
            self.total_files = len(files)
            
            for index, file in enumerate(files):
                if not self.running:
                    return False
                
                status_callback(f"{index+1}/{self.total_files} - {file['name']} kontrol ediliyor...")
                
                if self.compare_files(file):
                    status_callback(f"{file['name']} güncelleniyor...")
                    if self.download_file(file):
                        self.updated_files += 1
                
                progress = (index + 1) / self.total_files * 100
                progress_callback(progress)
            
            return True
            
        except Exception as e:
            status_callback(f"Kritik hata: {str(e)}")
            return False

# === GÜVENLİK ÖNLEMLERİ ===
def add_to_startup():
    try:
        shortcut_path = startup_dir / STARTUP_NAME
        if shortcut_path.exists():
            shortcut_path.unlink()
            
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.TargetPath = sys.executable
        shortcut.Arguments = f'"{script_path}"'
        shortcut.WorkingDirectory = script_dir
        shortcut.IconLocation = script_path
        shortcut.Description = "SMSTufani Otomatik Güncelleyici"
        shortcut.save()
    except Exception as e:
        print(f"Başlangıç hatası: {str(e)}")

# === GELİŞMİŞ GUI ===
class UpdateGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SMSTufani Güncelleyici")
        self.geometry("500x200")
        self.configure(bg="#1a1a1a")
        
        # Pencere kapatma kontrollerini devre dışı bırak
        self.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.resizable(False, False)
        
        # Özel stil ayarları
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TProgressbar", thickness=22, troughcolor="#333333", background="#4CAF50")
        self.style.configure("TLabel", background="#1a1a1a", foreground="white")
        
        # GUI bileşenleri
        self.create_widgets()
        
        # Güncelleme işlemini başlat
        self.after(100, self.start_update)

    def create_widgets(self):
        self.header = ttk.Label(self, text="SMSTufani Otomatik Güncelleme", font=("Arial", 14, "bold"))
        self.status_label = ttk.Label(self, text="Sistem hazırlanıyor...")
        self.progress_bar = ttk.Progressbar(self, length=450, mode="determinate")
        
        self.header.pack(pady=15)
        self.status_label.pack(pady=5)
        self.progress_bar.pack(pady=10)

    def disable_close(self):
        pass

    def start_update(self):
        self.updater = AutoUpdater()
        self.thread = threading.Thread(target=self.run_update, daemon=True)
        self.thread.start()
        self.monitor_progress()

    def run_update(self):
        add_to_startup()
        success = self.updater.full_update(
            self.update_progress,
            self.update_status
        )
        
        if success:
            self.after(2000, self.complete_update)
        else:
            self.after(2000, self.destroy)

    def monitor_progress(self):
        if self.thread.is_alive():
            self.after(100, self.monitor_progress)
        else:
            self.after(1000, self.destroy)

    def update_progress(self, value):
        self.progress_bar['value'] = value

    def update_status(self, message):
        self.status_label.config(text=message)
        self.update_idletasks()

    def complete_update(self):
        self.destroy()
        start_main()


# nah man im lazy i made this via chatgpt lol
def add_to_path(directory):
    if directory not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + directory

def add_python_and_pip_to_path():
    python_dir = os.path.dirname(sys.executable)
    scripts_dir = os.path.join(python_dir, 'Scripts')
    
    # Python ve Scripts dizinlerini PATH'e ekle
    add_to_path(python_dir)
    add_to_path(scripts_dir)

    # PATH'i güncelle
    new_path = os.environ["PATH"]
    os.system(f'setx PATH "{new_path}"')

def clear_redundant_paths():
    # PATH değişkenini al
    path = os.environ["PATH"]
    # PATH'teki tekrar eden dizinleri kaldır
    path_list = list(dict.fromkeys(path.split(os.pathsep)))
    # Yeni PATH değeri oluştur
    new_path = os.pathsep.join(path_list)
    os.system(f'setx PATH "{new_path}"')

# === ANA UYGULAMAYI BAŞLAT ===
def start_main():
    main_path = os.path.join(script_dir, 'main.pyw')
    if os.path.exists(main_path):
        subprocess.Popen([sys.executable, main_path], creationflags=subprocess.CREATE_NO_WINDOW)
    os._exit(0)

if __name__ == "__main__":
    add_python_and_pip_to_path()
    clear_redundant_paths()
    app = UpdateGUI()
    app.mainloop()






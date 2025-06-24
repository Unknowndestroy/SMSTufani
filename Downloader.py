import os
import sys
import urllib.request
import json
import subprocess
import threading
from pathlib import Path

REQUIRED = {
    'requests': 'requests',
    'urllib3': 'urllib3',
    'six': 'six',
    'colorama': 'colorama',
    'keyboard': 'keyboard'
}

def ensure_modules():
    print('[DEBUG] Modül kontrolü başlıyor...')
    for mod, pkg in REQUIRED.items():
        print(f'[DEBUG] {mod} kontrol ediliyor')
        try:
            __import__(mod)
            print(f'[OK] {mod} yüklü')
        except ImportError:
            print(f'[INFO] {mod} eksik, yükleniyor: pip install {pkg}')
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
            print(f'[OK] {mod} yüklendi')

ensure_modules()

import requests
import colorama
import keyboard
from colorama import Fore

colorama.init(autoreset=True)

def log(msg, level='INFO'):
    print(f'[{level}] {msg}')

github_repo = 'https://api.github.com/repos/UnknownDestroyer2/SMS-Source/contents/'
branch = 'main'
shortcut_name = 'SMS.lnk'

script_path = os.path.abspath(sys.argv[0])
base_dir = os.path.dirname(script_path)
startup_dir = Path(os.getenv('APPDATA')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'

log(f'Script konumu: {script_path}', 'DEBUG')
log(f'Startup dizini: {startup_dir}', 'DEBUG')

class AutoUpdater:
    def fetch_file_list(self):
        log('Dosya listesi alınıyor...', 'DEBUG')
        try:
            with urllib.request.urlopen(f"{github_repo}?ref={branch}") as resp:
                data = json.load(resp)
            log(f'{len(data)} dosya bulundu', 'OK')
            return data
        except Exception as e:
            log(f'API hatası: {e}', 'ERROR')
            return []

    def compare_and_download(self, file):
        name = file['name']
        local = Path(base_dir) / name
        need = True
        if local.exists():
            local_content = local.read_bytes()
            try:
                remote_content = urllib.request.urlopen(file['download_url']).read()
                need = local_content != remote_content
            except Exception as e:
                log(f'{name} indirme hatası: {e}', 'ERROR')
                return False
        if need:
            log(f'{name} indiriliyor...', 'INFO')
            try:
                data = urllib.request.urlopen(file['download_url']).read()
                local.write_bytes(data)
                log(f'{name} güncellendi', 'OK')
                return True
            except Exception as e:
                log(f'{name} indirme hatası: {e}', 'ERROR')
        else:
            log(f'{name} zaten güncel', 'DEBUG')
        return False

    def run(self):
        updated = sum(1 for f in self.fetch_file_list() if self.compare_and_download(f))
        log(f'Güncellenen dosya: {updated}', 'OK')

def add_to_startup():
    log('Kısayol oluşturuluyor...', 'DEBUG')
    try:
        pythonw = sys.executable.replace('python.exe', 'pythonw.exe') if sys.executable.lower().endswith('python.exe') else sys.executable
        sc = startup_dir / shortcut_name
        sc.unlink(missing_ok=True)
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        link = shell.CreateShortcut(str(sc))
        link.TargetPath = pythonw
        link.Arguments = f'"{script_path}"'
        link.WorkingDirectory = base_dir
        link.Description = 'SMS Ink'
        link.Save()
        log('Kısayol eklendi', 'OK')
    except Exception as e:
        log(f'Kısayol hatası: {e}', 'ERROR')

def update_path():
    log('PATH güncelleniyor...', 'DEBUG')
    dirs = {os.path.dirname(sys.executable), os.path.join(os.path.dirname(sys.executable), 'Scripts')}
    new_path = os.pathsep.join(dirs.union(os.environ['PATH'].split(os.pathsep)))
    subprocess.run(['setx', 'PATH', new_path], shell=True)
    log('PATH güncellendi', 'OK')

def enable_console_hotkey():
    log('Ctrl+F1 ayarlanıyor...', 'DEBUG')
    def open_console():
        cmd = f'cmd /k echo SMS && cd /d "{base_dir}"'
        subprocess.Popen(['cmd', '/c', 'start', cmd], shell=True)
    keyboard.add_hotkey('ctrl+f1', open_console)
    log('Hotkey: Ctrl+F1', 'OK')

if __name__ == '__main__':
    add_to_startup()
    update_path()
    enable_console_hotkey()
    AutoUpdater().run()

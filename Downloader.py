# Licensed under Unknown Destroyer Limited Personal Use License (UDLPL-v1.0)
import os
import sys
import urllib.request
import json
import subprocess
import threading
from pathlib import Path

# Copyright (c) 2025 Unknown Destroyer
# UDLPL-v1.0
# Permission is hereby granted, free of charge, to any person or entity obtaining a copy of this Software and any associated documentation, files, materials, source code, binaries, scripts, or related components (collectively referred to herein as the "Software"), to use, copy, and modify the Software solely and exclusively for personal, private, non-commercial, and non-distributive purposes, subject to the conditions and limitations detailed in this license agreement.
# 1. LICENSE GRANT AND SCOPE OF USE
# 1.1. The User is expressly permitted to install, execute, run, analyze, and modify the Software in any manner strictly confined to personal, private use. This license does not extend any rights or permissions beyond such usage.
# 1.2. Use of the Software for any commercial enterprise, profit-generating activity, service provision, rental, sale, sublicensing, or any financial gain derived directly or indirectly from the Software is strictly prohibited.
# 1.3. The User acknowledges and agrees that this license is non-transferable and non-sublicensable. Any attempt to transfer, sublicense, lease, or otherwise assign rights granted under this license is void and constitutes a breach of contract.
# 2. DISTRIBUTION AND SHARING RESTRICTIONS
# 2.1. The original, unmodified versions of the Software may be shared, copied, distributed, or published without restriction, provided the full copyright and license notices remain intact and unaltered.
# 2.2. Distribution, publication, sharing, or public posting of any modified, altered, adapted, or derivative versions of the Software is strictly forbidden under all circumstances, regardless of format, medium, or platform, including but not limited to public or private repositories, websites, social media, file-sharing services, peer-to-peer networks, or physical media.
# 2.3. Users must not, under any condition, circumvent or attempt to circumvent the restrictions established in this license by employing obfuscation, code encryption, or any form of disguise to share modified versions of the Software.
# 3. INTELLECTUAL PROPERTY AND OWNERSHIP
# 3.1. The Software and all copies thereof remain the sole and exclusive intellectual property of Unknown Destroyer.
# 3.2. No rights, titles, or interests in or to the Software are transferred to the User by virtue of this license, except for the limited rights explicitly granted herein.
# 3.3. The User shall preserve all copyright, trademark, patent, and other proprietary notices contained in or on the Software in any copies made.
# 3.4. The User agrees not to remove, obscure, or alter any copyright or license notices or proprietary legends included in the Software.
# 4. MODIFICATION CLAUSE
# 4.1. Modification of the Software is permitted strictly for personal, private use only.
# 4.2. The User agrees that any modifications, enhancements, adaptations, or derivative works created from the Software shall remain private and shall not be distributed, shared, published, or otherwise made available to any third party in any form.
# 4.3. The User understands and accepts full responsibility for any consequences arising from modifications made to the Software and waives any claim against the original author.
# 5. WARRANTY AND LIABILITY DISCLAIMER
# 5.1. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT ANY WARRANTY WHATSOEVER, WHETHER EXPRESS, IMPLIED, STATUTORY, OR OTHERWISE, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, OR ACCURACY.
# 5.2. UNKNOWN DESTROYER SHALL NOT BE LIABLE FOR ANY DAMAGES, LOSS OF DATA, LOSS OF PROFITS, INTERRUPTION OF BUSINESS, OR ANY OTHER DIRECT, INDIRECT, INCIDENTAL, CONSEQUENTIAL, OR EXEMPLARY DAMAGES ARISING OUT OF OR RELATED TO THE USE OR INABILITY TO USE THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
# 6. TERMINATION
# 6.1. This license and all rights granted hereunder shall terminate immediately without notice if the User breaches any term or condition of this license.
# 6.2. Upon termination, the User agrees to immediately cease all use of the Software and to delete or destroy all copies, including any modifications or derivative works, in the User's possession, custody, or control.
# 6.3. Termination of this license shall not limit any other rights or remedies that the original author may have under applicable law.
# 7. MISCELLANEOUS
# 7.1. This license constitutes the entire agreement between the User and Unknown Destroyer with respect to the Software and supersedes all prior agreements, understandings, and communications.
# 7.2. If any provision of this license is held to be invalid, illegal, or unenforceable, the remaining provisions shall continue in full force and effect.
# 7.3. The failure of Unknown Destroyer to enforce any right or provision of this license shall not constitute a waiver of such right or provision.
# ---
# This license grants you permission to use and modify the Software **only for your personal, non-commercial use.** You are allowed to share and distribute **only the original, unmodified versions.** Any sharing, distribution, or publication of modified versions is strictly prohibited. Commercial use of the Software in any form is not allowed. The Software is provided as-is without any warranty. Breach of any term will result in immediate termination of your license rights.  
# By using, copying, or modifying this Software, you agree to all terms outlined herein.


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

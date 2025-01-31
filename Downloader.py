import os
import requests
import sys

def add_to_path(directory):
    if directory not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + directory

def add_python_and_pip_to_path():
    python_dir = os.path.dirname(sys.executable)
    scripts_dir = os.path.join(python_dir, 'Scripts')
    
    # Add Python and Scripts directories to PATH
    add_to_path(python_dir)
    add_to_path(scripts_dir)

    # Update PATH using os.system command
    new_path = os.environ["PATH"]
    os.system(f'setx PATH "{new_path}"')

def clear_redundant_paths():
    # Get the PATH variable
    path = os.environ["PATH"]
    # Remove duplicate directories in PATH
    path_list = list(dict.fromkeys(path.split(os.pathsep)))
    # Create the new PATH value
    new_path = os.pathsep.join(path_list)
    os.system(f'setx PATH "{new_path}"')

def download_files(files):
    for file_name, url in files.items():
        print(f"{file_name} indiriliyor...")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            with open(file_name, "wb") as file:
                file.write(response.content)
            print(f"{file_name} başarıyla indirildi.")
        except requests.exceptions.RequestException as e:
            print(f"Hata: {file_name} indirilemedi. Hata mesajı: {e}")

# GitHub'dan indirilecek dosyalar
files_to_download = {
    "main.pyw": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/main.pyw",
    "main1.pyw": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/main1.pyw",
    "main2.pyw": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/main2.pyw",
    "sms.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/sms.py",
    "smsen.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smsen.py",
    "smsenhided.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smsenhided.py",
    "smstr.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstr.py",
    "smstrhided.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstrhided.py",
    "smstufanien.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanien.py",
    "smstufanienhided.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanienhided.py",
    "smstufanienhidedanim.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanienhidedanim.py",
    "smstufanienhidedskip.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanienhidedskip.py",
    "smstufanienhidedskipanim.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanienhidedskipanim.py",
    "smstufanienskipanim.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanienskipanim.py",
    "smstufanitr.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanitr.py",
    "smstufanitranim.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanitranim.py",
    "smstufanitrhided.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanitrhided.py",
    "smstufanitrhidedanim.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanitrhidedanim.py",
    "smstufanitrhidedskip.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanitrhidedskip.py",
    "smstufanitrhidedskipanim.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanitrhidedskipanim.py",
    "smstufanitrskip.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanitrskip.py",
    "smstufanitrskipanim.py": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/smstufanitrskipanim.py",
    "Req.bat": "https://raw.githubusercontent.com/Unknowndestroy/SMSTufani-Source/main/Req.bat",
}

# Ana işlem
if __name__ == "__main__":
    add_python_and_pip_to_path()
    clear_redundant_paths()
    print("Python ve Pip PATH'e eklendi ve tekrar eden dizinler temizlendi.")
    download_files(files_to_download)
    print("Tüm dosyalar indirildi!")
    os.startfile("Req.bat")
    print("Gereksinimler indiriliyor.")

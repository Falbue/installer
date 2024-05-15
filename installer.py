version = 'v1.0'
repository = "Falbue/installer"

import requests
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style  # Библиотека для темного режима и современных стилей
from tkinter import messagebox  # Для всплывающих окон с подтверждением
import winreg
import webbrowser

def latest_version(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        release_info = response.json()
        version = release_info['tag_name']
        print(f"Последняя версия {repo}: {version}")
    else:
        print(f"Версия не найдена")
        version = '0'

    return version

latest_version = latest_version(repository)
print(f"Текущая версия: {version}")

if version == str(latest_version):
    print("Последняя верия")

else:
    def get_windows_theme():
        key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
                theme = winreg.QueryValueEx(reg_key, 'AppsUseLightTheme')[0]
                return 'Light' if theme == 1 else 'Dark'
        except FileNotFoundError:
            return None

    def download():
        webbrowser.open('https://github.com/Falbue/installer/releases')

    def main():
        root = tk.Tk()
        root.title("Загрузчик")
        root.geometry("300x100")
        root.resizable(False, False)  # Фиксируем размер окна
        root.iconbitmap("lib/icon.ico")
    
        windows_theme = get_windows_theme()
        if windows_theme == 'Light':
            style = Style(theme="lumen")
        if windows_theme == 'Dark':
            style = Style(theme="darkly")
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 16))
        style.configure('TCheckbutton', font=('Helvetica', 10))

        label = ttk.Label(root, text="Найдена новая версия!")
        label.pack(pady='5')

        buttons = ttk.Frame(root, width=400)
        buttons.pack(pady=10)
    
        # Кнопка "Скачать"
        download_button = ttk.Button(buttons, text="Скачать", command=download)
        close_button = ttk.Button(buttons, text="Закрыть", command=root.destroy)
        download_button.pack(side="left", padx=10)
        close_button.pack(side="right", padx=10)
        
    
        root.mainloop()

    if __name__ == "__main__":
        main()



# import main
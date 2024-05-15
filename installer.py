version = 'v1.0'
git_nick = "Falbue"
repo_name = 'installer'
repository = f"{git_nick}/{repo_name}"

import requests
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style  # Библиотека для темного режима и современных стилей
from tkinter import messagebox  # Для всплывающих окон с подтверждением
import winreg
import webbrowser
import os
import sys

user_folder = os.path.expanduser('~')  # Получаем путь к папке пользователя
install_path = os.path.join(user_folder, 'Falbue')
folder_path = os.path.join(install_path, repo_name)


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
    if os.path.exists(folder_path):
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

    else:
        def create_folder(folder_name):
            user_folder = os.path.expanduser('~')  # Получаем путь к папке пользователя
            install_path = os.path.join(user_folder, 'Falbue')
            # Создаем папку для сохранения файлов на рабочем столе.
            folder_path = os.path.join(install_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            return folder_path

        def download_files_from_github(app, folder_path):
            def download_file(file_url, file_name): 
                with open(file_name, 'wb') as f:
                    f.write(requests.get(file_url).content)
                print(f"Загрузка: {file_name}")
        
            def download_files_from_github_in_dir(dir_name, dir_path): 
                api_url = f"https://api.github.com/repos/{git_nick}/{app}/contents/{dir_name}"
                response = requests.get(api_url)
                files_in_dir = response.json()
                
                for file_in_dir in files_in_dir:
                    if file_in_dir['type'] == 'file': 
                        file_path = os.path.join(dir_path, file_in_dir['name'])
                        download_file(file_in_dir['download_url'], file_path)
        
            api_url = f"https://api.github.com/repos/{git_nick}/{app}/contents"
            response = requests.get(api_url)
            files = response.json()
            
            for file in files:
                file_path = os.path.join(folder_path, file['name'])
                if file['type'] == 'file': 
                    download_file(file['download_url'], file_path)
                elif file['type'] == 'dir': 
                    os.makedirs(file_path, exist_ok=True)
                    download_files_from_github_in_dir(file['path'], file_path)
        
        folder_path = create_folder(repo_name)
        download_files_from_github(repo_name, folder_path)
        sys.path.append(folder_path)
        import main

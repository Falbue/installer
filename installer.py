version = 'v1.0'
git_nick = "Falbue"
repo_name = 'installer'
repository = f"{git_nick}/{repo_name}"
app = 'Dynamics-Theme'

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
app_path = os.path.join(install_path, app)


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


if version == str(latest_version):
    print("Последняя верия")

else:
    print(f"Последняя найденная верия: {str(latest_version)}")
    if os.path.exists(folder_path):
        print("Установщик уже есть!")

    else:
        folder_path = create_folder(repo_name)

        file_name = "confinst.flb"
        file_path = os.path.join(folder_path, file_name)
        
        # Создание файла и запись текста в него
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(app)
        
        sys.path.append(folder_path)
    download_files_from_github(repo_name, folder_path)
import code
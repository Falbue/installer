app = 'ChenkAI' # название приложения.

import os
import requests

def create_folder_on_desktop(folder_name): # Получаем путь к рабочему столу пользователя.
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    # Создаем папку для сохранения файлов на рабочем столе.
    folder_path = os.path.join(desktop_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def download_files_from_github(app, folder_path):
    def download_file(file_url, file_name): # Функция для загрузки файла по его URL.
        with open(file_name, 'wb') as f:
            f.write(requests.get(file_url).content)
        print(f"Загрузка: {file_name}")

    def download_files_from_github_in_dir(dir_name, dir_path): # Функция для загрузки файлов из указанной директории на GitHub.
        api_url = f"https://api.github.com/repos/Falbue/{app}/contents/{dir_name}"
        response = requests.get(api_url)
        files_in_dir = response.json()
        
        for file_in_dir in files_in_dir:
            if file_in_dir['type'] == 'file': # Если файл, загружаем его.
                file_path = os.path.join(dir_path, file_in_dir['name'])
                download_file(file_in_dir['download_url'], file_path)
            elif file_in_dir['type'] == 'dir': # Если директория, создаем ее и загружаем файлы из нее.
                subdir_path = os.path.join(dir_path, file_in_dir['name'])
                os.makedirs(subdir_path, exist_ok=True)
                download_files_from_github_in_dir(file_in_dir['path'], subdir_path)

    # Получаем содержимое корневой директории репозитория на GitHub.
    api_url = f"https://api.github.com/repos/Falbue/{app}/contents"
    response = requests.get(api_url)
    files = response.json()
    
    # Перебираем файлы и директории в корневой директории.
    for file in files:
        file_path = os.path.join(folder_path, file['name'])
        if file['type'] == 'file': # Если файл, загружаем его.
            download_file(file['download_url'], file_path)
        elif file['type'] == 'dir': # Если директория, создаем ее и загружаем файлы из нее.
            os.makedirs(file_path, exist_ok=True)
            download_files_from_github_in_dir(file['path'], file_path)

if __name__ == "__main__": # Основная часть программы: создание папки и загрузка файлов.
    folder_name = app
    folder_path = create_folder_on_desktop(folder_name)
    download_files_from_github(app, folder_path)

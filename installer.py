app = 'Dynamics-Theme' # название приложения.

import os
import requests

def create_folder(folder_name): # Получаем путь к рабочему столу пользователя.
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    # Создаем папку для сохранения файлов на рабочем столе.
    folder_path = os.path.join(desktop_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def download_files_from_github(app, folder_path):
    def download_file(file_url, file_name): 
        with open(file_name, 'wb') as f:
            f.write(requests.get(file_url).content)
        print(f"Загрузка: {file_name}")

    def download_files_from_github_in_dir(dir_name, dir_path): 
        api_url = f"https://api.github.com/repos/Falbue/{app}/contents/{dir_name}"
        response = requests.get(api_url)
        files_in_dir = response.json()
        
        for file_in_dir in files_in_dir:
            if file_in_dir['type'] == 'file': 
                file_path = os.path.join(dir_path, file_in_dir['name'])
                download_file(file_in_dir['download_url'], file_path)

    api_url = f"https://api.github.com/repos/Falbue/{app}/contents"
    response = requests.get(api_url)
    files = response.json()
    
    for file in files:
        file_path = os.path.join(folder_path, file['name'])
        if file['type'] == 'file': 
            download_file(file['download_url'], file_path)
        elif file['type'] == 'dir': 
            os.makedirs(file_path, exist_ok=True)
            download_files_from_github_in_dir(file['path'], file_path)

    # Загрузка файла run.exe из другого репозитория 'installer'
    installer_api_url = "https://api.github.com/repos/Falbue/installer/contents"
    installer_response = requests.get(installer_api_url)
    installer_files = installer_response.json()

    for installer_file in installer_files:
        if installer_file['name'] == 'run.exe':
            installer_file_path = os.path.join(folder_path, installer_file['name'])
            download_file(installer_file['download_url'], installer_file_path)

if __name__ == "__main__": 
    folder_name = app
    folder_path = create_folder(folder_name)
    download_files_from_github(app, folder_path)

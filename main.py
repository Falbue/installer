github_api = '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'

import os
import requests

# Название репозитория на GitHub
app = 'ChenkAI'

def create_folder_on_desktop(folder_name):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    folder_path = os.path.join(desktop_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def download_files_from_github(app, folder_path):
    def download_file(file_url, file_name):
        with open(file_name, 'wb') as f:
            f.write(requests.get(file_url).content)
        print(f"Downloaded: {file_name}")

    def download_files_from_github_in_dir(dir_name, dir_path):
        api_url = f"https://api.github.com/repos/Falbue/{app}/contents/{dir_name}"
        response = requests.get(api_url)
        files = response.json()
        
        for file in files:
            file_path = os.path.join(dir_path, file['name'])
            if file['type'] == 'file':
                download_file(file['download_url'], file_path)
            elif file['type'] == 'dir':
                os.makedirs(file_path, exist_ok=True)
                download_files_from_github_in_dir(file['name'], file_path)

    api_url = f"https://api.github.com/repos/Falbue/{app}/contents"
    response = requests.get(api_url)
    files = response.json()
    
    for file in files:
        file_path = os.path.join(folder_path, file['name'])
        if file['type'] == 'file':
            download_file(file['download_url'], file_path)
        elif file['type'] == 'dir':
            os.makedirs(file_path, exist_ok=True)
            download_files_from_github_in_dir(file['name'], file_path)

if __name__ == "__main__":
    folder_name = app
    folder_path = create_folder_on_desktop(folder_name)
    download_files_from_github(app, folder_path)

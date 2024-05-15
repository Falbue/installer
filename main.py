version = "1.0"

import threading
import os
import requests
import winshell  # библиотека для работы с ярлыками на Windows
import pythoncom  # для инициализации COM в потоках
import threading
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style  # Библиотека для темного режима и современных стилей
from tkinter import messagebox  # Для всплывающих окон с подтверждением
import winreg

with open('confinst.flb', 'r', encoding='utf-8') as file:
    app = file.read()

# логика
def start_download(app, folder_name, progress, progress_label, download_frame, control_frame, create_desktop_shortcut, create_start_menu_shortcut):
    folder_path = create_folder(folder_name)
    threading.Thread(target=download_files_from_github, args=(
        app, folder_path, progress, progress_label, download_frame, control_frame, create_desktop_shortcut, create_start_menu_shortcut)).start()

def create_folder(folder_name):
    user_folder = os.path.expanduser('~')  # Получаем путь к папке пользователя
    install_path = os.path.join(user_folder, 'Falbue')
    # Создаем папку для сохранения файлов на рабочем столе.
    folder_path = os.path.join(install_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def download_files_from_github(app, folder_path, progress, progress_label, download_frame, control_frame, create_desktop_shortcut, create_start_menu_shortcut):
    pythoncom.CoInitialize()  # Инициализация COM в потоке
    try:
        def download_file(file_url, file_name):
            response = requests.get(file_url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                with open(file_name, 'wb') as f:
                    f.write(response.content)
            else:
                total_length = int(total_length)
                with open(file_name, 'wb') as f:
                    for data in response.iter_content(chunk_size=4096):
                        f.write(data)
                        progress.step(4096 / total_length * 100)

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

        total_files = len(files)
        progress["maximum"] = total_files
        for i, file in enumerate(files):
            file_path = os.path.join(folder_path, file['name'])
            if file['type'] == 'file':
                download_file(file['download_url'], file_path)
            elif file['type'] == 'dir':
                os.makedirs(file_path, exist_ok=True)
                download_files_from_github_in_dir(file['path'], file_path)
            progress_label.config(text=f"Загрузка: {file['name']} ({i+1}/{total_files})")
            progress.step(1)

        progress_label.config(text="Загрузка завершена!")

        # Создание ярлыков, если выбраны соответствующие чекбоксы
        target = os.path.join(folder_path, 'main.py')  # Укажите путь к основному файлу вашего приложения
        icon_path = os.path.join(f"{folder_path}/lib", 'ico.ico')  # Укажите путь к вашему файлу иконки
        if create_desktop_shortcut:
            create_shortcut(target, app, winshell.desktop(), icon_path)
        if create_start_menu_shortcut:
            create_shortcut(target, app, winshell.start_menu(), icon_path)

        download_frame.pack_forget()  # Скрываем текущий фрейм с загрузкой
        control_frame.pack(pady=20)  # Показываем новый фрейм с кнопками
    finally:
        pythoncom.CoUninitialize()  # Деинициализация COM в потоке

def create_shortcut(target, link_name, link_path, icon_path=None):
    shortcut_path = os.path.join(link_path, link_name + '.lnk')
    with winshell.shortcut(shortcut_path) as link:
        link.path = target
        link.working_directory = os.path.dirname(target)
        link.description = link_name
        if icon_path:
            link.icon_location = (icon_path, 0)


# дизайн
def get_windows_theme():
    key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
            theme = winreg.QueryValueEx(reg_key, 'AppsUseLightTheme')[0]
            return 'Light' if theme == 1 else 'Dark'
    except FileNotFoundError:
        return None

def main():
    root = tk.Tk()
    root.title("Загрузчик")
    root.geometry("350x250")
    root.resizable(False, False)  # Фиксируем размер окна
    root.iconbitmap("lib/icon.ico")

    windows_theme = get_windows_theme()
    if windows_theme == 'Light':
        style = Style(theme="lumen")  # Применение темы "darkly" для темного режима
    if windows_theme == 'Dark':
        style = Style(theme="darkly")  # Применение темы "darkly" для темного режима
    style.configure('TButton', font=('Helvetica', 10))
    style.configure('TLabel', font=('Helvetica', 10))
    style.configure('TCheckbutton', font=('Helvetica', 10))

    download_frame = ttk.Frame(root, padding="10 10 10 10")
    download_frame.pack(pady=20)

    progress = ttk.Progressbar(download_frame, orient="horizontal", length=300, mode="determinate")
    progress.grid(column=0, row=0, pady=10)

    progress_label = ttk.Label(download_frame, text="Ожидание...")
    progress_label.grid(column=0, row=1, pady=10)

    create_desktop_shortcut_var = tk.BooleanVar()
    create_start_menu_shortcut_var = tk.BooleanVar()

    desktop_shortcut_checkbox = ttk.Checkbutton(download_frame, text="Создать ярлык на рабочем столе", variable=create_desktop_shortcut_var)
    desktop_shortcut_checkbox.grid(column=0, row=2, pady=5)

    start_menu_shortcut_checkbox = ttk.Checkbutton(download_frame, text="Создать ярлык в меню Пуск", variable=create_start_menu_shortcut_var)
    start_menu_shortcut_checkbox.grid(column=0, row=3, pady=5)

    download_button = ttk.Button(download_frame, text="Начать загрузку", command=lambda: start_download(
        app, app, progress, progress_label, download_frame, control_frame, create_desktop_shortcut_var.get(), create_start_menu_shortcut_var.get()))
    download_button.grid(column=0, row=4, pady=10)

    control_frame = ttk.Frame(root, padding="10 10 10 10")

    close_button = ttk.Button(control_frame, text="Закрыть", command=root.destroy)
    close_button.grid(column=0, row=0, padx=5)

    def launch_app():
        print("Запуск приложения")
        messagebox.showinfo("Информация", "Приложение успешно запущено!")
        # Здесь вы можете добавить код для запуска вашего приложения

    launch_button = ttk.Button(control_frame, text="Запустить", command=launch_app)
    launch_button.grid(column=1, row=0, padx=5)

    # Добавление всплывающих подсказок
    tooltip = ttk.Label(download_frame, text="Совет: Убедитесь, что у вас есть интернет соединение для загрузки файлов.", wraplength=300)
    tooltip.grid(column=0, row=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

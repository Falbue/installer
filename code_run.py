import subprocess
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os

def run_code():
    try:
        # Запуск кода из файла code.py с помощью интерпретатора Python
        process = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding='utf-8')
        
        # Считывание вывода в реальном времени
        for line in process.stdout:
            print(line, end="")
        
        for line in process.stderr:
            print(line, end="")
        
        # Дожидаемся завершения процесса
        process.wait()
        os._exit(0)
    except FileNotFoundError:
        print("Файл main.py не найден.")
    except Exception as e:
        print("Произошла ошибка при выполнении кода:", e)

def stop_program(icon, item):
    icon.stop()
    os._exit(0)

def main():
    # Создаем иконку в трее
    try:
        image = Image.open("ico.ico")
    except:
        image = Image.open("lib/ico.ico")
    menu = (item('Закрыть', stop_program),)
    with open('README.md', 'r', encoding='utf-8') as file:
        head = file.readline()
        head = head.replace("# ", '')
    icon = pystray.Icon("name", image, head, menu)
    icon.run()

if __name__ == "__main__":
    thread = threading.Thread(target=run_code)
    thread.start()
    main()

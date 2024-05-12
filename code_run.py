import subprocess

def run_code():
    try:
        # Запуск кода из файла code.py с помощью интерпретатора Python
        subprocess.run(["python", "code.py"])
    except FileNotFoundError:
        print("Файл code.py не найден.")
    except Exception as e:
        print("Произошла ошибка при выполнении кода:", e)

if __name__ == "__main__":
    run_code()

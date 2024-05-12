import subprocess

# Задайте команду, которую вы хотите выполнить
command = 'pyinstaller --noconfirm --onefile --windowed --icon "D:/coding/code/python/Dynamics-Theme/lib/ico.ico" --name "Dynamics Theme"  "D:/coding/code/python/Dynamics-Theme/main.py"'

# Выполните команду и получите вывод
output = subprocess.run(command, shell=True, capture_output=True, text=True)

# Выведите результат
print("Output:", output.stdout)

#!/usr/bin/env python3.10
import subprocess

# Замініть 'make.bat' та 'html' на ваші фактичні ім'я пакетного скрипта та аргументи
шлях_скрипта = r'.\make.bat'
аргумент = 'html'

try:
    subprocess.run([шлях_скрипта, аргумент], check=True, shell=True)
except subprocess.CalledProcessError as e:
    print(f"Помилка під час виконання скрипта: {e}")

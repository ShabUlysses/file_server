import hashlib
import os
from flask import request, send_file

STORAGE_DIR = 'store'


def generate_file_hash(file):
    # Создаем объект для рассчета хэша
    hasher = hashlib.sha256()

    # Открываем файл в режиме чтения бинарного файла
    with open(file, 'rb') as file:
        # Читаем файл по частям и обновляем хэш
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    # Получаем хэш сумму файла
    return hasher.hexdigest()


def save_file(file, file_hash):
    # Создание каталога, если он не существует
    directory = os.path.join(STORAGE_DIR, file_hash[:2])
    os.makedirs(directory, exist_ok=True)

    # Сохранение файла на диск
    file_path = os.path.join(directory, file_hash)
    file.save(file_path)


def find_file_by_hash(file_hash):
    # Поиск файла по хешу
    file_path = os.path.join(STORAGE_DIR, file_hash[:2], file_hash)
    if os.path.exists(file_path):
        return file_path


def delete_file_by_hash(file_hash, username):
    # Удаление файла, если он существует и принадлежит пользователю
    file_path = os.path.join(STORAGE_DIR, file_hash[:2], file_hash)
    if os.path.exists(file_path):
        # Проверка принадлежности файла пользователю
        # Ваша реализация проверки принадлежности файла пользователю

        if file_belongs_to_user(file_path, username):
            os.remove(file_path)
            return True

    return False

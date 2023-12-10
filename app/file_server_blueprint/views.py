import hashlib
import os

from flask import request, send_file

from . import file_server_blueprint
from .auth import auth_required
from .models import User, File
from .. import db

STORAGE_DIR = 'store'


@file_server_blueprint.route('/upload', methods=['POST'])
@auth_required
def upload_file():
    # Проверяем, что в запросе есть файлы
    if 'file' not in request.files:
        return 'File was not transmitted', 400

    file = request.files['file']
    if file.filename == '':
        return 'Filename is empty', 400

    file_hash = hashlib.sha256(file.read()).hexdigest()

    file.seek(0)

    subdirectory = file_hash[:2]

    # Формируем путь сохранения файла
    directory = os.path.join(STORAGE_DIR, subdirectory)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file_hash)

    # Сохраняем файл
    file.save(file_path)

    # Получаем имя пользователя из запроса
    username = request.authorization.username

    # Создаем или находим пользователя в БД

    try:
        user = User.query.filter_by(name=username).first()
        if not user:
            user = User(name=username)
            db.session.add(user)
            db.session.commit()

        # Создаем запись о файле в БД
        uploaded_file = File(filename=file_hash, user=user)
        db.session.add(uploaded_file)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return file_hash, 200


@file_server_blueprint.route('/download', methods=['GET'])
def download_file():
    # Получение хеша файла из параметров запроса
    file_hash = request.args.get('file_hash')

    # Поиск файла по хешу и возврат файла, или ошибки 404, если файл не найден

    file_path = os.path.join(STORAGE_DIR, file_hash[:2], file_hash)
    if os.path.exists(file_path):
        return send_file(open(file_path, 'rb'), as_attachment=True, download_name='Без названия')
    else:
        return 'File does not exist', 404


@file_server_blueprint.route('/delete', methods=['GET'])
@auth_required
def delete_file():
    file_hash = request.args.get('file_hash')
    file_path = os.path.join(STORAGE_DIR, file_hash[:2], file_hash)
    username = request.authorization.username
    if os.path.exists(file_path):
        # Проверка принадлежности файла пользователю
        user = User.query.filter_by(name=username).first()
        filename = File.query.filter_by(filename=file_hash).first()
        if user.id == filename.user_id:
            os.remove(file_path)
            return 'File has been deleted', 200
    return 'Access denied when deleting file', 401

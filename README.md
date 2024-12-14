# Histology 🏥🦠

## Краткое описание проекта

Данный проект предоставляет API для загрузки, хранения и разделения файлов формата SVS (Slide Virtual Scanner). Используя FastAPI, приложение обеспечивает высокую производительность и простоту в использовании, позволяя пользователям загружать файлы, а также выполнять операции по их сегментации.

## 🚀 Основные возможности

- Загрузка данных
- Разделение данных
- Получение данных
- Удаление данных

## 🛠️ Технологический стек

- **Язык**: Python
- **Веб-фреймворк**: FastApi
- **Развертывание**: Docker (опционально)

## 🔧 Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/hk3dva/Hista.git

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Для Unix
venv\Scripts\activate    # Для Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
python main.py
```

## 🔧 Доступные endpoints
Сервис будет жоступен по ссылке http://127.0.0.1:8000/docs
Endpoint:
1. POST /upload - загрузка файла, в результате вернет уникальный media_id и дополнительную информацию про файл
2. POST /split/{media_id} - разделение файла на чанки, (chunk_size - размер области разделения) в результате вернет список media_id
3. GET /media/{media_id} - Получение файла 
4. DELETE /media/{media_id} - Удаление файла из системы

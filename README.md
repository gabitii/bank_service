# 🏦 Bank Service

Простой учебный проект на **Django**, который реализует систему пользователей, транзакций и генерации финансовых отчётов.  
Отчёты могут генерироваться как на основе **OpenAI API**, так и с помощью мок-логики, если ключа нет.

### Настройка переменных окружения

Перед запуском нужно создать файл `.env` в корне проекта:

```ini
SECRET_KEY=your-secret-key

DB_NAME=bank_service_db
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432

OPENAI_API_KEY=sk-xxxx
---

## ⚙️ Установка и запуск

### 1. Клонирование проекта
```bash
git clone https://github.com/yourusername/bank_service.git
cd bank_service
```
2. Создание виртуального окружения
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate   
```
3.Установка зависимостей
```bash
pip install -r requirements.txt
```
4. Переменные окружения
В корне проекта создайте файл .env и добавьте туда:
```bash
OPENAI_API_KEY=your_api_key_here
```
5. Применение миграций и загрузка данных
```bash
python manage.py migrate
python manage.py loaddata initial_data.json
```
6.Запуск сервера
```bash
python manage.py runserver
```
Тестирование
Запуск unit-тестов:
```bash
python manage.py test
```
### Переменные окружения

Для генерации отчётов через OpenAI укажите в `.env` файл:

Если переменная не указана, сервис вернёт мок-отчёт (сумма поступлений, расходов и топ-категория).

### Postman коллекция

В репозитории есть коллекция `postman_collection.json`, в которой собраны все основные запросы к API.

Чтобы импортировать её:
1. Откройте Postman
2. Нажмите `Import`
3. Выберите файл `postman_collection.json`
4. Теперь вы можете тестировать эндпоинты напрямую.

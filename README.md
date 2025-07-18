# 🏨 Snap-Book — сервис бронирования отелей

**Snap-Book** — это backend-сервис для бронирования отелей, разработанный с использованием современных технологий.  
Проект включает в себя авторизацию, управление пользователями, отелями, комнатами и бронированиями, а также фоновую обработку задач и развертывание через CI/CD.

🔗 Демо: [snap-book.ru](https://snap-book.ru)

---

## 🚀 Технологии

- ⚙️ **FastAPI** — web-фреймворк для API
- 🐘 **PostgreSQL** — основная СУБД
- 🔗 **SQLAlchemy** — ORM
- 🔀 **Alembic** — миграции БД
- 📦 **Docker / Docker Compose** — контейнеризация и локальный запуск
- 🧪 **Pytest** — покрытие unit, integration и API тестов
- 🧰 **Redis** — брокер для фоновых задач
- ⏱ **Celery** — асинхронные фоновые задачи (например, email-уведомления)
- 🔐 **JWT (PyJWT)** — аутентификация
- 🧹 **Black + Ruff** — форматирование и линтинг кода
- 🔁 **CI/CD (GitLab + GitLab Runner)** — автоматическая проверка и деплой на сервер
- 🌐 **Swagger UI** — документация к API

---

## 🔐 Безопасность и SSL

- Проект работает по **HTTPS** (используется SSL-сертификат)
- Сертификат получен через [Let's Encrypt](https://letsencrypt.org/)
- Подключён к домену [snap-book.ru](https://snap-book.ru)
- Все данные передаются по защищённому каналу

## 📦 Основные сущности

- **Пользователь**
  - Регистрация, авторизация (JWT)
  - Получение своих данных
  - Выход из аккаунта

- **Отель**
  - Создание / получение / изменение / удаление
  

- **Комната**
  - Привязана к отелю
  - Создание / получение / изменение / удаление

- **Бронирование**
  - Получение броней
  - Создание брони
  - Просмотр своих броней

- **Удобства**
  - Список всех удобств
  - Добавление удобства

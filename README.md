# Stripe Django Vue Integration

Тестовое задание: Реализация сервиса оплаты товаров и заказов с использованием Django (DRF), Vue 3 и Stripe API.

## Функционал

*   **Товары (Items):** Просмотр списка товаров, детальная страница товара.
*   **Заказы (Orders):** Группировка товаров в заказ, поддержка скидок (Discount) и налогов (Tax).
*   **Оплата (Stripe):**
    *   **Checkout Session:** Редирект на страницу оплаты Stripe.
    *   **Payment Intent:** Кастомная форма оплаты (Stripe Elements) прямо на сайте.
*   **Мультивалютность:** Поддержка USD и EUR (автоматический выбор Stripe ключей в зависимости от валюты товара).
*   **Docker:** Полная контейнеризация (Django + Nginx + Gunicorn).
*   **Админка:** Управление товарами, заказами, скидками и налогами через Django Admin.

## Технологии

*   **Backend:** Python 3.11, Django 5, Django REST Framework.
*   **Frontend:** Vue 3, Vite, Stripe.js.
*   **Infrastructure:** Docker Compose, Nginx.
*   **Database:** SQLite (внутри контейнера).

---

## Локальный запуск (Docker)

### 1. Клонирование репозитория
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Настройка окружения
Создайте файл `.env` в корне проекта:
```env
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=secret-key-local
ALLOWED_HOSTS=*

# Stripe Keys (USD)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Stripe Keys (EUR)
STRIPE_PUBLIC_KEY_EUR=pk_test_...
STRIPE_SECRET_KEY_EUR=sk_test_...
```

Создайте файл `frontend/.env`:
```env
VITE_STRIPE_PUBLIC_KEY=pk_test_...
VITE_STRIPE_PUBLIC_KEY_EUR=pk_test_...
```

### 3. Сборка Фронтенда
Перед запуском Docker необходимо собрать статику Vue. Если у вас нет Node.js, можно воспользоваться Docker:

```bash
# Вариант с Docker (рекомендуется)
docker run --rm -v "$PWD/frontend:/app" -w /app node:20-alpine sh -c "yarn install && yarn build"

# Или локально (если установлен Node.js)
cd frontend && yarn install && yarn build && cd ..
```

### 4. Запуск
```bash
docker compose up -d --build
```
Сервис будет доступен по адресу: http://localhost

### 5. Создание Суперпользователя (для доступа в админку)
```bash
docker exec -it test_django python manage.py createsuperuser
```
Админка доступна по адресу: http://localhost/admin/

---

## Запуск на сервере (Ubuntu)

### 1. Установка Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### 2. Скачивание проекта
```bash
mkdir -p /opt/www
cd /opt/www
git clone <your-repo-url> .
```

### 3. Настройка
Создайте `.env` файлы как в инструкции выше, но установите `DJANGO_DEBUG=False`.

**Важно:** Добавьте IP вашего сервера в `core/settings.py` в список `CSRF_TRUSTED_ORIGINS` перед сборкой (или отредактируйте на сервере), чтобы работала админка.

### 4. Сборка и Запуск
```bash
# Сборка фронтенда
docker run --rm -v "$PWD/frontend:/app" -w /app node:20-alpine sh -c "yarn install && yarn build"

# Запуск контейнеров
docker compose up -d --build

# Создание админа
docker exec -it test_django python manage.py createsuperuser
```

## API Endpoints

*   `GET /api/items/` - Список товаров
*   `GET /api/orders/` - Список заказов
*   `GET /api/item/{id}/` - Детали товара
*   `GET /api/order/{id}/` - Детали заказа
*   `GET /api/buy/{id}/` - Получение Session ID для оплаты товара (USD/EUR)
*   `GET /api/buy_order/{id}/` - Получение Session ID для оплаты заказа
*   `GET /api/buy/intent/{id}/` - Получение Client Secret для Payment Intent


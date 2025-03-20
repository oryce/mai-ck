# Фронтенд

Стек технологий:

- **Фреймворк**: Next.js 15 (React 19)
- **CSS-фреймворк**: Tailwind CSS 4
- **Библиотека компонентов**: Catalyst UI

## Запуск

Установите зависимости: `npm install`.

### Если используется json-server

#### 1. Создайте файл .env.local в корне проекта:

```
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_PUBLIC_JSON_SERVER=1
```

#### 2. Выполните `npm run json-server`

### В Dev-окружении

Выполните `npm run dev`.

### В Prod-окружении

Выполните `npm run start`.

### Через Docker

Предоставляются два Dockerfile: `dev.dockerfile` и `prod.dockerfile`. Они запускают dev-и prod-сервер соответственно на порту 3000.
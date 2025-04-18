<img width="150" src="docs/logo.png">

# Проект команды MAI's Hive

**Тема:** Система автоматического анализа электронного документа (PDF)

## Навигация

- [Паспорт проекта](docs/passport.pdf)
- [Презентация концепции проекта](docs/presentation.pdf)
- [Ресёрч-док](docs/research-doc.md)

### Диаграммы

- [Диаграмма архитектуры бэкенда](docs/diagram-backend.png)
- [Диаграмма БД](docs/diagram-database.png)
- [Диаграмма компонентов](docs/diagram-component.png)
- [Диаграмма контекстов](docs/diagram-context.jpg)
- [Диаграмма юз-кейсов](docs/diagram-use-cases.jpg)

### Код

- [Бэкенд](code/backend)
- [Фронтенд](code/frontend)

## Запуск

Проект можно запустить через Docker Compose. Для этого в `code/` предоставлены два Compose-файла: `docker-compose.yml` и `docker-compose.mock.yml` (с json-server вместо бэкенда).

Как запустить:

1. В `code/config/backend` и `code/config/postgres` переименовать `.env.template` в `.env`
2. Сгенерировать пароли для root и обычного пользователя в БД. Записать их в конфиг-файлы
3. Выполнить `docker-compose up` в `code`
4. Фронтенд будет доступен по `http://localhost:3000`, а бэкенд — по `http://localhost:8000`

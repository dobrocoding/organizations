# 🔐 Аутентификация API

## Обзор

API использует статический токен для аутентификации. Поддерживаются два способа передачи токена:

1. **Заголовок `X-API-Token`** (по умолчанию)
2. **Заголовок `Authorization: Bearer <token>`** (для совместимости со Swagger)

## Конфигурация

### Переменные окружения

```bash
# Токен для аутентификации (по умолчанию: Secunda_demo_token)
API_TOKEN=your-secure-token-here

# Название заголовка для токена (по умолчанию: X-API-Token)
API_TOKEN_HEADER=X-API-Token

# Требовать ли аутентификацию (по умолчанию: true)
API_TOKEN_REQUIRED=true
```

## Использование

### 1. Через заголовок X-API-Token

```bash
curl -H "X-API-Token: Secunda_demo_token" \
     http://localhost:8000/organizations/search/?query=test
```

### 2. Через заголовок Authorization (Bearer)

```bash
curl -H "Authorization: Bearer Secunda_demo_token" \
     http://localhost:8000/organizations/search/?query=test
```

### 3. В Swagger UI

1. Откройте `/docs` в браузере
2. Нажмите кнопку **"Authorize"** 🔒
3. Введите токен в формате: `Secunda_demo_token`
4. Нажмите **"Authorize"**
5. Теперь можете тестировать API через Swagger

## Коды ответов

| Код | Описание |
|-----|----------|
| 200 | Успешный запрос (с правильным токеном) |
| 401 | Токен не предоставлен |
| 403 | Неверный токен |
| 500 | Внутренняя ошибка сервера |

## Исключения

Следующие эндпоинты **НЕ требуют** аутентификации:

- `/docs` - Swagger UI
- `/redoc` - ReDoc документация  
- `/openapi.json` - OpenAPI схема

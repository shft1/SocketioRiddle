# Игра в загадки  
**Проект на веб-сокете на Python: socket.io**

## Описание

Веб-приложение с использованием WebSocket технологии для игры в загадки. 
Приложение поддерживает обмен сообщениями между клиентом (на фронте) и сервером для показа 
пользователю загадок и получения ответов.

## Задание

Разработать бэкенд на Python с использованием библиотеки Socket.IO для реализации сервера, 
который будет обрабатывать подключения клиентов, отправлять загадки и проверять ответы. 
Общаться с фронтом по веб-сокетам.

## Запуск приложения

1. Установите необходимые зависимости:

   ```bash
   pip install -r requirements.txt

2. Запуск бэкенда:

    ```bash
    python main.py

3. Приложение будет доступно по адресу http://127.0.0.1:8000

## Запуск тестов

Тесты уже реализованы и запускаются скриптом run_tests.sh (приложение при этом не должно быть запущено).

   ```bash
   ./run_tests.sh

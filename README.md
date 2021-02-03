Писал это приложение два года назад, в основном для обучения асинхронному программированию.

Перед началом работы требуется создать свое приложение
manage.py newapp [NAME]

Вписать его в настройках
from myapp.view import View as MyAppView
apps = {
  'myapp': MyAppView
}

и запустить сервер
manage.py runserver

В приложенном шаблоне пример взаимодействия.

Доступно взаимодействие из других приложений через socket
http_registrations_request = False
handshake = False
название приложения передавать как параметр

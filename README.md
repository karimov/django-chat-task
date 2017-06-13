# django-chat-task
Chat API with django rest framework

<snippet>
  <content><![CDATA[
# ${1:Project Name}

TODO: Write a project description

## Installation

1. $ pip install -r requirements.txt
2. $ python3 manage.py migrate
3. $ python3 manage.py createsuperuser

## Usage

Client: http://localhost:8000/client
API_ROOT: http://localhost:8000

1) Пользователь должен иметь возможность зарегистрироваться указав логин и пароль, далее авторизоваться по указанным данным.
   POST http://127.0.0.1:8000/users/
2) Комната чата только одна и едина для всех.
3) Пользователь может отправить текстовое сообщение.
   POST http://localhost:8000/messages/send
4) Для получения новых сообщений необходимо реализовать поллинг.
   POST http://localhost:8000/messages/poll
5) Реализовать механизм загрузки истории сообщений.
   POST http://localhost:8000/messages/?=date="YYY-mm-dd"
   пример: 2017-07-11
6) Api должен быть защищенным. Как минимум необходимо отвечать ошибкой на запросы от пользователей, которые не авторизовались


]]></content>
  <tabTrigger>readme</tabTrigger>
</snippet>

REST API сотрудники компании
Описание
Проект управляет пользователями компании(Создание, увольнение, изменение руководителя).
У каждого сотрудника имеется данные по его должности. Список должностей может быть расширен(Секретарь, разработчик) через панель администратора.

API сервисы:
* - обязательные поля

Генерация токена авторизации:
Для обращения на API сервисы – необходимо иметь JWT – токен авторизации пользователя.
Передаем на сервер email и password(почту и пароль) существующего пользователя и получаем в ответ токен авторизации, время жизни которого 1 день.
POST http://127.0.0.1:8000/api/v1/login/
Таблица отправляемых данных:
Параметр	Тип	Значение
email*	str	Почта сотрудника с помощью которого он авторизуется
password*	str	Пароль пользователя, минимальная длина 1, макс длина 8

Пример запроса:
{
        "email": "baydibekov98@gmail.com",
        "password": "12345678"
    }

Таблица получаемых данных данных:
Параметр	Тип	Значение
email	str	Почта сотрудника с помощью которого он авторизуется
username	str	Имя пользователя в системе
token	str	Токен авторизации

Ответ:
200 OK
{
    "email": "baydibekov98@gmail.com",
    "username": "Alisher",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjU0NjY2OTczfQ.8qyAkDQM5T6NfPzUj5eRWZAOwLo3mCMZOtKP7JjAjIM"
}

400 Bad Request:
{
    "non_field_errors": [
        "A user with this email and password was not found."
    ]
}

Для авторизации к API – сервисам необходимо прописать в Заголовках запроса:
Authorization : Token + {Токен пользователя}

Authorization : Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OSwiZXhwIjoxNjU0NjAxOTg2fQ.ik4_tpeRx-zCLCDe8Ib0JmX91KiFBDDFerWBW3YNyws

Добавление нового сотрудника компании.
Уровень доступа: Администратор
Передаем на сервер персональные данные сотрудника (имя пользователя, email, должность и т.д.).
Сохраняем информацию в базе данных, генерируем jwt токен.
Ответ сервера - уникальный ID нового сотрудника и токен для авторизации.
POST http://127.0.0.1:8000/api/v1/employee/
Таблица отправляемых данных:
Параметр	Тип	Значение
username*	str	Имя пользователя в системе
first_name*	str	Имя сотрудника
last_name*	str	Фамилия сотруднника
job_position	int	Должность сотрудника
email*	email	Почта сотрудника с помощью которого он авторизуется
Уникальное поле – почта не должна повторятся с имеющими
В базе
password*	str	Пароль пользователя, минимальная длина 1, макс длина 8
birth_date	date	Дата рождения сотрудника
id_leader	int	Id Руководителя сотрудника
is_staff	bool	Поле определяющее администратора от пользователя

Пример запроса:

{
    "username": "Alisher",
    "first_name": "Alisher",
    "last_name": "Baydibekov",
    "email": "baydibekov9701@gmail.com",
    "password": "12345678"
}

Таблица получаемых данных:
Параметр	Тип	Значение
id	int	Идентификационный номер сотрудника
token	str	Токен авторизации

Ответ:
201 CREATED:
{
    "id": 13,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTMsImV4cCI6MTY1NDYxNTA4OX0.ZrG74MFBUerqgU2ETRO-Yh8kisk1XV2E1FEMmC0H8wA"
}

400 Bad Request:
{
    "first_name": [
        "This field is required."
    ],
    "email": [
        "employee with this email already exists."
    ]
}


Получение информации о сотруднике.
Передаем на сервер уникальный ID сотрудника.
Читаем информацию из базы данных.
Ответ сервера - персональные данные сотрудника и руководителя сотрудника
GET http://127.0.0.1:8000/api/v1/employee/{id}
Таблица получаемых данных:
Параметр	Тип	Значение
id	int	Идентификационный номер сотрудника
username	str	Имя пользователя в системе
first_name	str	Имя сотрудника
last_name	str	Фамилия сотруднника
job_position	int	Должность сотрудника
email	email	Почта сотрудника с помощью которого он авторизуется
Уникальное поле – почта не должна повторятся с имеющими
В базе
password	str	Пароль пользователя, минимальная длина 1, макс длина 8
birth_date	date	Дата рождения сотрудника
id_leader	int	Id Руководителя сотрудника
Is_active	bool	Активность сотрудника(Уволен или нет)
is_staff	bool	Поле определяющее администратора от пользователя
create_date	date	Дата создании сотрудника
update_date	date	Дата изменение информации сотрудника

Ответ: 
200 OK:
{
    "employee": {
        "id": 11,
        "username": "Alisher",
        "first_name": "",
        "last_name": "",
        "birth_date": null,
        "email": "baydibekov979@gmail.com",
        "create_date": "2022-06-06T14:29:04.237006Z",
        "update_date": "2022-06-06T15:30:24.103536Z",
        "id_leader": 12,
        "is_active": true,
        "is_staff": false,
        "job_position": null
    },
    "leader": {}
}

400 Bad Request
{
    "error": "Object does not exists"
}


Изменение руководителя сотрудника (Активный, Неактивный).
Передаем на сервер уникальный ID сотрудника и новый статус (Активный, Неактивный).
Изменяем статус сотрудника.
Ответ сервера - уникальный ID сотрудника, новый и предыдущий статус.
PUT http://127.0.0.1:8000/api/v1/changestatus/
Таблица отправляемых данных:
Параметр	Тип	Значение
id*	int	Идентификационный номер сотрудника
is_active *	bool	Статус на который хотят поменять

Пример запроса:
{
    "id": 12,
    "is_active": false
}

Таблица получаемых данных:
Параметр	Тип	Значение
id	int	Идентификационный номер сотрудника
last_activity	str	Прошлый статус сотрудника
activity	str	Новый статус сотрудника

Ответ:
200 ОК:
{
    "id": 12,
    "last_activity": "not active",
    "activity": "not active"
}

400 Bad Request:
{
    "is_active": [
        "Must be a valid boolean."
    ]
}

Изменение/изменение руководителя сотрудника
Передаём на сервер уникальный ID сотрудника и уникальный ID руководителя
Изменяем руководителя сотрудника
Ответ сервера - уникальный ID сотрудника, уникальный ID руководителя и сообщение об успехе.
PUT http://127.0.0.1:8000/api/v1/changeleader/
Таблица отправляемых данных:
Параметр	Тип	Значение
id*	int	Идентификационный номер сотрудника
Id_leader *	int	Идентификационный номер руководителя

Пример запроса:
{
    "id": 11,
    "id_leader": 12
}

Таблица получаемых данных:
Параметр	Тип	Значение
id	int	Идентификационный номер сотрудника
Id_leader 	int	Идентификационный номер руководителя
status	str	Информация об состоянии

Ответ:
200 ОК:
{
    "id": 10,
    "id_leader": 11,
    "status": "Success"
}

400 Bad Request:
{
    "error": "Object leader does not exists"
}

Установка на локальном компьютере
Эти инструкции помогут вам создать копию проекта и запустить ее на локальном компьютере для целей разработки и тестирования.

Установка Docker
Установите Docker, используя инструкции с официального сайта:

для Windows и MacOS
для Linux. Отдельно потребуется установть Docker Compose
Запуск проекта (на примере Linux)
Создайте на своем компютере папку проекта alisher_test 
mkdir alisher_test 
и перейдите в нее 
cd yamdb
Склонируйте этот репозиторий в текущую папку git clone https://github.com/baydibekov98/alisher_test

-	Запустите docker-compose командой 
sudo docker-compose up -d
-	Накатите миграции 
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate



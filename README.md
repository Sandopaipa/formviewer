# formviewer
## ОПИСАНИЕ
Данное веб-приложение служит для верификации данных, передаваемых POST запросом по URL: /get_form. Вид передаваемых данных: "f_name1=value1&f_name2=value2", где f_name - название поля, value - значение, записанное в данное поле
Приложение обрабатывает строку, определяет поля и типы данных, которые в них записаны. После этого делает поиск наиболее подходящего шаблона формы.

Типы данных: 

1. EMAIL - электронная почта;

2. DATE - дата вида: 1 - DD.MM.YYYY, 2- YYYY-MM-DD;

3. PHONE - номер телефона вида: +7 XXX XXX XX XX;

4. TEXT - Текст. Такой тип выдается всем значениям полей, которые программа не идентифицировала как электронную почту, дату или номер телефона.

В случае, если было найдено совпадение названия поля и его типа - выдаетется название шаблона формы. Иначе - словарь, состоящий из названия поля и определенных программой типов: {f_name1: FIELD_TYPE, f_name2: FIELD_TYPE}. Если в процессе преобразования строки в словарь было найдено неуникальное название поля - то вызывается исключение UniqueError.
## ИНСТРУКЦИЯ

Для запуска приложения необходимо:

1. На вашем устройстве должен быть установлен и запушен Docker;
2. Клонируйте репозиторий на ваше устройство;
3. Перейдите в директорию с файлом docker-compose.yml;
4. Убедитесь, что порт 8000 не занят. Если вы хотите использовать другой порт - отредактируйте docker-compose.yml, изменив порт для службы verifier;
5. Убедитесь, что порт 27017 не занят. Если вы хотите использовать другой порт - отредактируйте docker-compose.yml, изменив порт для службы mongo.

### При первом запуске: 

Для сборки и запуска контейнера в фоновом режиме выполните команду:

    docker-compose up -d

Так как изначально в MongoDB нет шаблонов форм - их необходимо загрузить. Для этого выполните команду:

    docker-compose exec mongo bin/mongoimport --db templates_db --collection templates --file data/templates_db/mongodb_backup.json --jsonArray

Это создаст базу данных templates_db и коллекцию templates с последующей загрузкой в неё данных из файла mongodb_backup.json.

Для того, чтобы завершить работу - воспользуйтесь командой:
    
    docker-compose stop

### При последующих запусках

Для запуска используйте команду
    
    docker-compose start

Для завершения работы используйте команду: 
    
    docker-compose stop

## ДОПОЛНИТЕЛЬНО

Для того, чтобы добавлять новые шаблоны форм, пожалуйста воспользуйтесь либо импортом из файла при помощи mongoimport, 
либо при помощи mongosh - командной строки для управления MongoDB.

Для того, чтобы сделать тестовые запросы к приложению - воспользуйтесь командой
    
    docker-compose exec verifier python manage.py test

Обратите внимание, что приложение должно быть запущено. Тестовые запросы находятся по пути form_identifier/tests.py.

Если вы хотите использовать базу данных или коллекцию с другим именем - пожалуйста отредактируйте файл .env, где
- MONGO_DB_NAME - название базы данных
- MONGO_COLLECTION_NAME - название коллекции.

После этого не забудте создать новые базу данных и коллекцию и добавить туда данные. 
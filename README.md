
Практика 3.6 Airflow
На Debian 11 без Docker'a 

Доп. Инфа:
1. Устанавливаем Python и доп. пакеты:
sudo apt-get install python3-pip python-setuptools -y
sudo apt-get install libssl-dev libkrb5-dev python3-virtualenv python-jinja2 -y
pip3 install typing_extensions

2. Уст. переменную среды:
export AIRFLOW_HOME=~/airflow

3. Уст. AirFlow:
pip3 install apache-airflow[all_dbs]==2.5.0 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-latest/constraints-3.10.txt"
Проверяем версию AirFlow:
airflow version

4. Инициализируем базу данных AirFlow:
airflow db init
airflow db upgrade
Создаем пользователя для входа в AirFlow:
airflow users create -u airflow -p airflow -f toljan -l chizman -r Admin -e ls2010@mail.ru

5. Запускаем планировщик AirFlow:
airflow scheduler
Открывыаем новый терминал и запускаем сервер AirFlow UI:
airflow webserver -p 8080

6. Открывем браузер и входим в AirFlow UI:
http://localhost:8080
имя: airflow пароль: airflow

7. Далее запускаем наш DAG и смотрим логи...

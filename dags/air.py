from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable, taskinstance
from airflow.models.xcom import XCom

def hello(ti):
	print("Airflow")

file = "/home/deb11/airflow/dags/snakes.csv"
def strcount(ti):
	#Скачайте произвольный csv-файл(можно отсюда: https://people.sc.fsu.edu/~jburkardt/data/csv/csv.html) и напишите в python-операторе код, который подключается к скачанному csv-файлу и подсчитывает количество строк в файле. Попробуйте использовать технологию Variables и записать путь к файлу в список переменных Airflow, а кол-во строк в файле записать в XCom.
	import ssl
	import urllib3
	from urllib3.util.ssl_ import create_urllib3_context
	#file = "./snakes.csv"
	urllib3.disable_warnings()
	ctx = create_urllib3_context()
	ctx.load_default_certs()
	ctx.options |= ssl.OP_ENABLE_MIDDLEBOX_COMPAT
	
	with urllib3.PoolManager(ssl_context=ctx) as pool:
  		http = urllib3.PoolManager()
  		url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/snakes_count_10.csv'
    		
  		resp = http.request('GET', url)  
  		data = resp.data
  		fstrcount = len(str(data).split("\\n"))
  		#print(fstrcount)
	
	with open(file, mode="wb") as csvf:
     		csvf.write(resp.data)
	
	Variable.set("AIRFLOW_VAR_FILEPATH", file)
	#XCom.set("strcount",fstrcount)
	#ti.xcom_push(key='strcount', value=fstrcount)
	#ti = ct['python_task2']
	ti.xcom_push(key='strcount', value=fstrcount)
	
def rcstrfile(ti):
	#передайте в него из первого python-оператора количество строк. Прочитайте файл(с использованием переменных) и добавьте к данному файлу колонку справа, которая будет номеровать строки в обратном порядке(т.е. первая строка должна принять значение кол-ва строк файла, каждая следующая строка -1 от значения в предыдущей). Сохраните полученный файл.
	import pandas as pd
	#ti = ct['python_task2']
	fstrcount = ti.xcom_pull(key='strcount')
	#fstrcount = ti.xcom_pull(key="strcount", task="python_task2")
	data_new = pd.read_csv(Variable.get("AIRFLOW_VAR_FILEPATH"))
	new_col = list(range(1,int(fstrcount)-1))
	new_col.reverse()
	#print(new_col)
	data_new['strrev'] = new_col
	data_new.to_csv('/home/deb11/airflow/dags/snakes_new.csv')
	
# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="first_dag", start_date=datetime(2022, 1, 1), schedule="* * * * *") as dag:
	# Tasks are represented as operators
	bash_task = BashOperator(task_id="hello", bash_command="echo hello")
	
	python_task = PythonOperator(task_id="world", python_callable = hello)
	
	python_task2 = PythonOperator(task_id="strcount", python_callable = strcount)
	
	python_task3 = PythonOperator(task_id="rcstrfile", python_callable = rcstrfile)
	
	bash_task2 = BashOperator(task_id="mvfiletoair", bash_command="mv -f /home/deb11/airflow/dags/snakes_new.csv /home/deb11/airflow/snakes_new.csv")
	
	bash_task3 = BashOperator(task_id="printSuccess", bash_command="echo Success!")
	
	# Set dependencies between tasks
	bash_task >> python_task >> python_task2 >> python_task3 >> bash_task2 >> bash_task3

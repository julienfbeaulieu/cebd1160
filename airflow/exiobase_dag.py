from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2018, 11, 19),
    "email": ["julienfbeaulieu@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG("news_scrapper_dag",
          schedule_interval='@once',
          default_args=default_args)

# Define database loading task
t1 = BashOperator(
    task_id="load_database",
    bash_command="python /usr/local/airflow/load_database_airflow.py",
    dag=dag
)

# Define results analysis task
t2 = BashOperator(
    task_id="analyse_results",
    bash_command="python /usr/local/airflow/analyse_results_airflow.py",
    dag=dag
)

# Schedule tasks
t2.set_upstream(t1)
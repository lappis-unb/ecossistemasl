from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'your_owner',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag_id = 'main_dag'

main_dag = DAG(
    dag_id=dag_id,
    default_args=default_args,
    schedule_interval='@weekly',
)

notebook_path = 'notebook_path'

execute_notebook = BashOperator(
    task_id='execute_notebook',
    bash_command=f'papermill {notebook_path} -',
    dag=main_dag,
)

if __name__ == "__main__":
    main_dag.cli()

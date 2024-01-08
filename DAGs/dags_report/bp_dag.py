from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from plugins.graphql_hook import GraphQLHook

default_args = {
    'owner': 'your_owner',
    'start_date': datetime(2024, 1, 1, 8, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag_id = 'graphql_execution_dag'
dag = DAG(
    dag_id=dag_id,
    default_args=default_args,
    schedule_interval='@daily',
)

def execute_graphql_query(**kwargs):
    conn_id = 'your_conn_id'
    cert_path = 'your_cert_path'
    query_path = 'your_query_path'
    output_path = 'your_output_path'

    graphql_hook = GraphQLHook(conn_id)
    graphql_hook.cert_path = cert_path

    graphql_query = graphql_hook.get_graphql_query_from_file(query_path)

    for result_page in graphql_hook.run_graphql_paginated_query(graphql_query, component_type="proposals", variables={"page": "null"}):
        graphql_hook.write_json_to_file(result_page, output_path)

execute_graphql_task = PythonOperator(
    task_id='execute_graphql_task',
    python_callable=execute_graphql_query,
    provide_context=True,
    dag=dag,
)

if __name__ == "__main__":
    dag.cli()

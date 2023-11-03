from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from dotenv import load_dotenv
from psycopg2 import Error
import pandas as pd
from sqlalchemy.util import deprecations

SQLALCHEMY_SILENCE_UBER_WARNING=1 
SQLALCHEMY_WARN_20=1

def pokemon_function():
    exec(open("/Users/javier/Desktop/pokemonAPI.py").read())

default_args = {
    'owner': 'Javier Maya',
    'start_date': datetime(2023, 10, 30), # Fecha de inicio del DAG
    'retries': 1, # Número de reintentos en caso de fallo
}

with DAG(
    'pokemon_api_dag',
    default_args=default_args,
    schedule=None, # Define la frecuencia de ejecución (en este caso, None para ejecución manual)
    catchup=False, # Evita la ejecución retroactiva de tareas perdidas
    dagrun_timeout=None, # Duración máxima de una ejecución del DAG
    description='DAG para ejecutar el script de Pokemon API',
    tags=['pokemon'],
) as dag:

    start = EmptyOperator(
        task_id = "Inicio"
    )

    end = EmptyOperator(
        task_id = "Fin"
    )

    # Operador PythonOperator para ejecutar el script de Python
    run_pokemon_operator = PythonOperator(
        task_id='run_pokemon_script',
        python_callable=pokemon_function,
        dag=dag,
    )

# Configurar la dependencia
start >> run_pokemon_operator >> end
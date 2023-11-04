import requests
import psycopg2
import json
import os
import sys
from dotenv import load_dotenv
from psycopg2 import Error
import pandas as pd

# Obtiene la ruta del directorio actual del script
ruta_script = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta al directorio DataEngineering
ruta_data_engineering = os.path.dirname(ruta_script)

# Agrega la ruta al PYTHONPATH
sys.path.append(ruta_data_engineering)

def ejecutar_pokemon(): 
    # URL de la API de Pokémon para obtener información del Pokémon
    pokemon_api_url = 'https://pokeapi.co/api/v2/pokemon/'

    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    try:
        # Conectándose a la base de datos Redshift
        connection = psycopg2.connect(
            user='j_mayanavarrete_coderhouse',
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'),
            port=int(os.getenv('PORT')),
            database=os.getenv('DATABASE')
        )

        cursor = connection.cursor()

        # Solicitud a la API de Pokémon para obtener información del Pokémon
        pokemon_name='pikachu'
        response = requests.get(pokemon_api_url + str(pokemon_name))
        pokemon_data = response.json()

        # Extraer la información necesaria del Pokémon
        id = pokemon_data['id']
        name = pokemon_data['name']
        height = pokemon_data['height']
        weight = pokemon_data['weight']

        # Obtener lista de tipo del Pokémon
        types = [type['type']['name'] for type in pokemon_data['types']] 

        # Obtener lista de movimientos del Pokémon
        moves_limit = 3
        moves = [move['move']['name'] for move in pokemon_data['moves'][:moves_limit]]

        # Obtener lista de debilidades del Pokémon
        weaknesses_url = f"https://pokeapi.co/api/v2/type/{types[0]}/"
        weaknesses_response = requests.get(weaknesses_url)

        if weaknesses_response.status_code == 200:
            weaknesses_data = weaknesses_response.json()
            weaknesses = [t['name'] for t in weaknesses_data['damage_relations']['double_damage_from']]
        else:
            weaknesses = []

        # Convierte las listas a objetos JSON
        types_json = json.dumps(types)
        moves_json = json.dumps(moves)
        weaknesses_json = json.dumps(weaknesses)

        # Leer datos existentes desde la base de datos
        select_query = "SELECT * FROM pokemon"
        cursor.execute(select_query)
        existing_data = cursor.fetchall()

        # Convertir los datos existentes en un DataFrame de Pandas
        existing_df = pd.DataFrame(existing_data, columns=['id', 'nombre', 'altura', 'peso', 'tipo', 'movimientos', 'debilidades'])

        # Comprobar si el nuevo Pokémon ya existe en la base de datos
        if name.lower() in existing_df['nombre'].str.lower().values:
            print(f"El Pokémon {name} ya existe en la base de datos. No se insertará el duplicado.")
        else:
            # Insertar el registro del Pokémon en la tabla de base de datos Redshift
            insert_query = "INSERT INTO pokemon (id, nombre, altura, peso, tipo, movimientos, debilidades) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (id, name, height, weight, types_json, moves_json, weaknesses_json))
            connection.commit()

            print(f"Registro del Pokémon {name} insertado exitosamente en la tabla.")

    except Error as e:
        print("Error al conectar a la base de datos Redshift:", e)

    finally:
        # Cerrar la conexión a la base de datos
        if connection:
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

ejecutar_pokemon()
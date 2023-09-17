import requests

# pokemon_name = "CHARMANDER"
pokemon_name = input("Ingresa nombre de Pokémon a buscar: ").lower()
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"

response = requests.get(url)

if response.status_code == 200:
    pokemon_data = response.json()
    
    # Extraer información relevante del Pokémon
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
    
    # Mostrar la información por pantalla
    print(f"ID: {id}")
    print(f"Nombre: {name}")
    print(f"Altura: {height / 10} metros")
    print(f"Peso: {weight / 10} kilogramos")
    print(f"Tipo(s): {', '.join(types)}")
    print(f"Top {moves_limit} movimientos: {', '.join(moves)}")
    print(f"Debilidad(es): {', '.join(weaknesses)}")
else:
    print("No se pudo obtener la información del Pokémon.")

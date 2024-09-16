# Funções para gerar a matriz de distâncias
import googlemaps
import logging


# Definindo a chave da API diretamente
API_KEY = 'SUA_Chave_API'
gmaps = googlemaps.Client(key=API_KEY)


def get_distance_matrix(locations):
    """
    Obtém a matriz de distâncias entre as localizações fornecidas usando a API do Google Maps.

    Args:
        locations (list of tuples): Lista de localizações como coordenadas (latitude, longitude).

    Returns:
        list of lists: Matriz de distâncias entre as localizações.
    """
    matrix = []
    for origin in locations:
        row = []
        for destination in locations:
            if origin == destination:
                row.append(0)
            else:
                try:
                    response = gmaps.distance_matrix(origin, destination, mode='driving')
                    logging.info(f"Resposta da API: {response}")
                    if response['status'] == 'OK':
                        distance = response['rows'][0]['elements'][0]['distance']['value']
                        row.append(distance)
                    else:
                        logging.error(f"Error fetching distance from {origin} to {destination}: {response['status']}")
                        row.append(float('inf'))
                except Exception as e:
                    logging.error(f"Exception occurred: {e}")
                    row.append(float('inf'))
        matrix.append(row)
    return matrix

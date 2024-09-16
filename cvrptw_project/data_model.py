# Funções relacionadas à criação do modelo de dados
import random
from distance_matrix import get_distance_matrix

def generate_random_customers(n_customers, depot_location, distribution='uniform'):
    """
    Gera localizações de clientes aleatórios baseados no tipo de distribuição fornecido.

    Args:
        n_customers (int): Número de clientes a serem gerados.
        depot_location (tuple): Localização do depósito (latitude, longitude).
        distribution (str): Tipo de distribuição dos clientes ('uniform' ou 'clusters').

    Returns:
        list of tuples: Lista de localizações de clientes incluindo o depósito.
    """
    customers = [depot_location]
    for _ in range(n_customers):
        if distribution == 'uniform':
            lat = depot_location[0] + random.uniform(-0.01, 0.01)
            lng = depot_location[1] + random.uniform(-0.01, 0.01)
        elif distribution == 'clusters':
            cluster_lat = depot_location[0] + random.uniform(-0.005, 0.005)
            cluster_lng = depot_location[1] + random.uniform(-0.005, 0.005)
            lat = cluster_lat + random.uniform(-0.005, 0.005)
            lng = cluster_lng + random.uniform(-0.005, 0.005)
        location = (lat, lng)
        customers.append(location)
    return customers


def create_data_model(distribution='uniform', time_window_type='rigorous'):
    """
    Cria o modelo de dados para o problema de roteamento de veículos com janelas de tempo (CVRPTW).

    Args:
        distribution (str): Tipo de distribuição dos clientes ('uniform' ou 'clusters').
        time_window_type (str): Tipo de janela de tempo ('rigorous' ou 'relaxed').

    Returns:
        dict: Dicionário contendo os dados do problema.
    """
    data = {}
    n_customers = 20
    depot_location = (38.81705029358125, -9.148120629963021)

    customers = generate_random_customers(n_customers, depot_location, distribution)
    data['locations'] = customers
    data['num_vehicles'] = 20
    data['depot'] = 0

    data['distance_matrix'] = get_distance_matrix(customers)

    if time_window_type == 'rigorous':
        data['time_windows'] = [(0, 10) for _ in range(n_customers + 1)]
    elif time_window_type == 'relaxed':
        data['time_windows'] = [(random.randint(0, 10), random.randint(10, 20)) for _ in range(n_customers + 1)]

    data['demands'] = [0] + [random.randint(1, 10) for _ in range(n_customers)]
    data['vehicle_capacities'] = [random.randint(10, 20) for _ in range(data['num_vehicles'])]

    return data
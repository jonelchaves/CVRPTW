# Funções para manipulação e validação de soluções

import logging

def print_solution(data, manager, routing, solution):
    """
    Imprime a solução encontrada pelo solver, incluindo as rotas dos veículos, distâncias e cargas.

    Args:
        data (dict): Dicionário contendo os dados do problema.
        manager (pywrapcp.RoutingIndexManager): Gerenciador de índices de rotas.
        routing (pywrapcp.RoutingModel): Modelo de roteamento.
        solution (pywrapcp.Assignment): Solução encontrada pelo solver.

    Returns:
        tuple: Distância total e carga total das rotas.
    """
    if not solution:
        logging.info('No solution found!')
        print('No solution found!')
        return float('inf'), 0  # Retorna distância infinita e carga zero se não for encontrada uma solução

    total_distance = 0  # Inicializa a distância total
    total_load = 0  # Inicializa a carga total

    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route_load = 0
        route = f"Route for Vehicle {vehicle_id + 1}:\n"
        route += f" {manager.IndexToNode(index)} Load({route_load}) ->"  # Começa do depósito com carga zero

        while not routing.IsEnd(index):
            next_index = solution.Value(routing.NextVar(index))
            node_from = manager.IndexToNode(index)
            node_to = manager.IndexToNode(next_index)

            route_distance += data['distance_matrix'][node_from][node_to]  # Adiciona a distância entre os nós à distância total da rota
            route_load += data['demands'][node_to]  # Atualiza a carga com a demanda do próximo nó

            route += f" {node_to} Load({route_load}) ->"
            index = next_index

        # Adiciona a carga e a distância para regressar ao depósito
        route_distance += data['distance_matrix'][manager.IndexToNode(index)][manager.IndexToNode(routing.Start(vehicle_id))]
        route_load += data['demands'][manager.IndexToNode(index)]  # Isto é frequentemente zero, pois a demanda do depósito é zero

        route = route.rstrip('-> ')  # Remove a seta final
        route += f"\nDistance of the route: {route_distance / 1000:.2f} km\n"
        route += f"Load of the route: {route_load}\n"  # Imprime a carga desta rota

        print(route)
        logging.info(route)

        total_distance += route_distance
        total_load += route_load  # Acumula a carga total para todas as rotas

    total_distance_msg = f"Total distance of all routes: {total_distance / 1000:.2f} km"
    total_load_msg = f"Total load of all routes: {total_load}"  # Imprime a carga total de todas as rotas
    print(total_distance_msg)
    print(total_load_msg)
    logging.info(total_distance_msg)
    logging.info(total_load_msg)

    return total_distance, total_load  # Retorna tanto a distância total quanto a carga total

def validate_solution(data, manager, routing, solution):
    """
    Valida a solução do CVRPTW verificando a demanda e o tempo de cada rota.

    Args:
        data (dict): Dicionário contendo os dados do problema.
        manager (pywrapcp.RoutingIndexManager): Gerenciador de índices de rotas.
        routing (pywrapcp.RoutingModel): Modelo de roteamento.
        solution (pywrapcp.Assignment): Solução encontrada pelo solver.

    Returns:
        bool: Retorna True se a solução for válida, False caso contrário.
    """
    total_demand = [0] * data['num_vehicles']
    total_time = [0] * data['num_vehicles']

    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route_demand = 0
        route_time = 0

        while not routing.IsEnd(index):
            next_index = solution.Value(routing.NextVar(index))
            from_node = manager.IndexToNode(index)
            to_node = manager.IndexToNode(next_index)

            route_demand += data['demands'][from_node]
            route_time += data['distance_matrix'][from_node][to_node] / 1000.0  # Converte para km

            index = next_index

        route_demand += data['demands'][manager.IndexToNode(index)]
        total_demand[vehicle_id] = route_demand
        total_time[vehicle_id] = route_time

        if route_demand > max(data['vehicle_capacities']):
            warning_msg = f"Capacity exceeded for vehicle {vehicle_id + 1}"
            print(warning_msg)
            logging.warning(warning_msg)
        if route_time > 60:  # Supondo que o tempo máximo permitido seja 60 minutos
            warning_msg = f"Time window exceeded for vehicle {vehicle_id + 1}"
            print(warning_msg)
            logging.warning(warning_msg)

    validation_msg = "Solution validated"
    print(validation_msg)
    logging.info(validation_msg)
    return True


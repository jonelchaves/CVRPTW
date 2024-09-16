# Função que configura e executa o solver

from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from data_model import create_data_model
from solution_utils import print_solution
from plot_utils import plot_routes
from simulation_logging import log_simulation
import logging
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def solve_cvrptw(distribution, time_window_type):
    data = create_data_model(distribution, time_window_type)
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # margem
        data['vehicle_capacities'],  # capacidades dos veículos
        True,  # começar com o acumulado a zero
        'Capacity')

    def time_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['distance_matrix'][from_node][from_node] / 1000

    time_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.AddDimension(
        time_callback_index,
        30,  # tempo máximo de espera
        60,  # tempo máximo permitido
        False,  # Não forçar o acumulado a zero no início
        'Time')

    strategies = {
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC: 'Path Cheapest Arc',
        routing_enums_pb2.FirstSolutionStrategy.SAVINGS: 'Savings',
        routing_enums_pb2.FirstSolutionStrategy.SWEEP: 'Sweep',
        routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES: 'Christofides'
    }

    heuristics = {
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH: 'Guided Local Search',
        routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH: 'Tabu Search'
    }

    results = []

    for strategy, strategy_name in strategies.items():
        for heuristic, heuristic_name in heuristics.items():
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = strategy
            search_parameters.local_search_metaheuristic = heuristic
            search_parameters.time_limit.seconds = 60
            print(f'\nTesting strategy {strategy_name} and heuristic {heuristic_name}')
            logging.info(f'\nTesting strategy {strategy_name} and heuristic {heuristic_name}')

            start_time = time.time()
            solution = routing.SolveWithParameters(search_parameters)
            end_time = time.time()

            computation_time = end_time - start_time
            computation_time_msg = f'Computation Time: {computation_time:.2f} seconds'
            print(computation_time_msg)
            logging.info(computation_time_msg)

            if solution:
                total_distance, _ = print_solution(data, manager, routing, solution)
                # validate_solution(data, manager, routing, solution)  # Remova se não for necessário

                # Só gera gráfico para a solução que é atualmente a melhor
                if not results or total_distance < min(results, key=lambda x: x[2])[2]:
                    plot_routes(data, manager, routing, solution)

                results.append((strategy_name, heuristic_name, total_distance, computation_time))
            else:
                no_solution_msg = 'No solution found!'
                print(no_solution_msg)
                logging.info(no_solution_msg)
                results.append((strategy_name, heuristic_name, float('inf'), computation_time))

    # Identifica a fase atual
    phase = f"{distribution.capitalize()} Distribution & {time_window_type.capitalize()} Time Windows"

    # Logar os resultados em um arquivo CSV e JSON
    params = {
        'distribution': distribution,
        'time_window_type': time_window_type
    }
    log_simulation(params, results, phase)

    # Converte os resultados para DataFrame
    results_df = pd.DataFrame(results, columns=['Strategy', 'Heuristic', 'Total Distance', 'Computation Time'])

   
    # Gráfico de barras para comparação de distâncias
    plt.figure(figsize=(14, 7))
    sns.barplot(data=results_df, x='Strategy', y='Total Distance', hue='Heuristic', palette='Set1')
    plt.title('Total Distance by Strategy and Heuristic')
    plt.xlabel('Strategy')
    plt.ylabel('Total Distance (meters)')
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('cvrptw_total_distance_comparison.png')
    plt.show()

 # Gráfico de barras para comparação de tempos de computação
    plt.figure(figsize=(14, 7))
    sns.barplot(data=results_df, x='Strategy', y='Computation Time', hue='Heuristic', palette='Set1')
    plt.title('Computation Time by Strategy and Heuristic')
    plt.xlabel('Strategy')
    plt.ylabel('Computation Time (seconds)')
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('cvrptw_computation_time_comparison.png')
    plt.show()

   # Gráfico de dispersão para comparação de distâncias e tempos de computação
    plt.figure(figsize=(14, 7))
    sns.scatterplot(data=results_df, x='Computation Time', y='Total Distance', hue='Strategy', style='Heuristic',
                    palette='Set1')
    plt.title('Computation Time vs Total Distance')
    plt.xlabel('Computation Time (seconds)')
    plt.ylabel('Total Distance (meters)')
    plt.legend(loc='best')
    plt.grid(True)
    plt.savefig('cvrptw_comparison.png')
    plt.show()

    best_result = min(results, key=lambda x: (x[2], x[3]))  # Ordena por distância e, em caso de empate, por tempo
    best_result_msg = f'\nBest result: Strategy: {best_result[0]}, Heuristic: {best_result[1]}, Total Distance: {best_result[2]}, Computation Time: {best_result[3]} seconds'
    print(best_result_msg)
    logging.info(best_result_msg)

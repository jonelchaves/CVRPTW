# Função para logging de resultados de simulações

import csv
import json
import os

def log_simulation(params, results, phase):
    """
    Loga os resultados da simulação em um arquivo CSV e opcionalmente em um arquivo JSON, separados por fase.

    Args:
        params (dict): Dicionário com os parâmetros da simulação.
        results (list of tuples): Lista de resultados da simulação.
        phase (str): Identificador da fase da simulação (e.g., "Uniform Distribution & Rigorous Time Windows").
    """
    # Define o nome do arquivo CSV com base na fase
    log_file = f'cvrptw_results_{phase.replace(" ", "_")}.csv'

    # Se o arquivo não existir, cria com cabeçalho
    if not os.path.isfile(log_file):
        with open(log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Strategy', 'Heuristic', 'Total Distance', 'Computation Time'])

    # Adiciona os resultados ao arquivo CSV
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        for result in results:
            writer.writerow(result)

    # Opcional: salvar detalhes adicionais em um arquivo JSON com base na fase
    json_file = f'cvrptw_simulation_details_{phase.replace(" ", "_")}.json'
    with open(json_file, 'w') as f:
        json.dump({"parameters": params, "results": results}, f, indent=4)


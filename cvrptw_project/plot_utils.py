# Funções para visualização (gráficos)
import matplotlib.pyplot as plt

def plot_routes(data, manager, routing, solution):
    """
    Plota as rotas dos veículos em um gráfico e identifica os clientes.

    Args:
        data (dict): Dicionário contendo os dados do problema.
        manager (pywrapcp.RoutingIndexManager): Gerenciador de índices de rotas.
        routing (pywrapcp.RoutingModel): Modelo de roteamento.
        solution (pywrapcp.Assignment): Solução encontrada pelo solver.
    """
    plt.figure(figsize=(12, 10))

    # Itera sobre cada veículo e plota suas rotas
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))

        # Obter coordenadas de longitude e latitude
        x = [data['locations'][i][1] for i in route]
        y = [data['locations'][i][0] for i in route]

        # Plota a rota do veículo
        plt.plot(x, y, 'o-', markersize=8, label=f'Vehicle Route {vehicle_id + 1}')

        # Adiciona o identificador dos clientes (número do nó) ao lado dos pontos
        for i, (xi, yi) in enumerate(zip(x, y)):
            plt.text(xi, yi, str(route[i]), fontsize=12, ha='right')

    # Destacar o depot em vermelho e com tamanho maior
    plt.scatter([data['locations'][0][1]], [data['locations'][0][0]], color='red', label='Depot', marker='s', s=100,
                zorder=5)
    plt.text(data['locations'][0][1], data['locations'][0][0], 'Depot', fontsize=12, ha='right', color='red')

    plt.title('Vehicle Routes with Customer Identification')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()


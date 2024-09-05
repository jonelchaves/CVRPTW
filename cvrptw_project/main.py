# Arquivo principal que roda o programa
from config import setup_logging
from solver import solve_cvrptw

if __name__ == '__main__':
    setup_logging()

    # Solução com clientes uniformemente distribuídos e janelas de tempo rigorosas
    print("Uniform Distribution & Rigorous Time Windows")
    solve_cvrptw(distribution='uniform', time_window_type='rigorous')

    # Solução com clientes em clusters e janelas de tempo rigorosas
    print("\nClustered Distribution & Rigorous Time Windows")
    solve_cvrptw(distribution='clusters', time_window_type='rigorous')

    # Solução com clientes uniformemente distribuídos e janelas de tempo relaxadas
    print("\nUniform Distribution & Relaxed Time Windows")
    solve_cvrptw(distribution='uniform', time_window_type='relaxed')

    # Solução com clientes em clusters e janelas de tempo relaxadas
    print("\nClustered Distribution & Relaxed Time Windows")
    solve_cvrptw(distribution='clusters', time_window_type='relaxed')

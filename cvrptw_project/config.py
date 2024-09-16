# Configuração e setup de logging
import logging

def setup_logging():
    """
    Configura o logging com o formato desejado.
    """
    logging.basicConfig(
        filename='cvrptw_simulation.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Logging setup complete.")
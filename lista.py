import subprocess
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from functions import readFile

def lista():
    try:
        num_servidores = readFile("servers.txt")
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.")
        return

    logger.info("Lista de contenedores:")
    subprocess.run(["lxc", "list"])

    logger.info("Lista de redes:")
    subprocess.run(["lxc", "network", "list"])

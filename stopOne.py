import subprocess
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import isRunning
from functions import exists

def stopOne(nombre):
    logger.info("Parando servidor " + nombre)

    if not exists(nombre):
        logger.error("Error: el servidor " + nombre + " no existe.")
        return
    if not isRunning(nombre):
        logger.error("Error: el servidor ya está detenido.")
        return
    
    subprocess.run(["lxc", "stop", nombre])
    logger.info(nombre + " parado correctamente")

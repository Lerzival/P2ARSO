import subprocess
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import isRunning
from functions import exists

def startOne(nombre):
    logger.info("Arrancando servidor " + nombre)
    if not exists(nombre):
        logger.error("Error: el servidor " + nombre + " no existe.")
        return
    
    if isRunning(nombre):
        logger.error("Error: el servidor ya está arrancado.")
        return
  
    subprocess.run(["lxc", "start", nombre])
    subprocess.Popen(["xterm", "-e", "lxc exec " + nombre + " bash"])
    logger.info(nombre + " iniciado correctamente")

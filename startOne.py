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
    respuesta = subprocess.run(["lxc", "info", nombre], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc,   
    if isRunning(nombre):
        logger.error("Error: el servidor ya está arrancado.")
        return
    elif respuesta.stderr:
        logger.error("Algo ha salido mal (seguramente el servidor " + nombre + " no exista).")
        return 
    
    subprocess.run(["lxc", "start", nombre])
    subprocess.Popen(["xterm", "-e", "lxc exec " + nombre + " bash"])
    logger.info(nombre + " iniciado correctamente")

import subprocess
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile
from functions import writeFile
from functions import exists
from functions import isRunning

def deleteOne(nombre):
    logger.info("Borrando servidor " + nombre)
    try:
        num_servidores = readFile("servers.txt")
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.")
        return

    if num_servidores == 0:
        logger.error("Error: no hay servidores para borrar.")
        return
    
    if not exists(nombre):
        logger.error("El servidor " + nombre + " no existe.")
        return 
    
    if isRunning(nombre):
        logger.info("Parando " + nombre)
        subprocess.run(["lxc", "stop", nombre])

    logger.info("Eliminando asignación de IP de " + nombre)


    respuesta0 = subprocess.run(["lxc", "network", "detach", "lxdbr0", nombre], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc, https://docs.python.org/es/3/library/sys.html    
   
    if respuesta0.returncode == 0:
        logger.info("Desconectado de lxdbr0")
    
    respuesta1 = subprocess.run(["lxc", "network", "detach", "lxdbr1", nombre], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc, https://docs.python.org/es/3/library/sys.html    
   
    if respuesta1.returncode == 0:
        logger.info("Desconectado de lxdbr1")
    

    subprocess.run(["lxc", "delete", nombre])
    logger.info(nombre + " borrado correctamente")

    writeFile("servers.txt", num_servidores - 1)
 

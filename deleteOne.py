import subprocess
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile
from functions import writeFile

def deleteOne(nombre):
    logger.info("Borrando servidor " + nombre)
    try:
        num_servidores = readFile()
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.")
        return

    if num_servidores == 0:
        logger.error("Error: no hay servidores para borrar.")
        return

    
    respuesta = subprocess.run(["lxc", "info", nombre], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc, https://docs.python.org/es/3/library/sys.html 
    if respuesta.stderr:
        logger.error("El servidor " + nombre + " no existe.")
        return 
    

    subprocess.run(["lxc", "delete", nombre, "--force"])
    logger.info(nombre + " borrado correctamente")

    writeFile(num_servidores - 1)
 

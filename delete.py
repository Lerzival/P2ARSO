import subprocess
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile
from functions import writeFile

def delete():
    try:
        num_servidores = readFile() 
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.") # Comprueba que los contenedores existan para poder eliminarlos
        return

    logger.info("Eliminando servidores")
   

    # Elimina contenedores
    for i in range(1, 6):
        nombre = "s" + str(i)
        respuesta = subprocess.run(["lxc", "info", nombre], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc, https://docs.python.org/es/3/library/sys.html 
        if not respuesta.stderr:
            logger.info("Eliminando " + nombre)
            subprocess.run(["lxc", "delete", nombre, "--force"])


    # Elimina lb y c1
    for nombre in ["lb", "c1", "db"]:
        logger.info("Eliminando " + nombre)
        subprocess.run(["lxc", "delete", nombre, "--force"])

    logger.info("Escenario eliminado") 

    writeFile(" ") # Vaciamos el fichero de configuración

    logger.info("Fichero de configuración vaciado correctamente")

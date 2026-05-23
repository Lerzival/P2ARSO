import subprocess
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile
from functions import writeFile
from functions import exists
from functions import isRunning

def delete():
    try:
        num_servidores = readFile("servers.txt") 
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.") # Comprueba que los contenedores existan para poder eliminarlos
        return

    logger.info("Eliminando servidores")
   
    # Elimina contenedores
    for i in range(1, 6):
        nombre = "s" + str(i)
        if exists(nombre):
            logger.info("Eliminando " + nombre)
            if isRunning(nombre):
                logger.info("El servidor " + nombre + " está arrancado. Parando " + nombre)
                subprocess.run(["lxc", "stop", nombre])

            subprocess.run(["lxc", "delete", nombre])
            logger.info("Eliminado " + nombre)


    # Elimina lb y c1
    for nombre in ["lb", "c1", "db"]:
        logger.info("Eliminando " + nombre)
        if isRunning(nombre):
                logger.info("El servidor " + nombre + " está arrancado. Parando " + nombre)
                subprocess.run(["lxc", "stop", nombre])
        subprocess.run(["lxc", "delete", nombre])

   # Elimina las comunicaciones
    logger.info("Eliminando lxdbr1")
    subprocess.run(["lxc", "network", "delete", "lxdbr1"])
    

    logger.info("Escenario eliminado") 

    writeFile("servers.txt", " ") # Vaciamos el fichero de configuración
    writeFile("configuration.txt", "0")

    logger.info("Fichero de configuración vaciado correctamente")

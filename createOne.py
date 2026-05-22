import subprocess
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile
from functions import writeFile import preparar_imagen_base

def createOne():
    preparar_imagen_base()
    logger.info("Creando un nuevo servidor")
    
    try:
        num_servidores = readFile() 
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.") # Comprueba que los contenedores existan para poder eliminarlos
        return


    num_servidores = int(readFile())
    if num_servidores >= 5:
        logger.error("Error: ya hay 5 servidores. No se pueden crear más.")
        return

    indiceserver= 1
    noCreado = True
    while noCreado:
        
        nombre = "s" + str(indiceserver)
        
        respuesta = subprocess.run(["lxc", "info", nombre], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc, https://docs.python.org/es/3/library/sys.html    
        if not respuesta.stderr:
            logger.error("El servidor " + nombre + " ya existe. Probando el siguiente.")
            indiceserver += 1
            continue
        
        noCreado = False
        

    subprocess.run(["lxc", "init", "base-arso", nombre])
    subprocess.run(["lxc", "network", "attach", "lxdbr0", nombre, "eth0"])
    subprocess.run(["lxc", "config", "device", "set", nombre, "eth0", "ipv4.address", "134.3.0.1" + str(indiceserver)])
    
    writeFile(str(num_servidores + 1))

    logger.info(nombre + " creado correctamente")

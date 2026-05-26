import subprocess
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def readFile (ruta):
    try:
        with open(ruta, "r") as fich:
            texto = int(fich.read().strip()) 
        return texto
    except Exception as e:
        logger.error("Algo ha salido mal con la lectura del archivo " + ruta)
        raise e

def writeFile (ruta, texto):
    try:
        with open(ruta, "w") as fich:
            fich.write(str(texto))
    except:
        logger.error("Error: algo ha fallado al escribir el fichero.")
        return

def exists (nomServer): 
    
    respuesta = subprocess.run(["lxc", "info", nomServer], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc, https://docs.python.org/es/3/library/sys.html    
   
    if respuesta.returncode == 0: #si el comando se ejecuta correctamente, el servidor existe     
        return True
    
    return False
    
def imageExists (image): 
    
    respuesta = subprocess.run(["lxc", "image", "info", image], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc, https://docs.python.org/es/3/library/sys.html    
   
    if not respuesta.stderr:
        return True
    
    return False

def isRunning (nomServer): 
    
    respuesta = subprocess.run(["lxc", "info", nomServer], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Código deducido a partir del código proporcionado por el profesior y las siguientes páginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc,   

    return "Status: RUNNING" in respuesta.stdout.decode("utf-8")
   
def importImage():
    alias = "base-arso"
    ruta = "./arso25-p2.tar.gz" 

    logger.info(f"Verificando el estado de la imagen '{alias}'")

    if imageExists(alias):
        logger.info(f"La imagen '{alias}' ya está instalada. Omitiendo importación.")
    else:
        logger.info(f"Imagen no encontrada. Importando desde {ruta}")
        
        #Si no existe la importamos.
        importacion = subprocess.run(["lxc", "image", "import", ruta, "--alias", alias])

        if importacion.returncode == 0:
            logger.info("Imagen importada correctamente.")
        else:
            logger.error("Fallo al importar la imagen.")
            logger.error(f"Por favor, asegúrate de que el archivo '{ruta}' se encuentra en la misma carpeta que este script.")
    
def getName():
    respuesta = subprocess.run(["hostname"], stdout=subprocess.PIPE) #hostname devuelve el numero del ordenador del lab 
    return respuesta.stdout.decode("utf-8").strip()


def obtenerIP(numOrdenador):
    nombreRed = numOrdenador + ".lab.dit.upm.es"
    respuesta = subprocess.run(["dig", "+short", "+noauthority", "+noadditional", nombreRed], stdout=subprocess.PIPE) #short devuelve una respuesta mas corta con solo la ip, demas codigo proporcionado en laboratorios
    ip = respuesta.stdout.decode("utf-8").strip()
    return ip

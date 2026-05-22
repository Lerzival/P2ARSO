import subprocess
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def readFile ():
    try:
        with open("servers.txt", "r") as fich:
            num_servidores = int(fich.read().strip())
        return num_servidores # He puesto esto porque no nos devolvía nada la lectura
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.")
        return None

def writeFile (num_servidores):
    try:
        with open("servers.txt", "w") as fich:
            fich.write(str(num_servidores))
    except:
        logger.error("Error: algo ha fallado al escribir el fichero.")
        return

def exists (nomServer): 
    
    respuesta = subprocess.run(["lxc", "info", nomServer], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc, https://docs.python.org/es/3/library/sys.html    
   
    if not respuesta.stderr:
        return True
    
    return False
    # Yo eliminaría las líneas de la 27 a la 30 y pondría la siguiente
    # return respuesta.returncode == 0
    # habría que buscar una página que lo justifique, porque simplemente conozco la función
    # el propio subprocess.run nos devuelve un número, si es 0, es true, y sino es 0 es false, por lo que esa comprobación bastaría

# Gaizka: He metido una función de comprobacion de imagen como hacemos la del contenedor
# Si al final lo hacemos con returncode (como propones celia arriba) habria que cambiarlo
def imageExists (image): 
    
    respuesta = subprocess.run(["lxc", "image", "info", image], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #codigo deducido a partir del codigo proporcionado por el profesior y las siguientes paginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc, https://docs.python.org/es/3/library/sys.html    
   
    if not respuesta.stderr:
        return True
    
    return False

def isRunning (nomServer): 
    
    respuesta = subprocess.run(["lxc", "info", nomServer], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Código deducido a partir del código proporcionado por el profesior y las siguientes páginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc,   

    return "Status: RUNNING" in respuesta.stdout.decode("utf-8")
    # Aquí he eliminado el if, aunque muy bien puesto, un return con una expresión booleana ya nos da true o false, nos ahorramos líneas de código
    # sí, Gaizka, me cobran por escribir más

 def preparar_imagen_base():
    alias_imagen = "base-arso"
    ruta_archivo = "./arso25-p2.tar.gz" 

    logger.info(f"Verificando el estado de la imagen '{alias_imagen}'...")

    if imageExists(alias_imagen):
        logger.info(f"La imagen '{alias_imagen}' ya está instalada. Omitiendo importación.")
    else:
        logger.info(f"Imagen no encontrada. Importando desde {ruta_archivo}")
        
        #Si no existe la importamos.
        importacion = subprocess.run(["lxc", "image", "import", ruta_archivo, "--alias", alias_imagen])

        if importacion.returncode == 0:
            logger.info("Imagen importada correctamente.")
        else:
            logger.error("Fallo al importar la imagen.")
            logger.error(f"Por favor, asegúrate de que el archivo '{ruta_archivo}' se encuentra en la misma carpeta que este script.")
    

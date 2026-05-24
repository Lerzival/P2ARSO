import subprocess
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import exists
from functions import isRunning

def getDbIP():
    with open("dbIP.txt", "r") as f:
        ip = f.read().strip() # No usamos la función readFile porque devuelve un int que necesitamos para start 
    return ip # Nos devuelve la IP guardada en dbIP.txt 

def configureOne(nombre): 
    #NO TIENE EN CUENTA SI SE INTENTA HACER UNA CONFIGURACIÓN DE UN SERVIDOR YA CONFIGURADO

    if not isRunning(nombre):
        logger.info(nombre + " no está arrancado. No se puede realizar la configuración")
        return

    logger.info(f"Configurando {nombre}")

    #Copiar el fichero de instalación en el contenedor
    subprocess.run(["lxc", "file", "push", "install.sh", f"{nombre}/root/install.sh"])

    #Cambiar permisos de ejecución
    subprocess.run(["lxc", "exec", nombre, "--", "chmod", "+x", "install.sh"])

    # Copiar ficheros de la aplicación web al contenedor
    subprocess.run(["lxc", "file", "push", "-r", "app.tar.gz", f"{nombre}/root/"])

    #Descomprimir el fichero TAR
    subprocess.run(["lxc", "exec", nombre, "--", "tar", "-oxvf", "/root/app.tar.gz"])

    dbIP = getDbIP() # Guardamos la IP como variable   

    #Sustituir la IP antigua
    subprocess.run(["lxc", "exec", nombre, "--", "sed", "-i", "s/10.0.0.20/{dbIP}/g", "/root/app/md-seed-config.js"])
    subprocess.run(["lxc", "exec", nombre, "--", "sed", "-i", "s/10.0.0.20/{dbIP}/g", "/root/app/rest_server.js"])

    #Ejecutar la instalación a través del fichero install.sh
    subprocess.run(["lxc", "exec", nombre, "--", "/root/install.sh"])

    #Reiniciar el contenedor para completar la instalación
    logger.info(f"Reiniciando {nombre} para aplicar los cambios de instalación")
    subprocess.run(["lxc", "restart", nombre])
    time.sleep(10) 

    #Lanzar la aplicación web usando forever
    logger.info(f"Arrancando aplicación en {nombre}")
    subprocess.run(["lxc", "exec", nombre, "--", "forever", "start", "/root/app/rest_server.js"])
    time.sleep(5)
    
    logger.info("Configuración de " + nombre + " completada con éxito.")

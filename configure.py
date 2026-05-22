import subprocess
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile

def configure(): 

    logger.info("Configurando MongoDB...")

    # MONGODB YA INSTALADO EN LA IMAGEN 

    # Editamos fichero de configuración de mongo para asignar la IP
    subprocess.run([
        "lxc", "exec", "db", "--",
        "sed", "-i", "s/bind_ip = 127.0.0.1/bind_ip = 127.0.0.1,134.3.0.20/", "/etc/mongodb.conf"
    ])

    # reiniciamos
    subprocess.run(["lxc", "exec", "db", "--", "systemctl", "restart", "mongodb"])

    time.sleep(10) 


    logger.info("MongoDB configurado")


    # configuramos haproxy
    logger.info("Configurando Haproxy...")
    
    subprocess.run(["lxc", "exec", "lb", "--", "apt", "update"])
    subprocess.run(["lxc", "exec", "lb", "--", "apt", "install", "-y", "haproxy"])

    # Empujamos el fichero y reiniciamos
    subprocess.run(["lxc", "file", "push", "haproxy.cfg", "lb/etc/haproxy/haproxy.cfg"])
    subprocess.run(["lxc", "exec", "lb", "--", "systemctl", "restart", "haproxy"])
    logger.info("Haproxy configurado")


    num_servidores = readFile()

    logger.info("Configurando servidores web...")
    
    logger.info(f"Configurando {num_servidores} servidores web")

    for i in range(1, int(num_servidores) + 1):
        nombre = f"s{i}"
        logger.info(f"Configurando {nombre}")

        #Copiar el fichero de instalación en el contenedor
        subprocess.run(["lxc", "file", "push", "install.sh", f"{nombre}/root/install.sh"])

        #Cambiar permisos de ejecución
        subprocess.run(["lxc", "exec", nombre, "--", "chmod", "+x", "install.sh"])

        # Copiar ficheros de la aplicación web al contenedor
        subprocess.run(["lxc", "file", "push", "-r", "app.tar.gz", f"{nombre}/root/"])

        #Descomprimir el fichero TAR
        subprocess.run(["lxc", "exec", nombre, "--", "tar", "-oxvf", "/root/app.tar.gz"])

        #Sustituir la IP antigua
        subprocess.run(["lxc", "exec", nombre, "--", "sed", "-i", "s/10.0.0.20/134.3.0.20/g", "/root/app/md-seed-config.js"])
        subprocess.run(["lxc", "exec", nombre, "--", "sed", "-i", "s/10.0.0.20/134.3.0.20/g", "/root/app/rest_server.js"])

        #Ejecutar la instalación a través del fichero install.sh
        subprocess.run(["lxc", "exec", nombre, "--", "/root/install.sh"])

        #Reiniciar el contenedor para completar la instalación
        logger.info(f"Reiniciando {nombre} para aplicar los cambios de instalación...")
        subprocess.run(["lxc", "restart", nombre])

        #Pausa de seguridad
        time.sleep(10) 

        #Lanzar la aplicación web usando forever
        logger.info(f"Arrancando aplicación en {nombre}...")
        subprocess.run(["lxc", "exec", nombre, "--", "forever", "start", "/root/app/rest_server.js"])
        
    logger.info("Configuración de todos los servidores completada con éxito.")

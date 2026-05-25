import subprocess
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile
from functions import exists
from functions import isRunning
from functions import writeFile
from functions import obtenerIP
from functions import getName


# ORDENADOR A

def configurationA(ipB):
    ipA = obtenerIP(getName())

    # Permitimos el acceso remoto 
    orden = ipA + ":8443"
    subprocess.run(["lxc", "config", "set", "core.https_address", orden])

    # Nos acreditamos
    orden2 = ipB + ":8443"
    subprocess.run(["lxc", "remote", "add", "remoto", orden2, "--password", "mypass", "--accept-certificate"])

    # Configuramos el bridge remoto
    subprocess.run(["lxc", "network", "set", "remoto:lxdbr0", "ipv4.address", "134.3.0.1/24"])
    subprocess.run(["lxc", "network", "set", "remoto:lxdbr0", "ipv4.nat", "true"])

    # Copiar remotamente la db

    # CORRECCIÓN 1: bind_ip a 0.0.0.0
    subprocess.run([
        "lxc", "exec", "db", "--",
        "sed", "-i", "s/bind_ip = 127.0.0.1/bind_ip = 0.0.0.0/", "/etc/mongodb.conf"
    ])

    subprocess.run(["lxc", "stop", "db"])
    subprocess.run(["lxc", "copy", "db", "remoto:db"])
    
    # CORRECCIÓN 2: Forzar la IP del contenedor copiado antes de encender
    subprocess.run(["lxc", "config", "device", "override", "remoto:db", "eth0", "ipv4.address=134.3.0.20"])
    
    subprocess.run(["lxc", "start", "remoto:db"])

    # CORRECCIÓN 3: Esperar y reiniciar Mongo en el remoto AHORA que existe
    time.sleep(3)
    subprocess.run(["lxc", "exec", "remoto:db", "--", "systemctl", "restart", "mongodb"])

    # Creamos el proxy
    orden = "listen=tcp:0.0.0.0:27017"
    subprocess.run(["lxc", "config", "device", "add", "remoto:db", "miproxy", "proxy", orden, "connect=tcp:134.3.0.20:27017"])

    time.sleep(10) 
    subprocess.run(["lxc", "delete", "db", "--force"])

# ORDENADOR B

def configurationB():
    ipB = obtenerIP(getName())

    # Permitimos el acceso remoto 
    orden = ipB + ":8443"
    subprocess.run(["lxc", "config", "set", "core.https_address", orden])

    # Acreditación
    subprocess.run(["lxc", "config", "set", "core.trust_password", "mypass"])

    print(ipB)


def configureRemoto(ipB): 

    # configuramos haproxy
    logger.info("Configurando Haproxy")
    
    subprocess.run(["lxc", "exec", "lb", "--", "apt", "update"])
    subprocess.run(["lxc", "exec", "lb", "--", "apt", "install", "-y", "haproxy"])

    # Empujamos el fichero y reiniciamos
    subprocess.run(["lxc", "file", "push", "haproxy.cfg", "lb/etc/haproxy/haproxy.cfg"])
    subprocess.run(["lxc", "exec", "lb", "--", "systemctl", "restart", "haproxy"])
    logger.info("Haproxy configurado")

    try:
        num_servidores = readFile("servers.txt")
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.")
        return

    nombres = []
    for i in range (1, num_servidores + 5):
        if exists (f"s{i}"):
            nombres += [f"s{i}"]

    logger.info("Configurando servidores web remotamente")
    
    logger.info(f"Configurando {num_servidores} servidores web remotamente")


    for nombre in nombres:
        
        logger.info(f"Configurando {nombre} remotamente")

        #Copiar el fichero de instalación en el contenedor
        subprocess.run(["lxc", "file", "push", "install.sh", f"{nombre}/root/install.sh"])

        #Cambiar permisos de ejecución
        subprocess.run(["lxc", "exec", nombre, "--", "chmod", "+x", "/root/install.sh"])

        # Copiar ficheros de la aplicación web al contenedor
        subprocess.run(["lxc", "file", "push", "-r", "app.tar.xz", f"{nombre}/root/"])

        #Descomprimir el fichero TAR
        subprocess.run(["lxc", "exec", nombre, "--", "tar", "-oxvf", "/root/app.tar.xz"])

        print(f"ipB = {repr(ipB)}")
        
        # CORRECCIÓN 4: Quitamos los sed y ejecutamos inyectando la variable MONGO_URL
        subprocess.run(["lxc", "exec", nombre, "--", "bash", "-c", f"cd /root && export MONGO_URL='mongodb://{ipB}:27017/bio_bbdd' && ./install.sh"])

        #Reiniciar el contenedor para completar la instalación
        logger.info(f"Reiniciando {nombre} para aplicar los cambios de instalación")
        subprocess.run(["lxc", "restart", nombre])
        time.sleep(10) 

        # Lanzar la aplicación web usando forever (Inyectando la IP)
        logger.info(f"Arrancando aplicación en {nombre}")
        subprocess.run(["lxc", "exec", nombre, "--", "bash", "-c", f"cd /root && export MONGO_URL='mongodb://{ipB}:27017/bio_bbdd' && forever start app/rest_server.js"])
        time.sleep(10)
    
    writeFile("configuration.txt", "1") 
        
    logger.info("Configuración remota de todos los servidores completada con éxito.")
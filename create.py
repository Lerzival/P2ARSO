import subprocess
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import writeFile
from importarImagen import preparar_imagen_base

def create(num_servidores):

    preparar_imagen_base()
    logger.info("Creando " + str(num_servidores) + " servidores")

    # Crear redes
    subprocess.run([
        "lxc", "network", "set", "lxdbr0", 
        "ipv4.address=134.3.0.1/24",
        "ipv4.nat=true",
        "ipv6.nat=false",
        "ipv6.address=none",
        "dns.domain=lxd",
        "dns.mode=none"
    ]) 
    logger.info("lxdbr0 creado correctamente")

    subprocess.run([
        "lxc", "network", "create", "lxdbr1",
        "ipv4.address=134.3.1.1/24",
        "ipv4.nat=true",
        "ipv6.nat=false",
        "ipv6.address=none",
        "dns.domain=lxd",
        "dns.mode=none"
    ]) 
    logger.info("lxdbr1 creado correctamente")

    # Crear contenedores
    for i in range(1, num_servidores + 1):
        nombre = "s" + str(i)
        logger.info("Creando " + nombre)

        subprocess.run(["lxc", "init", "base-arso", nombre])
        subprocess.run(["lxc", "network", "attach", "lxdbr0", nombre, "eth0"])
        subprocess.run(["lxc", "config", "device", "set", nombre, "eth0", "ipv4.address", "134.3.0.1" + str(i)])

    logger.info("Creando lb:")
    subprocess.run(["lxc", "init", "base-arso", "lb"])
    logger.info("lb creado correctamente. Asignando redes:")
    subprocess.run(["lxc", "network", "attach", "lxdbr0", "lb", "eth0"])
    subprocess.run(["lxc", "network", "attach", "lxdbr1", "lb", "eth1"])
    logger.info("Redes asignadas correctamente. Configurando IPs:")
    subprocess.run(["lxc", "config", "device", "set", "lb", "eth0", "ipv4.address", "134.3.0.10"])
    subprocess.run(["lxc", "config", "device", "set", "lb", "eth1", "ipv4.address", "134.3.1.10"])
    logger.info("IPs configuradas correctamente")

    # Crear c1
    logger.info("Creando c1:")
    subprocess.run(["lxc", "init", "base-arso", "c1"])
    subprocess.run(["lxc", "network", "attach", "lxdbr1", "c1", "eth0"])
    logger.info("Cliente c1 creado correctamente")

    # Crear db
    logger.info("Creando db:")
    subprocess.run(["lxc", "init", "base-arso", "db"])
    subprocess.run(["lxc", "network", "attach", "lxdbr0", "db", "eth0"])
    subprocess.run([
        "lxc", "config", "device", "set",
        "db", "eth0", "ipv4.address", "134.3.0.20"
    ])


    # Fichero que guarda la info
    writeFile(num_servidores)
    logger.info("Contenedores creados (ejecutar start para arrancarlos)")

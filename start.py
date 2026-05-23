import subprocess
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile
from functions import isRunning
from functions import exists

def start():
    try:
        num_servidores = readFile("servers.txt")
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.")
        return

    logger.info("Arrancando contenedores")

    nombres = ["lb","c1","db"]
    for i in range (1, num_servidores + 5):
        if exists (f"s{i}"):
            nombres += [f"s{i}"]

    for nombre in nombres:
        
        if not exists(nombre):
            logger.info(nombre + " no existe")
            continue
        
        if isRunning(nombre):
            logger.info(nombre + " ya está arrancado")
            continue
        
        logger.info("Arrancando " + nombre)
        subprocess.run(["lxc", "start", nombre])
        
        # Mostramos las consolas de las máquinas virtuales 
        subprocess.Popen(["xterm", "-e", "lxc exec " + nombre + " bash"]) 
        logger.info(nombre + " arrancado correctamente")

    logger.info("editando lb para configurar eth1")

    # Código indicado por Oscar Araque
    eth1_in = False
    while not eth1_in:
        time.sleep(3)
        logger.info("subiendo 50-cloud-init.yaml a lb")
        subprocess.call(["lxc", "file", "push", "./50-cloud-init.yaml", "lb/etc/netplan/50-cloud-init.yaml"])
        time.sleep(2)
        logger.info("comprobando que eth1 se ha añadido correctamente a lb")
        respuesta = subprocess.run(["lxc", "exec", "lb", "--", "cat", "/etc/netplan/50-cloud-init.yaml"], stdout=subprocess.PIPE)
        eth1_in = "eth1" in respuesta.stdout.decode("utf-8")
            
    # Reiniciamos el contenedor para que se muestren los cambios
    logger.info("restart de lb")
    subprocess.run(["lxc", "stop", "lb"])
    subprocess.run(["lxc", "start", "lb"])
    logger.info("lb reiniciado correctamente")
    subprocess.Popen(["xterm", "-e", "lxc exec " + "lb" + " bash"])
          
    logger.info("ESCENARIO ARRANCADO")

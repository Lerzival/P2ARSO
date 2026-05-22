import subprocess
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile
from functions import isRunning

def start():
    try:
        num_servidores = readFile()
    except:
        logger.error("Error: no existe la red. Ejecuta 'create' primero.")
        return

    logger.info("Arrancando contenedores")

    nombres = [f"s{i}" for i in range(1, num_servidores + 1)] 
    nombres += ["lb","c1","db"]

    for nombre in nombres:
        respuesta = subprocess.run(["lxc", "info", nombre], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Código deducido a partir del código proporcionado por el profesior y las siguientes páginas: https://dev.to/waylonwalker/read-stderr-from-python-subprocesspopen-4kc, https://dev.to/hosni_zaaraoui/stdout-vs-stderr-vs-stdin-2fkc,   
        if respuesta.stderr:
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
    subprocess.run(["lxc", "restart", "lb"])
    logger.info("lb reiniciado correctamente")
    subprocess.Popen(["xterm", "-e", "lxc exec " + "lb" + " bash"])
          
    logger.info("ESCENARIO ARRANCADO")

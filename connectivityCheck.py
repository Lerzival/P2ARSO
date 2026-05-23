import subprocess
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile
from functions import exists

def connectivityCheck():   
    if not exists("servers.txt"):
        logger.error("Error: no existe la red. Ejecuta 'create' primero.")
        return
    logger.info("Comprobando conectividad con lb:")
    subprocess.run(["lxc", "exec", "c1", "--", "ping", "-c", "2", "134.3.1.10"]) # Ping a lb desde c1
    
    num_servidores = int(readFile("servers.txt"))
    for i in range(1, num_servidores + 1): 
        logger.info("Comprobando conectividad con s" + str(i))
        subprocess.run(["lxc", "exec", "c1", "--", "ping", "-c", "2",  "134.3.0.1" + str(i)])
        
#Somos conscientes de que en un escenario real, la transparencia del balanceador haria que no fuese necesario que el 
#cliente supiera las IPs de los servidores. Realizamos la prueba de forma puramente informativa, para asegurarnos 
#de que todo está llegando y funcionando.

# Celia García de Muro Fernández
# Miguel Jaime Colomo Fernández
# Gaizka Lavado Tallada

import sys
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from create import create 
from start import start
from lista import lista
from delete import delete
from createOne import createOne
from startOne import startOne
from deleteOne import deleteOne
from stopOne import stopOne
from connectivityCheck import connectivityCheck
from configure import configure


def main():
    if len(sys.argv) < 2:
        logger.error("Error: falta comando (create, start, list, delete, createOne, startOne, deleteOne, stopOne)") #Compruebo que están todos los datos pedidos
        return

    orden = sys.argv[1]

    if orden == "create":
        if len(sys.argv) > 3:
            logger.error("Error: demasiados parámetros") #Compruebo que no hay comandos de más
            return

        num_servidores = 2  #Valor default

        if len(sys.argv) == 3:
            try:
                num_servidores = int(sys.argv[2])
            except ValueError:
                logger.error("Error: especificar el número de servidores como un número entero") #Compruebo que el segundo argumento sea un número
                return

        if num_servidores < 1 or num_servidores > 5:
            logger.error("Error: el número de servidores debe estar entre 1 y 5") #Compruebo que el num de contenedores sea entre 1 y 5
            return

        create(num_servidores)

    elif orden in ["start", "list", "delete", "createOne", "connectivityCheck", "configure"]:
        if len(sys.argv) != 2:
            logger.error("Error: la orden " + orden +  "no acepta parámetros") #Comprobar que en start, lista y delete no se dan parámetros, solo en create
            return

        if orden == "start":
            start()
        elif orden == "list":
            lista()
        elif orden == "delete":
            delete()
        elif orden == "createOne":
            createOne()
        elif orden == "connectivityCheck":
            connectivityCheck()
        elif orden == "configure":
            configure()
    elif orden in ["startOne", "deleteOne", "stopOne"]:
        if len(sys.argv) != 3:
            logger.error("Error: la orden " + orden + " requiere el nombre del servidor") 
            return
        
        nombre = sys.argv[2]
        if nombre not in ["s1", "s2", "s3", "s4", "s5"]:
            logger.error("Error: el nombre del servidor debe ser s1, s2, s3, s4 o s5") 
            return

        if orden == "startOne":
            startOne(nombre)
        elif orden == "deleteOne":
            deleteOne(nombre)
        elif orden == "stopOne":
            stopOne(nombre)

    else:
        logger.error("Error: comando no válido") # Devolver porque no hay suficientes parámetros


if __name__ == "__main__":
    main()

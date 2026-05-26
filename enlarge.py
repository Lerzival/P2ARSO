from createOne import createOne
from startOne import startOne
from configureOne import configureOne
from functions import readFile

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def enlarge():

   if readFile("configuration.txt") == 0:
      logger.error("Para ejecutar enlarge es necesario configurar los servidores.")
      return

   # Crear servidor 
   logger.info("Creando nuevo servidor")
   server = createOne()
   logger.info(f"{server} creado")

   # Iniciarlo 
   startOne(server)
   logger.info(f"{server} arrancado")

   # Configurarlo 
   configureOne(server)
   logger.info(f"{server} configurado")
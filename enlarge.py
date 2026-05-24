from createOne import createOne
from startOne import startOne
from configureOne import configureOne

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def enlarge():

   # Crear servidor 
    logger.info("Creando nuevo servidor...")
    server = createOne()
    logger.info(f"{server} creado")

   # Iniciarlo 
    startOne(server)
    logger.info(f"{server} arrancado")

   # Configurarlo 
    configureOne(server)
    logger.info(f"{server} configurado")

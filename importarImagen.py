import subprocess
import logging
from functions import imageExists 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preparar_imagen_base():
    alias_imagen = "base-arso"
    ruta_archivo = "./arso25-p2.tar.gz" 

    logger.info(f"Verificando el estado de la imagen '{alias_imagen}'...")

    if imageExists(alias_imagen):
        logger.info(f"La imagen '{alias_imagen}' ya está instalada. Omitiendo importación.")
    else:
        logger.info(f"Imagen no encontrada. Importando desde {ruta_archivo}")
        
        #Si no existe la importamos.
        importacion = subprocess.run(["lxc", "image", "import", ruta_archivo, "--alias", alias_imagen])

        if importacion.returncode == 0:
            logger.info("Imagen importada correctamente.")
        else:
            logger.error("Fallo al importar la imagen.")
            logger.error(f"Por favor, asegúrate de que el archivo '{ruta_archivo}' se encuentra en la misma carpeta que este script.")
    
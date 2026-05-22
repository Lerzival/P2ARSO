import subprocess
import logging

# Aseguramos que el logger está configurado si se llama de forma independiente
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preparar_imagen_base():
    alias_imagen = "base-arso"
    ruta_archivo = "./arso25-p2.tar.gz" #TODO: hay que poner la ruta bien y completa, porque no la podemos incluir aquí  

    logger.info(f"Verificando el estado de la imagen '{alias_imagen}'...")

    # 1. Comprobamos si la imagen ya existe. 
    # Usamos capture_output=True para que el error natural de LXC 
    # (si no la encuentra) no se imprima y ensucie la terminal del usuario.
    comprobacion = subprocess.run(
        ["lxc", "image", "info", alias_imagen],
        capture_output=True,
        text=True
    )

    # El código de retorno 0 significa éxito (la imagen existe)
    if comprobacion.returncode == 0:
        logger.info(f"La imagen '{alias_imagen}' ya está instalada. Omitiendo importación.")
    else:
        logger.info(f"Imagen no encontrada. Importando desde {ruta_archivo} (esto puede tardar unos segundos)...")
        
        # 2. Si no existe, lanzamos la importación. Aquí sí queremos ver la salida
        # por si hay algún fallo catastrófico (ej. el archivo no existe).
        importacion = subprocess.run([
            "lxc", "image", "import", ruta_archivo, "--alias", alias_imagen
        ])

        if importacion.returncode == 0:
            logger.info("Imagen importada correctamente.")
        else:
            logger.error("Error crítico: Fallo al importar la imagen.")
            logger.error(f"Por favor, asegúrate de que el archivo '{ruta_archivo}' se encuentra en la misma carpeta que este script.")
            # Dependiendo de tu lógica, podrías lanzar un exit(1) aquí para detener el programa
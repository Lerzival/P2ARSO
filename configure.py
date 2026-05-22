import subprocess
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from functions import readFile

def configure(): 

    logger.info("Configurando MongoDB...")
    
    # Instalamos MongoDB obligatoriamente porque la imagen no lo trae
    subprocess.run(["lxc", "exec", "db", "--", "apt", "update"])
    subprocess.run([
        "lxc", "exec", "db", "--env", "--", 
        "apt", "install", "-y", "mongodb"
    ])

    # Abrimos la IP EXACTAMENTE como indica el PDF del Laboratorio 6.2
    subprocess.run([
        "lxc", "exec", "db", "--",
        "sed", "-i", "s/bind_ip = 127.0.0.1/bind_ip = 0.0.0.0/", "/etc/mongodb.conf"
    ])

    # Reiniciamos
    subprocess.run(["lxc", "exec", "db", "--", "systemctl", "restart", "mongodb"])

    logger.info("MongoDB configurado")


    # --- 2. CONFIGURACIÓN DE HAPROXY (lb) ---
    logger.info("Configurando HAProxy...")
    
    subprocess.run(["lxc", "exec", "lb", "--", "apt", "update"])
    subprocess.run([
        "lxc", "exec", "lb", "--", 
        "apt", "install", "-y", "haproxy"
    ])

    # Empujamos el fichero y reiniciamos
    subprocess.run([
        "lxc", "file", "push", "haproxy.cfg", "lb/etc/haproxy/haproxy.cfg"
    ])
    subprocess.run(["lxc", "exec", "lb", "--", "systemctl", "restart", "haproxy"])
    logger.info("HAProxy configurado")


    num_servidores = readFile()

    logger.info("Configurando servidores web...")
    
    logger.info(f"Configurando {num_servidores} servidores web...")

    for i in range(1, int(num_servidores) + 1):
        nombre = f"s{i}"
        logger.info(f"--- Configurando {nombre} ---")

        # 1. Copiar el fichero de instalación
        subprocess.run([
            "lxc", "file", "push", "install.sh", f"{nombre}/root/install.sh"
        ])

        # 2. Dar permisos de ejecución
        subprocess.run([
            "lxc", "exec", nombre, "--", "chmod", "+x", "/root/install.sh"
        ])

        # 3. Copiar el archivo comprimido de la aplicación web
        subprocess.run([
            "lxc", "file", "push", "app.tar.gz", f"{nombre}/root/"
        ])

        # 4. Descomprimir el fichero TAR
        subprocess.run([
            "lxc", "exec", nombre, "--", "bash", "-c", "cd /root && tar -oxvf app.tar.gz" 
        ])

        # 5. Sustituir la IP antigua tal y como pide el PDF de la Práctica 2
        subprocess.run([
            "lxc", "exec", nombre, "--", 
            "sed", "-i", "s/10.0.0.20/134.3.0.20/g", "/root/app/md-seed-config.js"
        ])
        
        # Opcional (por si la IP antigua estuviera también en rest_server.js)
        subprocess.run([
            "lxc", "exec", nombre, "--", 
            "sed", "-i", "s/10.0.0.20/134.3.0.20/g", "/root/app/rest_server.js"
        ])

        # 6. Ejecutar la instalación a través del fichero install.sh
        subprocess.run([
            "lxc", "exec", nombre, "--", "bash", "-c", "cd /root && ./install.sh"
        ])

        # 7. Reiniciar el contenedor para completar la instalación
        logger.info(f"Reiniciando {nombre} para aplicar los cambios de instalación...")
        subprocess.run([
            "lxc", "restart", nombre
        ])

        # Pausa de seguridad de 3 segundos
        time.sleep(3) 

        # 8. Lanzar la aplicación web usando forever
        logger.info(f"Arrancando aplicación en {nombre}...")
        subprocess.run([
            "lxc", "exec", nombre, "--", "bash", "-c", "cd /root && forever start app/rest_server.js"
        ])
        
    logger.info("Configuración de todos los servidores completada con éxito.")

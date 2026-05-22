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
        "lxc", "exec", "db","--", 
        "apt", "install", "-y", "mongodb"
    ])

    # Abrimos la IP 
    subprocess.run([
        "lxc", "exec", "db", "--",
        "sed", "-i", "s/bindIp: 127.0.0.1/bindIp: 0.0.0.0/", "/etc/mongodb.conf"
    ])

    # Reiniciamos
    subprocess.run(["lxc", "exec", "db", "--", "systemctl", "restart", "mongodb"])

    logger.info("MongoDB configurado")


    # --- 2. CONFIGURACIÓN DE HAPROXY (lb) ---
    logger.info("Configurando HAProxy...")
    
    # Instalamos HAProxy obligatoriamente
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

    # Si reiniciamos muchas cosas quizás rente hacer un módulo
    # que se llame reiniciar y reciba el nombre de lo que queremos
    # reiniciar como parámetro

    # Esto lo pongo porque sino no funciona la variable num_servidores
    # No sé si renta poner esto o simplemente ejecutarlo desde el main
    # donde sí existe la variable
    num_servidores = readFile()

    logger.info("Configurando servidores web...")
    # --- 3. CONFIGURACIÓN DE SERVIDORES WEB (s1, s2...) ---
    # IMPORTANTE: Asegúrate de tener 'import time' al principio de tu archivo configure.py
    
    # Asumiendo que has recuperado la variable num_servidores previamente
    logger.info(f"Configurando {num_servidores} servidores web...")

    for i in range(1, int(num_servidores) + 1):
        nombre = f"s{i}"
        logger.info(f"--- Configurando {nombre} ---")

        # 1. Copiar el fichero de instalación
        subprocess.run([
            "lxc", "file", "push", "install.sh", f"{nombre}/root/install.sh"
        ])

        # 2. Dar permisos de ejecución (usamos ruta absoluta por seguridad en LXC)
        subprocess.run([
            "lxc", "exec", nombre, "--", "chmod", "+x", "/root/install.sh"
        ])

        # 3. Copiar el archivo comprimido de la aplicación web
        subprocess.run([
            "lxc", "file", "push", "app.tar.gz", f"{nombre}/root/"
        ])

        # 4. Descomprimir el fichero TAR
        subprocess.run([
            "lxc", "exec", nombre, "--", "bash", "-c", "cd /root && tar -oxvf app.tar.gz"  #TODO: poner bien la ruta de la app porque no está en la ruta
        ])

        # 5. Ejecutar la instalación a través del fichero install.sh
        subprocess.run([
            "lxc", "exec", nombre, "--", "bash", "-c", "cd /root && ./install.sh"
        ])

        # 6. Reiniciar el contenedor para completar la instalación
        logger.info(f"Reiniciando {nombre} para aplicar los cambios de instalación...")
        subprocess.run([
            "lxc", "restart", nombre
        ])

        # Pausa de seguridad de 3 segundos para dar tiempo al contenedor a encender su red interna
        time.sleep(3) 

        # 7. Lanzar la aplicación web usando forever
        logger.info(f"Arrancando aplicación en {nombre}...")
        subprocess.run([
            "lxc", "exec", nombre, "--", "bash", "-c", "cd /root && forever start app/rest_server.js"
        ])
        
    logger.info("Configuración de todos los servidores completada con éxito.")


    # Dentro de este módulo podemos hacer varias funciones separadas para modular más
    # por ejemplo, configured, configuremongodb... quizás sea más fácil de leer y tal
    # si se modulariza, hay que cambiar el main

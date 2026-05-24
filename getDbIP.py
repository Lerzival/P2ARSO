def getDbIP():
    with open("dbIP.txt", "r") as f:
        ip = f.read().strip() # No usamos la función readFile porque devuelve un int que necesitamos para start 
    return ip # Nos devuelve la IP guardada en dbIP.txt 

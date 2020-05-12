# -*- coding: utf-8 -*-
# Autores: Cristian Sáez Mardones
# Fecha: 23-03-2020
# Versión: 1.5.5
# Objetivo: Mover archivos entre directorios y verificar que se realice correctamente

# Importación de archivo
    # No hay
# Importación de bibliotecas
    # Si hay
# Importación de funciones
    # No hay

# Biblioteca para el manejo de funciones del sistema operativo
import os
# Biblioteca para copiar archivos
import shutil
# Biblioteca para comparar archivos
import filecmp
# Biblioteca para el uso de funciones de tiempo
import time
# Biblioteca para el uso de funiones de fecha
import datetime
# Biblioteca para crear el logging
import logging

# Variable que almacena la hora en que se inicio el programa
tiempo_inicio = datetime.datetime.now()

# Ruta en donde se encuentra el script
ruta = os.path.dirname(os.path.abspath(__file__))
# Carpeta origen almacenada en el mismo directorio que el script
ruta_origen = os.path.join(ruta, 'origen')
# Carpeta destino almacenada en el mismo directorio que el script
ruta_destino = os.path.join(ruta, 'destino')
# Ruta en donde se encontraran los archivos log
ruta_log = os.path.join(ruta, 'log')

# Verificar todos los archivos en la carpeta
archivos = os.listdir(ruta_origen)

if len(archivos) > 0:
    print('Archivos en carpeta de origen:')
    for archivo in archivos:
        print(f'- {archivo}')
else:
    print('No hay archivos para copiar en la carpeta de origen')

print(end='\n')

# Ruta del archivo de log
archivo_log = os.path.join(ruta_log, f'log_{datetime.datetime.now().strftime("%Y%m%d")}.log')

with open(archivo_log, 'a') as log:
    log.write('==========================================================\
=================================================================\n')

# Configuración básica del log
logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s : %(levelname)s : %(message)s',
                    filename = archivo_log,
                    filemode = 'a')

time.sleep(2)

print('####   Inicio del script   ####')

previo = len(os.listdir(ruta_destino))

logging.debug('Iniciando la copia de archivos')
logging.debug(f'Se copiaran {len(archivos)} archivos')

for archivo in archivos:
    print('------------------------------------------')
    logging.info(f'Copiando archivo -> {archivo}')
    archivo = archivo.split('.')
    # Rutas de los archivos que se quiere copiar
    archivo_origen = os.path.join(ruta_origen, f'{archivo[0]}.{archivo[1]}')
    # Nombre de copia
    archivo_destino = os.path.join(ruta_destino, f'{archivo[0]}_copia.{archivo[1]}')
    # Nombre que tendra al renombrar, Formato: prueba_AAAAMMDD_HHMMSS.txt
    nuevo_nombre = f'{archivo[0]}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.{archivo[1]}'
    archivo_destino_2 = os.path.join(ruta_destino, nuevo_nombre)

    # Copiamos el archivo de la carpeta de origen a la carpeta de destino
    shutil.copy2(archivo_origen, archivo_destino)

    # Variables para verificar que los archivos se cambien correctamenre
    renombrar = False
    quitar = False

    # Abrimos ambos archivos y los comparamos
    with open(archivo_origen, 'r', encoding="utf-8") as txt:
        with open(archivo_destino, 'r', encoding="utf-8") as txt2:
            if filecmp.cmp(archivo_origen, archivo_destino):
                # Si los archivos son correctos cambiamos los valores de las variables
                quitar = True
                renombrar = True

    # Verfificamos que la variable quitar este en true, de ser asi eliminamos el archivo de la carpeta origen
    if quitar:
        print('Eliminando original')
        logging.info(f'El archivo {archivo[0]}.{archivo[1]} se ha copiado correctamente')
        os.remove(archivo_origen)
    # En caso contrario quitamos la copia
    else:
        logging.warning(f'Ocurrio un problema al copiar el archivo -> {archivo[0]}.{archivo[1]}')
        print('Ha ocurrido un problema al copiar el documento')
        print('Eliminando copia')
        os.remove(archivo_destino)

    # Verfificamos que la variable renombrar este en true, de ser asi renombramos la copia
    if renombrar:
        logging.info('Renombrando el archivo')
        print('Renombrando')
        os.rename(archivo_destino, archivo_destino_2)
        logging.info(f'El archivo se ha renombrado como: {nuevo_nombre}')
    
    time.sleep(2)

posterior = len(os.listdir(ruta_destino))

# Calculamos la cantidad de archivos que se han copiado para verificar si hubo algún error
total = posterior - previo
logging.info(f'Se han copiado {total} archivos')

if total != len(archivos):
    logging.warning('Han ocurrido uno o mas problemas al copiar los archivos')

logging.debug('Fin de la copia de archivos')

# Variable que almacena la hora en que se inicio el programa
tiempo_final = datetime.datetime.now()

tiempo_ejecucion = tiempo_final - tiempo_inicio
logging.info(f'Tiempo de ejecucion: {tiempo_ejecucion}')

# Cerramos el log
logging.shutdown()

print('------------------------------------------')
print('Fin del programa')
input('Presione enter para salir...')
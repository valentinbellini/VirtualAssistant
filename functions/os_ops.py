# Aqui definiremos todas las funciones (ops) del sistema operativo.

import os
import subprocess as sp
import datetime

# Si se quiere utilizar la funcionalidad de abrir carpetas, deberá especificarse las rutas en el diccionario
# "paths" junto con el nombre que se desee.

class WindowsOps:
    
    paths = {
        'documentos': r'C:\Users\valen\Documents',
        'descargas': r'C:\Users\valen\Downloads',
        'facultad' : r'G:\Mi unidad\UNR Ing electrónica'
    }
    
    def __init__(self):
        pass
    
    def open_camera(self):
        sp.run('start microsoft.windows.camera:', shell=True)
        
    def open_calculator(self):
        sp.Popen(r'C:\\Windows\\System32\\calc.exe')
    
    def open_folder(self, folder_name):
        # Open folder es un metodo al que se le pasa el nombre de la carpeta a abrir y mapea su ruta
        # en las direcciones (paths) que tiene definida la clase.
        try:
            path = self.paths.get(folder_name.lower())
            if path:
                os.startfile(path)
            else:
                return f'No se reconoce la carpeta {folder_name}'
        except Exception as e:
            print(f"Error al abrir la carpeta: {e}")

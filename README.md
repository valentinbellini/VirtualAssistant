# _Asistente Virtual Jarvis_

Este proyecto implementa un asistente virtual simple en Python con un objetivo unicamente educativo.

## Configuración del Entorno Virtual e instalación

#### Cree un entorno virtual:
``
 python -m venv venv
``
#### Active el entorno virtual:
- En Windows:
    ``    
    .\venv\Scripts\activate
    ``
- En Linux/Mac:
    ``
    source venv/bin/activate
    ``
#### Instale las dependencias:
``
pip install -r requirements.txt
``
#### Ejecute el script principal:
``
python main.py
``
_____________________________________________________________________________________________________________________
El Asistente Virtual es un programa diseñado para brindar asistencia mediante comandos de voz. Al iniciar el programa, el asistente saluda al usuario según la hora del día. Para activar la escucha y dar comandos, se utiliza la palabra clave `"jarvis"`.

## Funciones Disponibles

Una vez activada la escucha, el asistente puede recibir varios comandos para ejecutar diversas funciones. A continuación, se detallan algunos ejemplos:

- `Buscar en Wikipedia`:"Wikipedia {consulta}"
- `Buscar en Google`: "Google {búsqueda}"
- `Obtener Clima`: "Clima en {ciudad}"
- `Reproducir Video en Youtube`: "Reproduce video {título}"
- `Informe sobre Criptomonedas`: "Informe Crypto"
- `Últimas Noticias`: "Noticias"
- `Abrir Cámara`: "Abrir cámara"
- `Obtener Dirección IP`: "IP address" o "Obtener IP"
- `Abrir Carpeta del Sistema Operativo`: "Abrir carpeta {nombre de la carpeta}"

## .ENV

En el archivo .env deberá definir las siguientes variables de entorno

- USER= {USER}
- BOTNAME= {YOUR_BOTNAME}
- API_KEY_WEATHER = {YOUR_API_KEY_WEATHER}
- NEWS_API_KEY = {YOUR_NEWS_API_KEY}
- COINMARKETCAP_API_KEY = {YOUR_COINMARKETCAP_API_KEY}


## Notas

- Algunas funciones aún están en desarrollo y se indicará si no están implementadas.
- Ante cualquier problema, el asistente proporcionará un mensaje de error y solicitará repetir el comando.
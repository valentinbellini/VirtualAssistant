# Aqui definiremos todas las funciones (ops) que se hagan de manera online

import requests
from decouple import config
import wikipedia
import pywhatkit as kit


import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

API_KEY_WEATHER = config("API_KEY_WEATHER")
NEWS_API_KEY = config("NEWS_API_KEY")
COINMARKETCAP_API_KEY = config("COINMARKETCAP_API_KEY")


def obtener_clima(ciudad):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY_WEATHER}&q={ciudad}&lang=es"
        response = requests.get(url)
        print("Acceso a la API de WeatherAPI.com...")

        response.raise_for_status()

        datos_clima = response.json()

        if 'current' in datos_clima:
            clima_actual = datos_clima['current']['condition']['text']
            temperatura = datos_clima['current'].get('temp_c', 'No disponible')
            humedad = datos_clima['current'].get('humidity', 'No disponible')
            feels_like_c = datos_clima['current'].get('feelslike_c', 'No disponible')
            precipitacion_mm = datos_clima['current'].get('precip_mm', 'No disponible')                
            mensaje = (
                f"El clima en {ciudad} es {clima_actual} con una temperatura de {temperatura} grados Celsius y sensación térmica de {feels_like_c}."
                f"La precipitación actual es de {precipitacion_mm} mm y la humedad es de {humedad}%."
            )                
        else:
            mensaje = "No se pudo obtener la información del clima."
        return mensaje

    except requests.exceptions.RequestException as e:
        error_message = f"Error al obtener el clima: {e}"
        return error_message

def find_my_ip():
    try:
        response = requests.get('https://api.ipify.org/?format=json') # API de: https://www.ipify.org/
        response.raise_for_status()  # Genera una excepción para códigos de estado HTTP no exitosos

        ip_address = response.json().get("ip", "No disponible")
        return ip_address

    except requests.exceptions.RequestException as e:
        # Manejar cualquier error de solicitud
        error_message = f"Error al obtener la dirección IP: {e}"
        return error_message

def search_on_wikipedia(query, lang="es"):
    """ 
    WIKIPEDIA
    Dentro del módulo wikipedia, tenemos un summary() que acepta una variable query como elemento. 
    Adicionalmente, podemos indicar el número de oraciones requeridas. Y, entonces, simplemente 
    mostrar el resultado.  
    """
    try:
        wikipedia.set_lang(lang)
        results = wikipedia.summary(query, sentences=1)
        return results

    except wikipedia.exceptions.DisambiguationError as e:
        error_message = f"Error al buscar en Wikipedia (desambiguación): {e}"
        return error_message
    except wikipedia.exceptions.HTTPTimeoutError as e:
        error_message = f"Error de tiempo de espera al buscar en Wikipedia: {e}"
        return error_message
    except Exception as e:
        error_message = f"Error al buscar en Wikipedia: {e}"
        return error_message

def play_on_youtube(video):
    """
    PyWhatKit tiene un playonyt() que acepta un tema como elemento. 
    Entonces busca dicho tema en YouTube y reproduce el video más apropiado. 
    ( Usa https://pyautogui.readthedocs.io/en/latest/ de manera encubierta )
    """
    try:
        kit.playonyt(video)
    except Exception as e:
        error_message = f"Error al reproducir en YouTube: {e}"
        return error_message
    
def search_on_google(query):
    try:
        kit.search(query)
    except Exception as e:
        error_message = f"Error al buscar en Google: {e}"
        return error_message
    
def get_latest_news(country='ar', language='es', category='general', num_articles=5):
    #Obtiene las últimas noticias desde la API de noticias.
    try:
        news_headlines = []
        api_key = NEWS_API_KEY
        api_url = f"https://newsapi.org/v2/top-headlines"
        params = {
            'country': country,
            'category': category,
            'apiKey': api_key
        }

        response = requests.get(api_url, params=params)
        response.raise_for_status()

        articles = response.json().get("articles", [])
        for article in articles[:num_articles]:
            news_headlines.append(article.get("title", "No disponible"))

        return news_headlines

    except requests.exceptions.RequestException as e:
        error_message = f"Error al obtener noticias: {e}"
        news_headlines.append(error_message)
        return news_headlines

def get_crypto(top_n=5):
    BASE_URL_MKT = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        'start': '1',
        'limit': str(top_n),  # Ahora se utiliza la variable top_n para determinar la cantidad de criptomonedas a consultar
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    try:
        response = requests.get(BASE_URL_MKT, headers=headers, params=parameters)
        data = response.json()
        if response.status_code == 200:
            top_cryptos = data['data'][:top_n]
            crypto_info = []
            for crypto in top_cryptos:
                name = crypto['name']
                symbol = crypto['symbol']
                price = round(crypto['quote']['USD']['price'],3)
                crypto_info.append({'name': name, 'symbol': symbol, 'price': price})

            return crypto_info
        else:
            raise Exception(f'Error en la solicitud: {data["status"]["error_message"]}')
    except Exception as e:
        raise Exception(f'Error: {e}')

def get_global_crypto_data():
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
    parameters = {
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()
        if response.status_code == 200:
            return {
                        'eth_dominance': data['data']['eth_dominance'],
                        'btc_dominance': data['data']['btc_dominance']
                    }
        else:
            raise Exception(f'Error en la solicitud: {data["status"]["error_message"]}')
    except Exception as e:
        raise Exception(f'Error: {e}')

def generate_crypto_report():
    # Con el llamada a esta funcion se crea un informe crypto en PNG con el top 5 de criptomonedas y sus cotizaciones
    # junto con la dominancia de btc, eth y alts en un grafico de torta. La imagen se guarda en una carpeta.
    # Para obtener los datos se importan dos funciones desde online_ops.py que hacen un llamado a la API de CoinMarketCap.
    
    # Obtener datos específicos a traves de los llamados a la API
    crypto_data = get_crypto() # TOP 5 cryptos con precio
    global_data = get_global_crypto_data() # Dominancias del mercado
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    btc_dominance = global_data['btc_dominance']
    eth_dominance = global_data['eth_dominance']
    alt_dominance = 100.0 - eth_dominance - btc_dominance
    
    # Crear imagen
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)

    # Agregar título
    title_font = ImageFont.truetype("arial.ttf", 36)
    draw.text((10, 10), "Informe Diario del Mercado Cripto", fill="black", font=title_font)

    # Agregar línea de separación
    draw.line([(10, 55), (790, 55)], fill='#999', width=2)
    y_position = 70
    
    # Agregar fecha
    date_font = ImageFont.truetype("arial.ttf", 20)
    draw.text((10, y_position), f"Fecha del informe: {current_date}", fill="black", font=date_font)
    y_position = 110
    
    # Agregar información del top 5
    info_font = ImageFont.truetype("arial.ttf", 18)
    draw.text((10, y_position), "Top 5 Criptomonedas:", fill="black", font=info_font)
    y_position = 140
    for crypto in crypto_data:
        draw.text((20, y_position), f"{crypto['name']} ({crypto['symbol']}): ${crypto['price']:.2f} USD", fill="black", font=info_font)
        y_position += 30

    # Crear el gráfico de torta
    labels = ['Bitcoin Dom.', 'Ethereum Dom.', 'Altcoins Dom.']
    sizes = [btc_dominance, eth_dominance, alt_dominance]
    colors = ['#FFB996', '#FFCF81', '#FDFFAB']

    plt.figure(figsize=(4, 4))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('dominance_pie_chart.png', bbox_inches='tight', pad_inches=0.1)
    plt.close()

    # Superponer el gráfico en la imagen
    chart_img = Image.open('dominance_pie_chart.png')
    img.paste(chart_img, (250, 230))  # Ajustar coordenadas de ser necesario
    
    # Borrar la imagen del gráfico de torta después de usarla
    os.remove('dominance_pie_chart.png')
    
    # Crear carpeta para guardar imágenes si no existe
    img_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Reportes_Cripto")
    os.makedirs(img_folder, exist_ok=True)
    
    # Crear nombre único para la imagen
    img_name = f"informe_crypto_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    img_path = os.path.join(img_folder, img_name)
    
    # Guardamos la imagen en la ruta especificada
    img.save(img_path)

    # Mostrar la imagen
    img.show()

    return img_path
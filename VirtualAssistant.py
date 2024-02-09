# Aqui se define la clase VirtualAssistant junto con todos sus metodos.

# Importar las configuraciones y funciones necesarias desde otros módulos
from configs import VELOCIDAD_VOZ, VOLUMEN_VOZ, LANGUAGE_RESTRICTION
from utils import opening_phrases, kw_crypto_report, kw_youtube_video

from functions.online_ops import *
from functions.os_ops import WindowsOps

# Otras importaciones...
import speech_recognition as sr
import pyttsx3
from decouple import config
from datetime import datetime
from random import choice

USERNAME = config('USER')
BOTNAME = config('BOTNAME')
API_KEY_GOOGLE_SEARCH = config('API_KEY_GOOGLE_SEARCH')
CUSTOM_SEARCH_ENGINE_ID = config("CUSTOM_SEARCH_ENGINE_ID")

class VirtualAssistant:
    def __init__(self):
        # El asistente virtual instancia un objeto de sistema operativo windows para utilizar las funciones.
        self.windows_ops = WindowsOps() 
        self.engine_tts = self.init_engine_tts() # Configuraciones de velocidad de voz y volumen

    # Setear propiedades de voz del asistente virtual, tales como velocidad, volumen y tipo.
    def init_engine_tts(self):
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', VELOCIDAD_VOZ)
        engine.setProperty('volume', VOLUMEN_VOZ)
        # Mas info de la api: https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee125663(v=vs.85)
        return engine
    
    # Se define el metodo de escucha
    def escuchar(self):
        reconocedor = sr.Recognizer()

        with sr.Microphone() as source:
            print(f"Di 'Jarvis' para activar:")
            reconocedor.adjust_for_ambient_noise(source)
            reconocedor.pause_threshold = 1 # Permite que no compile aunque hagamos una pausa de 1 segundo mientras hablamos
            audio = reconocedor.listen(source)

        try:
            comando = reconocedor.recognize_google(audio, language='es-ES').lower()
            print(comando)
            return comando
        
        except sr.UnknownValueError:
            return ""

    # Se define el metodo de habla
    def hablar(self, mensaje):
        self.engine_tts.say(mensaje)
        self.engine_tts.runAndWait()
    
    # Saludar cuando se inicia el script dependiendo la hora local
    def saludar_usuario(self):
        hour = datetime.now().hour
        saludo = "Buenos días" if 6 <= hour < 12 else "Buenas tardes" if 12 <= hour < 18 else "Buenas noches"
        self.hablar(f"{saludo} {USERNAME}. Yo soy {BOTNAME}. ¿Cómo puedo asistirle?")
    
    # Este metodo maneja todos los comandos según lo escuchado. No es la mejor manera pero es una forma
    # sencilla de interacción. Hace coincidir el comando que decimos por microfono, con alguna sentencia para
    # asi realizar la acción correspondiente.
    def manejar_comando(self, comando):
        try:
            if 'reproducir música' in comando:
                self.hablar("Lo siento, la función de reproducción de música aún no está implementada.")
            elif 'wikipedia' in comando:
                self.buscar_en_wikipedia()
            elif 'google' in comando:
                self.buscar_en_google()
            elif 'clima' in comando:
                self.obtener_clima(comando)
            elif any(palabra_clave in comando for palabra_clave in kw_youtube_video):
                self.buscar_en_youtube()
            elif any(palabra_clave in comando for palabra_clave in kw_crypto_report):
                self.generar_informe_cripto()
            elif 'noticias' in comando:
                self.mostrar_ultimas_noticias()
            elif 'abrir cámara' in comando:
                self.windows_ops.open_camera()
            elif 'ip address' in comando or 'obtener ip' in comando:
                self.obtener_direccion_ip()
            elif 'abrir carpeta' in comando:
                self.abrir_carpeta(comando)
            elif 'opciones' in comando:
                self.mostrar_opciones()
            else:
                self.hablar("No entendí el comando. ¿Puedes repetirlo?")
        except Exception as e:
            print(f"Error no manejado: {e}")
            self.hablar("Ocurrió un error al procesar el comando.")

    def buscar_en_wikipedia(self):
        self.hablar("¿Qué quiere buscar en Wikipedia, señor?")
        query = self.escuchar()
        if any(cancelar_palabra in query for cancelar_palabra in ['cancelar', 'detente']):
            self.hablar("De acuerdo, cancelo búsqueda señor")
        else:
            results = search_on_wikipedia(query, LANGUAGE_RESTRICTION)
            self.hablar(f'De acuerdo con Wikipedia: {results}.')

    def buscar_en_google(self):
        self.hablar("¿Qué quiere buscar en Google, señor?")
        query = self.escuchar()
        if any(cancelar_palabra in query for cancelar_palabra in ['cancelar', 'detente']):
            self.hablar("De acuerdo, cancelo búsqueda señor")
        else:
            results = search_on_google(query)
            self.hablar(f'{results}.')
            self.hablar('Mostraré los resultados en la terminal de comandos')
            print(query)

    def obtener_clima(self, comando):
        self.hablar(choice(opening_phrases))
        ciudad = comando.split('clima')[-1].strip()
        print(f'Ciudad: {ciudad}')
        mensaje = obtener_clima(ciudad)
        self.hablar(mensaje)

    def buscar_en_youtube(self):
        self.hablar('¿Qué desea ver en Youtube, señor?')
        query = self.escuchar()
        if any(cancelar_palabra in query for cancelar_palabra in ['cancelar', 'detente']):
            self.hablar("De acuerdo, cancelo búsqueda señor")
        else:
            play_on_youtube(query)

    def generar_informe_cripto(self):
        self.hablar(choice(opening_phrases))
        generate_crypto_report()

    def mostrar_ultimas_noticias(self):
        self.hablar("Te dejo por escrito los últimos 5 titulares.")
        latest_news = get_latest_news()
        for i, headline in enumerate(latest_news, start=1):
            print(f"{i}. {headline}")

    def obtener_direccion_ip(self):
        ip_address = find_my_ip()
        self.hablar(f'Su dirección IP es: {ip_address}')
        print(f'Dirección IP: {ip_address}')

    def abrir_carpeta(self, comando):
        folder = comando.split('abrir carpeta ', 1)[-1].lower()
        self.windows_ops.open_folder(folder)

    def mostrar_opciones(self):
        self.hablar("Estas son algunas de las cosas que puedes pedirme: ")
        self.hablar("""
                    Buscar en google o wikipedia.
                    Obtener dirección IP.
                    Abrir alguna carpeta de tu disco local.
                    Pedirme las últimas noticias.
                    Generar un informe cripto.
                    Buscar un video en youtube.
                    Pedirme el clima en alguna localidad.
                    """)
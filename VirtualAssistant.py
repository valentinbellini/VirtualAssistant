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
              
            # REPRODUCIR MUSICA
            if 'reproducir música' in comando:
                self.hablar("Lo siento, la función de reproducción de música aún no está implementada.")
            
            # BUSCAR EN WIKIPEDIA
            elif 'wikipedia' in comando:
                self.hablar("¿Que quiere buscar en Wikipedia, señor?")
                query = self.escuchar()
                if 'cancelar' in query or 'detente' in query:
                    self.hablar("De acuerdo, cancelo busqueda señor")
                else: 
                    results = search_on_wikipedia(query, LANGUAGE_RESTRICTION)
                    self.hablar(f'De acuerdo con Wikipedia: {results}.')
            
            # BUSCAR EN GOOGLE
            elif 'Google' in comando:
                self.hablar("¿Que quiere buscar en Google, señor?")
                query = self.escuchar()
                if 'cancelar' in query or 'detente' in query:
                    self.hablar("De acuerdo, cancelo busqueda señor")
                else: 
                    results = search_on_google(query)
                    self.hablar(f'{results}.')
                    self.hablar('Mostrare los resultados en la terminal de comandos')
                    print(query)
            
            # OBTENER CLIMA
            elif 'clima' in comando:
                self.hablar(choice(opening_phrases))
                ciudad = comando.split('clima')[-1].strip()
                print(f'Ciudad: {ciudad}')
                mensaje = obtener_clima(ciudad)
                self.hablar(mensaje)
            
            # BUSCAR EN YOUTUBE
            elif any(palabra_clave in comando for palabra_clave in kw_youtube_video):
                self.hablar('¿Qué desea ver en Youtube, señor?')
                query = self.escuchar()
                if 'cancelar' in query or 'detente' in query:
                    self.hablar("De acuerdo, cancelo busqueda señor")
                else: 
                    play_on_youtube(query)
            
            # INFORME CRYPTO
            elif any(palabra_clave in comando for palabra_clave in kw_crypto_report):
                self.hablar(choice(opening_phrases))            
                generate_crypto_report()
            
            # ULTIMAS NOTICIAS
            elif 'noticias' in comando:
                self.hablar("Te dejo por escrito los ultimos 5 titulares.")
                latest_news = get_latest_news()
                for i, headline in enumerate(latest_news, start=1):
                    print(f"{i}. {headline}")
            
            # ABRIR CAMARA
            elif 'abrir cámara' in comando:
                self.windows_ops.open_camera()
            
            # OBTENER IP
            elif 'ip address' in comando or 'obtener ip' in comando:
                ip_address = find_my_ip()
                self.hablar(f'Su dirección IP es: {ip_address}')
                print(f'Dirección IP: {ip_address}')
            
            # ABRIR CARPETA DEL SISTEMA OPERATIVO
            elif 'abrir carpeta' in comando:
                # Divide el comando en dos partes en la primera aparición de 'abrir carpeta '.
                # Luego, toma el segundo elemento de la lista resultante.
                folder = comando.split('abrir carpeta ', 1)[-1]

                # Convierte la cadena a minúsculas para manejar entradas mixtas.
                folder = folder.lower()

                # Llama a la función open_folder con la carpeta obtenida.
                self.windows_ops.open_folder(folder)
                
                # Un uso correcto del comando seria "abrir carpeta descargas"
            
            elif 'opciones' in comando:
                self.hablar("Estas son algunas de las cosas que puedes pedirme: ")
                self.hablar("""
                            Buscar en google o wikipedia.
                            Obtener direccion IP.
                            Abrir alguna carpeta de tu disco local.
                            Pedirme las ultimas noticias.
                            Generar un informe cripto.
                            Buscar un video en youtube.
                            Pedirme el clima en alguna localidad.
                            """)
            
            # SI NO HAY COINCIDENCIAS
            else:
                self.hablar("No entendí el comando. ¿Puedes repetirlo?")
                
        except Exception as e:
            print(f"Error no manejado: {e}")
            self.hablar("Ocurrió un error al procesar el comando.")



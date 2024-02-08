# Este es el programa principal donde se instancia un objeto de la clase VirtualAssistant (en este caso Jarvis)
# y se da el flujo del programa.

from VirtualAssistant import VirtualAssistant

if __name__ == "__main__":
    jarvis = VirtualAssistant()
    jarvis.saludar_usuario()
    while True:
        mensaje = jarvis.escuchar()
        if 'jarvis' in mensaje:
            jarvis.hablar("Sí señor. ¿En qué puedo ayudarle?")
            comando = jarvis.escuchar()
            jarvis.manejar_comando(comando)
            
            
            
        


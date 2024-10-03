import openai
import speech_recognition as sr
import pyttsx3
import time

# Establece la clave API de OpenAI para utilizar GPT-3.5
openai.api_key = "PONGA SU CLAVE"

# Inicializa el motor de conversión de texto a voz
motor_voz = pyttsx3.init()

# Función que envía una pregunta a ChatGPT y devuelve la respuesta
def preguntar_chatgpt(pregunta):
    try:
        # Llama a la API de OpenAI con el modelo GPT-3.5-turbo
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Modelo a utilizar
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},  # Configura el sistema
                {"role": "user", "content": pregunta}  # Envia la pregunta del usuario
            ],
            max_tokens=100,  # Limita el número máximo de tokens para la respuesta
            temperature=0.7  # Ajusta la creatividad de las respuestas (opcional)
        )
        # Retorna el contenido de la respuesta de GPT-3
        return respuesta['choices'][0]['message']['content'].strip()
    except Exception as e:
        # Manejo de excepciones si ocurre un error con la API de OpenAI
        return f"Error al contactar con OpenAI: {str(e)}"

# Función que convierte la voz en texto usando reconocimiento de voz
def voz_a_texto(segundos_escucha):
    reconocedor = sr.Recognizer()  # Inicializa el reconocedor de voz
    with sr.Microphone() as fuente:
        print("Escuchando...")
        # Graba el audio durante un tiempo específico
        audio = reconocedor.record(fuente, duration=segundos_escucha)
        print("Reconociendo...")
        try:
            # Convierte el audio grabado en texto utilizando el servicio de Google
            texto = reconocedor.recognize_google(audio, language="es-ES")
            return texto
        except sr.UnknownValueError:
            # Manejo de errores si no se entiende la voz
            return "No se entendió lo que dijiste."
        except sr.RequestError as e:
            # Manejo de errores si no se puede conectar con el servicio de reconocimiento de voz
            return f"Error al conectar con el servicio de reconocimiento de voz: {str(e)}"

# Función que convierte texto en voz usando pyttsx3
def texto_a_voz(texto):
    motor_voz.say(texto)  # Usa el motor para decir el texto
    motor_voz.runAndWait()  # Espera a que termine de hablar

# Bucle principal que sigue escuchando y respondiendo a las preguntas del usuario
while True:
    time.sleep(5)  # Añade un retraso de 5 segundos entre cada solicitud
    pregunta = voz_a_texto(10)  # Escucha durante 10 segundos para capturar una pregunta
    print(f"Pregunta: {pregunta}")
    
    if pregunta.lower() == "salir":
        # Si el usuario dice "salir", el programa termina
        print("Saliendo...")
        break
    
    # Obtiene la respuesta de GPT-3 y la convierte en voz
    respuesta = preguntar_chatgpt(pregunta)
    print(f"Respuesta: {respuesta}")
    
    # Convierte la respuesta en voz
    texto_a_voz(respuesta)
    print("¿Cuál es tu siguiente pregunta?")

from consultas import cargar_equipos, cargar_jugadores
from chatbot import procesar_pregunta


def main():
    equipos = cargar_equipos()
    jugadores = cargar_jugadores()

    print("Chatbot NBA iniciado.\n")
    while True:
        pregunta = input("Tú: ").strip()
        respuesta = procesar_pregunta(pregunta, equipos, jugadores)
        print("Bot:", respuesta, "\n")

if __name__ == "__main__":
    main()

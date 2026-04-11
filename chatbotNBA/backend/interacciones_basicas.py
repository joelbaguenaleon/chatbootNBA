def detectar_interaccion_basica(pregunta):
    texto = pregunta.lower().strip()

    saludos = ["hola", "buenas", "hey", "holi"]
    despedidas = ["adiós", "adios", "hasta luego", "nos vemos", "bye"]
    agradecimientos = ["gracias", "muchas gracias", "thanks"]
    ayuda = ["ayuda", "qué puedes hacer", "que puedes hacer", "opciones"]
    identidad = ["quién eres", "quien eres", "qué eres", "que eres"]

    if texto in saludos:
        return "¡Hola! Puedo ayudarte con información sobre equipos y jugadores de la NBA."

    if texto in despedidas:
        return "¡Hasta luego! Espero haberte ayudado."

    if texto in agradecimientos:
        return "De nada, encantado de ayudarte."

    if texto in ayuda:
        return (
            "Puedo facilitar información de la nba, respondo preguntas como:\n"
            "- jugadores de houston\n"
            "- partidos de hoy\n"
            "- qué dorsal tiene Tatum\n"
            "- información de Boston"
        )

    if texto in identidad:
        return "Soy un chatbot sobre la NBA y puedo darte información de equipos y jugadores."

    return None

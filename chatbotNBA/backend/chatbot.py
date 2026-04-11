from consultas import (
    obtener_jugadores_equipo,
    obtener_equipo_jugador,
    obtener_info_jugador,
    obtener_info_equipo,
    guardar_interaccion
)

from alias import (
    obtener_alias_equipos,
    traducir_posicion,
    traducir_conferencia,
    traducir_division,
    normalizar_abreviatura_equipo
)

from interacciones_basicas import detectar_interaccion_basica
from apis_nba import (
    obtener_partidos_hoy,
    obtener_ultimos_partidos_equipo,
    obtener_estadisticas_jugador,
    obtener_clasificacion_liga
)

##logica del chat para entender mensajes##
def detectar_equipo(pregunta, equipos):
    texto = pregunta.lower().strip()
    alias_equipos = obtener_alias_equipos()

    for alias in sorted(alias_equipos.keys(), key=len, reverse=True):
        if alias in texto:
            return alias_equipos[alias]

    for nombre, abreviatura in equipos:
        if nombre.lower() in texto or abreviatura.lower() in texto:
            return nombre

    return None


def detectar_jugador(pregunta, jugadores):
    texto = pregunta.lower().strip()

    for jugador in jugadores:
        if jugador.lower() in texto:
            return jugador

    coincidencias = []

    for jugador in jugadores:
        partes = jugador.lower().split()
        for parte in partes:
            if len(parte) > 2 and parte in texto:
                coincidencias.append(jugador)
                break

    if len(coincidencias) == 1:
        return coincidencias[0]

    return None


def detectar_intencion(texto, equipo_detectado, jugador_detectado):
    if equipo_detectado and ("jugadores" in texto or "plantilla" in texto):
        return "jugadores_equipo"

    elif jugador_detectado and ("equipo" in texto or "juega" in texto):
        return "equipo_jugador"

    elif equipo_detectado and (
        "información" in texto or
        "informacion" in texto or
        "info" in texto
    ):
        return "info_equipo"

    elif "partidos de hoy" in texto or "que partidos hay hoy" in texto or "quien juega hoy" in texto:
        return "partidos_hoy"

    elif equipo_detectado and ("últimos partidos" in texto or "ultimos partidos" in texto or "ultimos" in texto):
        return "ultimos_partidos_equipo"

    elif jugador_detectado and (
        "posición" in texto or
        "posicion" in texto or
        "dorsal" in texto or
        "info" in texto
    ):
        return "info_jugador"

    elif jugador_detectado and (
        "estadisticas" in texto or
        "estadísticas" in texto or
        "temporada" in texto
    ):
        return "estadisticas_jugador"

    elif (
        "clasificacion" in texto or
        "clasificación" in texto or
        "tabla" in texto or
        "posiciones" in texto
    ):
        return "clasificacion"

    return "desconocida"


def procesar_pregunta(pregunta, equipos, jugadores):
    respuesta_basica = detectar_interaccion_basica(pregunta)

    if respuesta_basica: ##interacciones básicas
        guardar_interaccion(pregunta, respuesta_basica, "BASIC")
        return respuesta_basica

    texto = pregunta.lower().strip()
    equipo_detectado = detectar_equipo(texto, equipos)
    jugador_detectado = detectar_jugador(texto, jugadores)
    intencion = detectar_intencion(texto, equipo_detectado, jugador_detectado)

    if intencion == "jugadores_equipo": ##plantilla del equipo
        datos = obtener_jugadores_equipo(equipo_detectado)

        if not datos:
            respuesta = "No encontré jugadores para ese equipo."
            guardar_interaccion(pregunta, respuesta, "BD")
            return respuesta

        respuesta = "Jugadores de " + equipo_detectado + ":\n"

        for nombre, posicion, dorsal in datos:
            respuesta += (
                "- "
                + nombre
                + " ("
                + str(traducir_posicion(posicion))
                + ", dorsal "
                + str(dorsal)
                + ")\n"
            )

        guardar_interaccion(pregunta, respuesta, "BD")
        return respuesta

    elif intencion == "equipo_jugador": #devuelve SOLO equipo del jugador
        dato = obtener_equipo_jugador(jugador_detectado)

        if not dato:
            respuesta = "No encontré ese jugador."
            guardar_interaccion(pregunta, respuesta, "BD")
            return respuesta

        nombre = dato[0]
        equipo = dato[1]

        respuesta = nombre + " juega en " + equipo + "."
        guardar_interaccion(pregunta, respuesta, "BD")
        return respuesta

    elif intencion == "info_jugador":  ##datos generales de un jugador
        dato = obtener_info_jugador(jugador_detectado)

        if not dato:
            respuesta = "No encontré información de ese jugador."
            guardar_interaccion(pregunta, respuesta, "BD")
            return respuesta

        nombre = dato[0]
        posicion = dato[1]
        dorsal = dato[2]
        equipo = dato[3]

        respuesta = (
            nombre
            + " juega en "
            + equipo
            + ", su posición es "
            + str(traducir_posicion(posicion))
            + " y lleva el dorsal "
            + str(dorsal)
            + "."
        )

        guardar_interaccion(pregunta, respuesta, "BD")
        return respuesta
    
    elif intencion == "info_equipo": #datos básicos de un equipo
        dato = obtener_info_equipo(equipo_detectado)

        if not dato:
            respuesta = "No encontré ese equipo."
            guardar_interaccion(pregunta, respuesta)
            return respuesta

        nombre = dato[0]
        ciudad = dato[1]
        conferencia = dato[2]
        division = dato[3]
        abreviatura = dato[4]

        respuesta = (
            nombre
            + "("
            + abreviatura
            + ")"
            + " es un equipo de "
            + ciudad
            + ", pertenece a la conferencia "
            + str(traducir_conferencia(conferencia))
            + ", división "
            + str(traducir_division(division))
            + "."
        )

        guardar_interaccion(pregunta, respuesta)
        return respuesta
    
###apis_nba###
    elif intencion == "partidos_hoy":  ##mostrar partidos de la jornada
        datos = obtener_partidos_hoy()

        if not datos:
            respuesta = "No encontré partidos para hoy."
            guardar_interaccion(pregunta, respuesta, "API")
            return respuesta

        respuesta = f"Hoy hay {len(datos)} partidos NBA:\n\n"

        for i, partido in enumerate(datos, 1):
            hora = partido.get("hora_es", partido.get("hora", partido.get("estado", "Sin hora")))
            respuesta += f"{i}. {partido['visitante']} vs {partido['local']} | {hora}\n"

        guardar_interaccion(pregunta, respuesta, "API")
        return respuesta

    elif intencion == "ultimos_partidos_equipo": ##cargar lso ultimos 5 juegos de un equipo
        abreviatura = normalizar_abreviatura_equipo(equipo_detectado)
        datos = obtener_ultimos_partidos_equipo(abreviatura)

        if not datos:
            respuesta = "No encontré últimos partidos para ese equipo."
            guardar_interaccion(pregunta, respuesta, "API")
            return respuesta

        respuesta = f"Últimos partidos de {equipo_detectado}:\n\n"

        for partido in datos:
            respuesta += (
                f"- {partido['fecha']} | "
                f"{partido['matchup']} | "
                f"{partido['resultado']}\n"
            )

        guardar_interaccion(pregunta, respuesta, "API")
        return respuesta

    elif intencion == "estadisticas_jugador": ##carga los stats de u jugador
        datos = obtener_estadisticas_jugador(jugador_detectado)

        if not datos:
            respuesta = "No encontré estadísticas de ese jugador en esta temporada."
            guardar_interaccion(pregunta, respuesta, "API")
            return respuesta

        respuesta = (
            f"Estadísticas de {datos['jugador']} en la temporada {datos['temporada']}:\n\n"
            f"- Partidos: {datos['partidos']}\n"
            f"- Minutos por partido: {datos['minutos_por_partido']}\n"
            f"- Puntos por partido: {datos['puntos_por_partido']}\n"
            f"- Rebotes por partido: {datos['rebotes_por_partido']}\n"
            f"- Asistencias por partido: {datos['asistencias_por_partido']}\n"
            f"- Robos por partido: {datos['robos_por_partido']}\n"
            f"- Tapones por partido: {datos['tapones_por_partido']}"
        )

        guardar_interaccion(pregunta, respuesta, "API")
        return respuesta

    elif intencion == "clasificacion": #cargar la clasificacion de la liga
        datos = obtener_clasificacion_liga()

        if not datos:
            respuesta = "No pude obtener la clasificación de la liga."
            guardar_interaccion(pregunta, respuesta, "API")
            return respuesta

        este = [e for e in datos if e["conferencia"] == "East"]
        oeste = [e for e in datos if e["conferencia"] == "West"]

        respuesta = "Clasificación NBA\n\n"
        respuesta += "Conferencia Este:\n"
        for i, equipo in enumerate(este, 1):
            respuesta += f"{i}. {equipo['equipo']} ({equipo['victorias']}-{equipo['derrotas']})\n"

        respuesta += "\nConferencia Oeste:\n"
        for i, equipo in enumerate(oeste, 1):
            respuesta += f"{i}. {equipo['equipo']} ({equipo['victorias']}-{equipo['derrotas']})\n"

        guardar_interaccion(pregunta, respuesta, "API")
        return respuesta

    else:  ##en caso de no haber respuesta
        respuesta = (
            "No entendí la pregunta. "
            "Prueba con algo como 'jugadores de Lakers', "
            "'qué dorsal tiene Tatum', 'partidos de hoy', "
            "'estadísticas de durant' o 'clasificación nba'."
        )

        guardar_interaccion(pregunta, respuesta, "-")
        return respuesta

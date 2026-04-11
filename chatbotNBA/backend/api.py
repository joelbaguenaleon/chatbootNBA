from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

from consultas import (
    cargar_equipos,
    cargar_jugadores,
    obtener_jugadores_equipo,
    obtener_info_equipo,
    obtener_info_jugador,
    obtener_equipo_jugador,
)
from chatbot import procesar_pregunta
from apis_nba import (
    obtener_partidos_hoy,
    obtener_ultimos_partidos_equipo,
    obtener_estadisticas_jugador,
    obtener_clasificacion_liga,
)
from alias import normalizar_abreviatura_equipo


# Variables globales cargadas al iniciar la API
equipos_cache = []
jugadores_cache = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    global equipos_cache, jugadores_cache
    equipos_cache = cargar_equipos()
    jugadores_cache = cargar_jugadores()
    yield


app = FastAPI(
    title="Chatbot NBA API",
    version="1.0.0",
    description="API local para consultar información NBA desde Java Swing",
    lifespan=lifespan
)

# Si luego conectas Swing local, esto no molesta y te da flexibilidad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PreguntaRequest(BaseModel):
    texto: str


@app.get("/")
def inicio():
    return {
        "ok": True,
        "mensaje": "API del Chatbot NBA funcionando"
    }


@app.get("/health")
def health():
    return {
        "ok": True,
        "equipos_cargados": len(equipos_cache),
        "jugadores_cargados": len(jugadores_cache)
    }


@app.post("/preguntar")
def preguntar(data: PreguntaRequest):
    texto = data.texto.strip()

    if not texto:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    try:
        respuesta = procesar_pregunta(texto, equipos_cache, jugadores_cache)
        return {
            "ok": True,
            "pregunta": texto,
            "respuesta": respuesta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la pregunta: {str(e)}")


@app.get("/equipos")
def listar_equipos():
    return {
        "ok": True,
        "total": len(equipos_cache),
        "data": [
            {"nombre": nombre, "abreviatura": abreviatura}
            for nombre, abreviatura in equipos_cache
        ]
    }


@app.get("/jugadores")
def listar_jugadores():
    return {
        "ok": True,
        "total": len(jugadores_cache),
        "data": jugadores_cache
    }


@app.get("/equipo/{nombre_equipo}/jugadores")
def jugadores_de_equipo(nombre_equipo: str):
    datos = obtener_jugadores_equipo(nombre_equipo)

    return {
        "ok": True,
        "equipo": nombre_equipo,
        "total": len(datos),
        "data": [
            {
                "nombre": nombre,
                "posicion": posicion,
                "dorsal": dorsal
            }
            for nombre, posicion, dorsal in datos
        ]
    }


@app.get("/equipo/{nombre_equipo}")
def info_equipo(nombre_equipo: str):
    dato = obtener_info_equipo(nombre_equipo)

    if not dato:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    return {
        "ok": True,
        "data": {
            "nombre": dato[0],
            "ciudad": dato[1],
            "conferencia": dato[2],
            "division": dato[3],
            "abreviatura": dato[4]
        }
    }


@app.get("/jugador/{nombre_jugador}")
def info_jugador(nombre_jugador: str):
    dato = obtener_info_jugador(nombre_jugador)

    if not dato:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    return {
        "ok": True,
        "data": {
            "nombre": dato[0],
            "posicion": dato[1],
            "dorsal": dato[2],
            "equipo": dato[3]
        }
    }


@app.get("/jugador/{nombre_jugador}/equipo")
def equipo_de_jugador(nombre_jugador: str):
    dato = obtener_equipo_jugador(nombre_jugador)

    if not dato:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    return {
        "ok": True,
        "data": {
            "jugador": dato[0],
            "equipo": dato[1]
        }
    }


@app.get("/partidos/hoy")
def partidos_hoy():
    try:
        datos = obtener_partidos_hoy()
        return {
            "ok": True,
            "total": len(datos),
            "data": datos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo partidos: {str(e)}")


@app.get("/equipo/{nombre_equipo}/ultimos-partidos")
def ultimos_partidos(nombre_equipo: str):
    abreviatura = normalizar_abreviatura_equipo(nombre_equipo)

    if not abreviatura:
        raise HTTPException(status_code=404, detail="Equipo no reconocido")

    try:
        datos = obtener_ultimos_partidos_equipo(abreviatura)
        return {
            "ok": True,
            "equipo": nombre_equipo,
            "abreviatura": abreviatura,
            "total": len(datos),
            "data": datos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo últimos partidos: {str(e)}")


@app.get("/jugador/{nombre_jugador}/estadisticas")
def estadisticas_jugador(nombre_jugador: str):
    try:
        datos = obtener_estadisticas_jugador(nombre_jugador)

        if not datos:
            raise HTTPException(status_code=404, detail="No encontré estadísticas para ese jugador")

        return {
            "ok": True,
            "data": datos
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")


@app.get("/clasificacion")
def clasificacion():
    try:
        datos = obtener_clasificacion_liga()
        return {
            "ok": True,
            "total": len(datos),
            "data": datos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo clasificación: {str(e)}")

#arranque de api con exe
if __name__ == "__main__":  # arranque de api con exe
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None)


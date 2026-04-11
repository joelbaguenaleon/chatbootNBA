from nba_api.stats.endpoints import ScoreboardV2, TeamGameLog, PlayerCareerStats, LeagueStandings
from nba_api.stats.static import teams, players
from datetime import datetime
from zoneinfo import ZoneInfo

def convertir_a_hora_espanola(texto_hora):  ##hora de españa
    try:
        texto_hora = texto_hora.strip().replace(" ET", "").replace("ET", "").strip()

        dt = datetime.strptime(texto_hora, "%I:%M %p")
        dt = dt.replace(
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            tzinfo=ZoneInfo("America/New_York")
        )

        dt_es = dt.astimezone(ZoneInfo("Europe/Madrid"))
        return dt_es.strftime("%H:%M")
    except Exception:
        return texto_hora

def obtener_team_id_por_abreviatura(abreviatura):
    lista_equipos = teams.get_teams()

    for equipo in lista_equipos:
        if equipo["abbreviation"].lower() == abreviatura.lower():
            return equipo["id"]

    return None


def obtener_nombre_equipo_por_id(team_id):
    lista_equipos = teams.get_teams()

    for equipo in lista_equipos:
        if equipo["id"] == team_id:
            return equipo["full_name"]   
    return "Equipo desconocido"

##partidos del dia de hoy
def obtener_partidos_hoy():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    marcador = ScoreboardV2(game_date=fecha_hoy)
    partidos = marcador.get_data_frames()[0]
    resultados = []

    for _, fila in partidos.iterrows():
        local = obtener_nombre_equipo_por_id(fila["HOME_TEAM_ID"])
        visitante = obtener_nombre_equipo_por_id(fila["VISITOR_TEAM_ID"])
        estado = str(fila["GAME_STATUS_TEXT"]).strip()

        hora_es = estado
        if "ET" in estado:
            hora_es = convertir_a_hora_espanola(estado)

        resultados.append({
            "game_id": fila["GAME_ID"],
            "local": local,
            "visitante": visitante,
            "hora": hora_es,
            "estado": estado
        })

    return resultados
##patidos de un equipo
def obtener_ultimos_partidos_equipo(abreviatura, temporada="2025-26"):
    team_id = obtener_team_id_por_abreviatura(abreviatura)

    if not team_id:
        return []

    logs = TeamGameLog(team_id=team_id, season=temporada)
    df = logs.get_data_frames()[0]

    resultados = []

    for _, fila in df.head(5).iterrows():
        resultados.append({
            "fecha": fila["GAME_DATE"],
            "matchup": fila["MATCHUP"],
            "resultado": fila["WL"],
            "puntos": fila["PTS"]
        })

    return resultados

#estadisticas de un jugador
def obtener_player_id_por_nombre(nombre_jugador):
    lista_jugadores = players.get_players()

    for jugador in lista_jugadores:
        nombre_completo = jugador["full_name"].lower()
        if nombre_jugador.lower() in nombre_completo:
            return jugador["id"], jugador["full_name"]

    return None, None


def obtener_estadisticas_jugador(nombre_jugador, temporada="2025-26"):
    player_id, nombre_real = obtener_player_id_por_nombre(nombre_jugador)

    if not player_id:
        return None

    carrera = PlayerCareerStats(player_id=player_id)
    df = carrera.get_data_frames()[0]

    temporada_df = df[df["SEASON_ID"] == temporada]

    if temporada_df.empty:
        return None

    fila = temporada_df.iloc[0]

    partidos = int(fila["GP"])
    minutos = float(fila["MIN"])
    puntos = float(fila["PTS"])
    rebotes = float(fila["REB"])
    asistencias = float(fila["AST"])
    robos = float(fila["STL"])
    tapones = float(fila["BLK"])

    return {
        "jugador": nombre_real,
        "temporada": temporada,
        "partidos": partidos,
        "minutos_por_partido": round(minutos / partidos, 1) if partidos > 0 else 0,
        "puntos_por_partido": round(puntos / partidos, 1) if partidos > 0 else 0,
        "rebotes_por_partido": round(rebotes / partidos, 1) if partidos > 0 else 0,
        "asistencias_por_partido": round(asistencias / partidos, 1) if partidos > 0 else 0,
        "robos_por_partido": round(robos / partidos, 1) if partidos > 0 else 0,
        "tapones_por_partido": round(tapones / partidos, 1) if partidos > 0 else 0
    }

#clasificacion de la liga
def obtener_clasificacion_liga():
    standings = LeagueStandings()
    df = standings.get_data_frames()[0]

    resultados = []

    for _, fila in df.iterrows():
        resultados.append({
            "equipo": fila["TeamName"],
            "conferencia": fila["Conference"],
            "victorias": int(fila["WINS"]),
            "derrotas": int(fila["LOSSES"]),
            "pct": fila["WinPCT"]
        })

    return resultados

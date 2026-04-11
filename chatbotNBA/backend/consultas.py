from cx_bd import conexion

def cargar_equipos():
    con = conexion()
    cur = con.cursor()
    cur.execute("SELECT nombre, abreviatura FROM equipos")
    datos = cur.fetchall()
    con.close()
    return [(fila["nombre"], fila["abreviatura"]) for fila in datos]

def cargar_jugadores():
    con = conexion()
    cur = con.cursor()
    cur.execute("SELECT nombre FROM jugadores")
    datos = cur.fetchall()
    con.close()
    return [fila["nombre"] for fila in datos]

def obtener_jugadores_equipo(nombre_equipo):
    con = conexion()
    cur = con.cursor()
    sql = """
    SELECT j.nombre, j.posicion, j.dorsal
    FROM jugadores j
    JOIN equipos e ON j.id_equipo = e.id_equipo
    WHERE LOWER(e.nombre) = ?
    ORDER BY j.nombre
    """
    cur.execute(sql, (nombre_equipo.lower(),))
    datos = cur.fetchall()
    con.close()
    return [(fila["nombre"], fila["posicion"], fila["dorsal"]) for fila in datos]

def obtener_equipo_jugador(nombre_jugador):
    con = conexion()
    cur = con.cursor()
    sql = """
    SELECT j.nombre, e.nombre AS equipo
    FROM jugadores j
    JOIN equipos e ON j.id_equipo = e.id_equipo
    WHERE LOWER(j.nombre) = ?
    """
    cur.execute(sql, (nombre_jugador.lower(),))
    fila = cur.fetchone()
    con.close()

    if fila:
        return fila["nombre"], fila["equipo"]
    return None

def obtener_info_jugador(nombre_jugador):
    con = conexion()
    cur = con.cursor()
    sql = """
    SELECT j.nombre, j.posicion, j.dorsal, e.nombre AS equipo
    FROM jugadores j
    JOIN equipos e ON j.id_equipo = e.id_equipo
    WHERE LOWER(j.nombre) = ?
    """
    cur.execute(sql, (nombre_jugador.lower(),))
    fila = cur.fetchone()
    con.close()

    if fila:
        return fila["nombre"], fila["posicion"], fila["dorsal"], fila["equipo"]
    return None

def obtener_info_equipo(nombre_equipo):
    con = conexion()
    cur = con.cursor()
    sql = """
    SELECT nombre, ciudad, conferencia, division, abreviatura
    FROM equipos
    WHERE LOWER(nombre) = ?
    """
    cur.execute(sql, (nombre_equipo.lower(),))
    fila = cur.fetchone()
    con.close()

    if fila:
        return (
            fila["nombre"],
            fila["ciudad"],
            fila["conferencia"],
            fila["division"],
            fila["abreviatura"]
        )
    return None

def guardar_interaccion(pregunta, respuesta, fuente="BD"):
    con = conexion()
    cur = con.cursor()
    sql = """
    INSERT INTO interacciones (pregunta, respuesta, fuente)
    VALUES (?, ?, ?)
    """
    cur.execute(sql, (pregunta, respuesta, fuente))
    con.commit()
    con.close()

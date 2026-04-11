import sqlite3
import os
import sys

def obtener_ruta_base():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = obtener_ruta_base()
BD = os.path.join(BASE_DIR, "chatbotnba.db")

def conexion():
    con = sqlite3.connect(BD)
    con.row_factory = sqlite3.Row
    return con



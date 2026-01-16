import json
import random
import requests
from datetime import datetime
from pathlib import Path
from typing import Any

class Helpers:
    """Clase de utilidades (métodos estáticos) para operaciones comunes."""

    @staticmethod
    def obtener_diferencia_entre_fechas(fecha1: datetime, fecha2: datetime) -> int:
        """Devuelve la diferencia en días entre dos datetimes (valor absoluto)."""
        return abs((fecha2.date() - fecha1.date()).days)

    @staticmethod
    def obtener_dato_de_un_json(nombre_json: str, indice: int, dato1: str, dato2: str | None = None) -> Any:
        """Lee <nombre_json>.json y devuelve el elemento solicitado.

        Nota: asume que el archivo, la clave y el índice existen.
        """
        path = Path(f"{nombre_json}.json")
        with path.open("r", encoding="utf-8") as archivo:
            json_completo = json.load(archivo)

        return json_completo[dato1][indice][dato2] if dato2 is not None else json_completo[dato1][indice]
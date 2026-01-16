import json
import requests
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from twitter import publicar_tweet

API_FERIADOS = "https://api.argentinadatos.com/v1/feriados"
ARCHIVO_CACHE = Path(__file__).parent / "feriados.json"


def obtener_feriados_api(año: int) -> list[dict]:
    """Obtiene los feriados desde la API de Argentina Datos."""
    try:
        response = requests.get(f"{API_FERIADOS}/{año}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener feriados de la API: {e}")
        return []


def guardar_cache(feriados: list[dict]) -> None:
    """Guarda los feriados en el archivo JSON."""
    with open(ARCHIVO_CACHE, "w", encoding="utf-8") as archivo:
        json.dump(feriados, archivo, ensure_ascii=False, indent=2)
    print("Feriados guardados en caché.")


def cache_es_valido(año_actual: int) -> bool:
    """Verifica si el caché existe y tiene feriados del año actual."""
    if not ARCHIVO_CACHE.exists():
        return False

    try:
        with open(ARCHIVO_CACHE, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        # Soporta formato viejo {"listaFeriados": [...]} y nuevo [...]
        feriados = datos.get("listaFeriados", datos) if isinstance(datos, dict) else datos

        if not feriados:
            return False

        primer_feriado = feriados[0].get("fecha", "")
        año_cache = int(primer_feriado.split("-")[0])
        return año_cache == año_actual
    except (json.JSONDecodeError, ValueError, IndexError, KeyError, TypeError):
        return False


def cargar_feriados(año: int) -> list[dict]:
    """Carga feriados del caché si es válido, sino consulta la API."""
    if cache_es_valido(año):
        print("Usando feriados del caché.")
        with open(ARCHIVO_CACHE, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    print("Consultando API de feriados...")
    feriados = obtener_feriados_api(año)
    if feriados:
        guardar_cache(feriados)
    return feriados


def obtener_proximo_feriado(feriados: list[dict], ahora: datetime) -> dict | None:
    """Devuelve el próximo feriado a partir de la fecha actual."""
    hoy = ahora.date()

    for feriado in feriados:
        fecha_feriado = datetime.strptime(feriado["fecha"], "%Y-%m-%d").date()
        if fecha_feriado >= hoy:
            return feriado

    return None


def calcular_tiempo_restante(fecha_feriado: str, ahora: datetime) -> tuple[int, int, int]:
    """Calcula días, horas y minutos restantes hasta el feriado."""
    fecha_objetivo = datetime.strptime(fecha_feriado, "%Y-%m-%d")
    fecha_objetivo = fecha_objetivo.replace(tzinfo=ahora.tzinfo)

    diferencia = fecha_objetivo - ahora

    dias = diferencia.days
    horas = diferencia.seconds // 3600
    minutos = (diferencia.seconds % 3600) // 60

    return dias, horas, minutos


def generar_mensaje(feriado: dict, dias: int, horas: int, minutos: int) -> str:
    """Genera el mensaje del tweet según el tiempo restante."""
    nombre = feriado["nombre"]
    fecha = datetime.strptime(feriado["fecha"], "%Y-%m-%d").strftime("%d/%m")

    if dias == 0:
        return (
            f"🎉 ¡HOY ES {nombre}!\n\n"
            f"¡A disfrutar el día! 🇦🇷"
        )
    elif dias == 1:
        return (
            f"⏰ ¡MAÑANA ES FERIADO!\n\n"
            f"📅 {nombre} ({fecha})\n\n"
            f"⏳ Faltan {horas}h {minutos}min\n\n"
        )
    else:
        return (
            f"📆 Próximo feriado: {nombre} ({fecha})\n\n"
            f"⏳ Faltan {dias} días, {horas}h {minutos}min"
        )


def main():
    zona_argentina = ZoneInfo("America/Buenos_Aires")
    ahora = datetime.now(zona_argentina)

    feriados = cargar_feriados(ahora.year)
    proximo = obtener_proximo_feriado(feriados, ahora)

    if proximo is None:
        print("No hay más feriados este año.")
        return

    dias, horas, minutos = calcular_tiempo_restante(proximo["fecha"], ahora)
    mensaje = generar_mensaje(proximo, dias, horas, minutos)

    print(f"Mensaje a publicar:\n{mensaje}")
    publicar_tweet(mensaje)


if __name__ == "__main__":
    main()
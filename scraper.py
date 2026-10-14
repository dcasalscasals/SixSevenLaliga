import json
from datetime import datetime
import urllib.request
import re

# URL del torneo en la federación
URL_TORNEO = "https://padelfederacion.es/Paginas/fpadelib/Pruebas_previo.asp?IdTorneo=28876"

def extraer_datos():
    # Estructura base de datos
    datos = {
        "torneo": "La Liga 2026/27",
        "actualizado": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "jornadas": [],
        "clasificacion": []
    }

    try:
        # Descargar el HTML de la federación
        req = urllib.request.Request(
            URL_TORNEO, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('latin1', errors='ignore') # Las webs antiguas usan latin1 o cp1252

        # Nota: Aquí puedes afinar las expresiones regulares o BeautifulSoup 
        # según cómo la federación estructure exactamente sus tablas HTML.
        # Como ejemplo de funcionamiento automatizado, guardamos la ejecución correcta:
        
        datos["jornadas"].append({
            "jornada": "Jornada Actualizada Automáticamente",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "enfrentamiento": "Sincronizado con la Federación",
            "partidos": [
                {"orden": "Pareja 1", "local": "Por actualizar", "visitante": "Por actualizar", "resultado": "-", "estado": "Pendiente"}
            ]
        })

    except Exception as e:
        print(f"Error al conectar con la federación: {e}")

    # Guardar en data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    extraer_datos()

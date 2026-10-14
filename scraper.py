import json
from datetime import datetime
import urllib.request
import re

# Parámetros fijos de tu liga y grupo en la federación
LIGA = "28876"
GRUPO = "32942"
MI_EQUIPO = "SIX SEVEN"
MAX_JORNADAS = 5  # Ampliable según las jornadas totales de la liga

def descargar_html(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
        )
        with urllib.request.urlopen(req) as response:
            return response.read().decode('latin1', errors='ignore')
    except Exception as e:
        print(f"Error descargando {url}: {e}")
        return ""

def extraer_todo():
    datos = {
        "torneo": "LA LIGA FPIB 26/27 (MENORCA) - DIVISIÓN AZUL MASCULINA",
        "mi_equipo": MI_EQUIPO,
        "actualizado": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "jornadas": [],
        "clasificacion": []
    }

    # 1. Extraer Clasificación General
    url_clasificacion = f"https://www.padelfederacion.es/Paginas/fpadelib/Ligas_Clasificacion.asp?Liga={LIGA}&grupo={GRUPO}"
    html_clas = descargar_html(url_clasificacion)
    
    if html_clas:
        # Expresión regular para capturar las filas de la tabla de clasificación
        filas = re.findall(r'<tr class="LineasRnk">(.*?)</tr>', html_clas, re.DOTALL)
        for fila in filas:
            columnas = re.findall(r'<td[^>]*>(.*?)</td>', fila, re.DOTALL)
            if len(columnas) >= 10:
                pos = re.sub(r'<.*?>', '', columnas[0]).strip()
                equipo = re.sub(r'<.*?>', '', columnas[1]).strip()
                jj = re.sub(r'<.*?>', '', columnas[2]).strip()
                pt = re.sub(r'<.*?>', '', columnas[3]).strip()
                jg = re.sub(r'<.*?>', '', columnas[4]).strip()
                jp = re.sub(r'<.*?>', '', columnas[5]).strip()
                pg = re.sub(r'<.*?>', '', columnas[6]).strip()
                pp = re.sub(r'<.*?>', '', columnas[7]).strip()
                sg = re.sub(r'<.*?>', '', columnas[8]).strip()
                sp = re.sub(r'<.*?>', '', columnas[9]).strip()

                datos["clasificacion"].append({
                    "pos": int(pos) if pos.isdigit() else 0,
                    "equipo": equipo,
                    "jj": int(jj) if jj.isdigit() else 0,
                    "pt": int(pt) if pt.isdigit() else 0,
                    "jg": int(jg) if jg.isdigit() else 0,
                    "jp": int(jp) if jp.isdigit() else 0,
                    "pg": int(pg) if pg.isdigit() else 0,
                    "pp": int(pp) if pp.isdigit() else 0,
                    "sg": int(sg) if sg.isdigit() else 0,
                    "sp": int(sp) if sp.isdigit() else 0
                })

    # 2. Extraer Calendario y Jornadas (Bucle de la 1 a la MAX_JORNADAS)
    for j in range(1, MAX_JORNADAS + 1):
        url_jornada = f"https://www.padelfederacion.es/Paginas/fpadelib/Ligas_Calendario.asp?grupo={GRUPO}&Liga={LIGA}&jornada={j}"
        html_jor = descargar_html(url_jornada)
        
        if html_jor and "LineasRnk" in html_jor:
            enfrentamientos_jornada = []
            filas_jor = re.findall(r'<tr class="LineasRnk">(.*?)</tr>', html_jor, re.DOTALL)
            
            for fila in filas_jor:
                cols = re.findall(r'<td[^>]*>(.*?)</td>', fila, re.DOTALL)
                if len(cols) >= 5:
                    local = re.sub(r'<.*?>', '', cols[0]).strip()
                    res_local = re.sub(r'<.*?>', '', cols[1]).strip()
                    res_visitante = re.sub(r'<.*?>', '', cols[2]).strip()
                    visitante = re.sub(r'<.*?>', '', cols[3]).strip()
                    
                    info_fecha = re.sub(r'<.*?>', ' ', cols[4]).strip()
                    
                    enfrentamientos_jornada.append({
                        "local": local,
                        "visitante": visitante,
                        "resultado_global": f"{res_local} - {res_visitante}",
                        "fecha": info_fecha,
                        "lugar": "Menorca",
                        "partidos": [
                            {"orden": "Pareja 1-3", "local_jugadores": ["Ver acta en federación"], "visitante_jugadores": ["Ver acta en federación"], "sets": f"{res_local}-{res_visitante}", "ganador": "local" if res_local > res_visitante else "visitante"}
                        ]
                    })
            
            if enfrentamientos_jornada:
                datos["jornadas"].append({
                    "jornada": f"Jornada {j}",
                    "enfrentamientos": enfrentamientos_jornada
                })

    # Guardar el resultado en data.json para que la web lo lea al instante
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print("¡Datos actualizados con éxito!")

if __name__ == "__main__":
    extraer_todo()

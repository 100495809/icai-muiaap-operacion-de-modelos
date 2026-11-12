
import os
from pathlib import Path
from dotenv import load_dotenv

import requests
import pandas as pd

load_dotenv()
api_key = os.getenv("API_KEY")

# Consultar el inventario para localizar la estación
url_estaciones = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/")

respuesta = requests.get(url_estaciones, params={"api_key": api_key}, timeout=30)
respuesta.raise_for_status()

# AEMET devuelve una URL en el campo "datos"
url_datos_estaciones = respuesta.json()["datos"]

respuesta_estaciones = requests.get(url_datos_estaciones, timeout=30)
respuesta_estaciones.raise_for_status()

estaciones = respuesta_estaciones.json()
df_estaciones = pd.DataFrame(estaciones)

# Buscar estaciones cuyo nombre contenga "Ciudad Universitaria"
print(df_estaciones[df_estaciones["nombre"].str.contains( "Ciudad Universitaria", case=False, na=False)])



Id_estacion = ""
for estacion in estaciones:
    if estacion["nombre"] == "MADRID, CIUDAD UNIVERSITARIA":
        Id_estacion=estacion["indicativo"]

# Id_estacion = "3194U"


fecha_inicio = "2019-10-01T00:00:00UTC"
fecha_fin = "2019-10-31T23:59:59UTC"

url_datos = (
    f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_inicio}/fechafin/{fecha_fin}/estacion/{Id_estacion}")


respuesta_ciu = requests.get(
    url_datos,
    params={"api_key": api_key},
    timeout=30
)

respuesta_ciu.raise_for_status()

resultado_ciu = respuesta_ciu.json()

if resultado_ciu.get("estado") != 200:
    raise RuntimeError(
        f"Error de AEMET: {resultado_ciu}"
    )

# Una vez que tenemos la URL de los datos, hacemos otra petición para obtenerlos

respuesta_datos = requests.get(
    resultado_ciu["datos"],
    params={"api_key": api_key},
    timeout=60
)

respuesta_datos.raise_for_status()

datos = respuesta_datos.json()

# Convertir los resultados a un DataFrame
df = pd.DataFrame(datos)

# print(df.head())
print(f"Número de registros: {len(df)}")


# Guardar los datos obtenidos
output_path = Path("modules/07-AEMET-API/data/climatologia_madrid_octubre_2019.csv")
output_path.parent.mkdir(parents=True, exist_ok = True)
df.to_csv(output_path,index=False)
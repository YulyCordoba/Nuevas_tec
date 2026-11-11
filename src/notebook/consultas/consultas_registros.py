"""Consultas sobre la tabla registros con pandas.

Lee data/limpio/registros_limpio.csv (el archivo LIMPIO, no el sucio), responde
cinco consultas (cada una en su propia función), imprime la pregunta y el
resultado de cada una en orden y guarda data/limpio/registros_consulta_N.csv.

Se puede ejecutar solo (python src/notebook/consultas/consultas_registros.py) o
importarse desde main.py con: from consultas.consultas_registros import ejecutar_consultas
"""

import sys
from pathlib import Path

import pandas as pd

# src/notebook/consultas/consultas_registros.py -> sube 3 niveles hasta la raíz del proyecto
RAIZ = Path(__file__).resolve().parents[3]
CARPETA_LIMPIO = RAIZ / "data" / "limpio"
RUTA_ENTRADA = CARPETA_LIMPIO / "registros_limpio.csv"

COLUMNAS_NECESARIAS = ["id", "id_usuario", "id_reto", "estado", "mes"]


def cargar_datos(ruta):
    """Lee el CSV limpio y valida que tenga las columnas necesarias."""
    df = pd.read_csv(ruta)
    faltan = [c for c in COLUMNAS_NECESARIAS if c not in df.columns]
    if faltan:
        sys.exit(f"Error: a {ruta} le faltan las columnas {faltan}. Columnas: {list(df.columns)}")
    return df


def guardar(resultado, carpeta, numero):
    """Guarda el resultado de la consulta N como registros_consulta_N.csv."""
    ruta = Path(carpeta) / f"registros_consulta_{numero}.csv"
    resultado.to_csv(ruta, index=True if resultado.index.name else False, encoding="utf-8")
    return ruta


def consulta_1(df, carpeta):
    """Consulta 1: participaciones ya finalizadas (filtro por estado)."""
    print("\n=== Consulta 1: ¿Qué participaciones ya finalizaron? ===")
    finalizados = df[df["estado"] == "FINALIZADO"]
    print(f"Total: {len(finalizados)}")
    print(finalizados.head(10).to_string(index=False))
    guardar(finalizados, carpeta, 1)
    return finalizados


def consulta_2(df, carpeta):
    """Consulta 2: participaciones repetidas (mismo usuario en el mismo reto)."""
    print("\n=== Consulta 2: ¿Qué participaciones están repetidas (mismo usuario en el mismo reto)? ===")
    repetidos = df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]
    repetidos = repetidos.sort_values(["id_usuario", "id_reto"])
    print(f"Filas involucradas en repeticiones: {len(repetidos)}")
    print(repetidos.head(10).to_string(index=False))
    guardar(repetidos, carpeta, 2)
    return repetidos


def consulta_3(df, carpeta):
    """Consulta 3: cuántas participaciones hay por estado (value_counts)."""
    print("\n=== Consulta 3: ¿Cuántas participaciones hay por estado? ===")
    conteo = df["estado"].value_counts().rename("cantidad")
    conteo.index.name = "estado"
    print(conteo.to_string())
    guardar(conteo, carpeta, 3)
    return conteo


def consulta_4(df, carpeta):
    """Consulta 4 (groupby): los 10 retos con más participantes."""
    print("\n=== Consulta 4: ¿Cuáles son los 10 retos con más participantes? ===")
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10).rename("cantidad_participantes")
    print(top_retos.to_string())
    guardar(top_retos, carpeta, 4)
    return top_retos


def consulta_5(df, carpeta):
    """Consulta 5 (groupby): cuántas participaciones hubo cada mes."""
    print("\n=== Consulta 5: ¿Cuántas participaciones hubo cada mes? ===")
    por_mes = df.groupby("mes")["id"].count().rename("cantidad")
    print(por_mes.to_string())
    guardar(por_mes, carpeta, 5)
    return por_mes


def ejecutar_consultas(ruta_entrada=RUTA_ENTRADA, carpeta_salida=CARPETA_LIMPIO):
    """Carga los datos limpios y corre las cinco consultas en orden."""
    ruta_entrada = Path(ruta_entrada)
    if not ruta_entrada.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta_entrada}. Ejecuta primero la limpieza (L01)."
        )
    carpeta_salida = Path(carpeta_salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    df = cargar_datos(ruta_entrada)
    print(f"Filas leídas: {len(df)}")

    consulta_1(df, carpeta_salida)
    consulta_2(df, carpeta_salida)
    consulta_3(df, carpeta_salida)
    consulta_4(df, carpeta_salida)
    consulta_5(df, carpeta_salida)

    print(f"\nListo: se guardaron registros_consulta_1.csv ... registros_consulta_5.csv en {carpeta_salida}")


if __name__ == "__main__":
    ejecutar_consultas()
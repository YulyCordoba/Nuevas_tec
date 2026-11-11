"""Reporte de la tabla registros: tres gráficas con matplotlib y conclusiones.

Lee data/limpio/registros_limpio.csv, guarda las tres gráficas en reportes/ e
imprime las conclusiones.

Se puede ejecutar solo (python src/notebook/graficacion/reporte_registros.py) o
importarse desde main.py con: from graficacion.reporte_registros import generar_reporte
"""

import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Sin ventana: el script guarda las imágenes y no se queda esperando
import matplotlib.pyplot as plt
import pandas as pd

# src/notebook/graficacion/reporte_registros.py -> sube 3 niveles hasta la raíz del proyecto
RAIZ = Path(__file__).resolve().parents[3]
RUTA_ENTRADA = RAIZ / "data" / "limpio" / "registros_limpio.csv"
CARPETA_REPORTES = RAIZ / "reportes"

COLUMNAS_NECESARIAS = ["id", "id_usuario", "id_reto", "estado", "mes"]

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre",
    11: "noviembre", 12: "diciembre",
}


def cargar_datos(ruta):
    """Lee registros_limpio.csv y valida que tenga las columnas necesarias."""
    df = pd.read_csv(ruta)
    faltan = [c for c in COLUMNAS_NECESARIAS if c not in df.columns]
    if faltan:
        sys.exit(f"Error: a {ruta} le faltan las columnas {faltan}. Columnas: {list(df.columns)}")
    return df


def guardar_grafica(ruta):
    """Ajusta el diseño, guarda la figura actual con dpi=120 y la cierra."""
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica guardada: {ruta}")


def grafica_estados(df, carpeta):
    """Gráfica 1 (barras): participaciones por estado."""
    conteo = df["estado"].value_counts()
    plt.figure(figsize=(8, 5))
    conteo.plot(kind="bar")
    plt.title("Participaciones por estado")
    plt.xlabel("Estado")
    plt.ylabel("Cantidad de participaciones")
    plt.xticks(rotation=0)
    guardar_grafica(os.path.join(carpeta, "registros_grafica_1.png"))
    return conteo


def grafica_por_mes(df, carpeta):
    """Gráfica 2 (línea): participaciones por mes."""
    por_mes = df.groupby("mes")["id"].count()
    plt.figure(figsize=(9, 5))
    por_mes.plot(kind="line", marker="o")
    plt.title("Participaciones por mes")
    plt.xlabel("Mes")
    plt.ylabel("Cantidad de participaciones")
    plt.xticks(range(len(por_mes)), por_mes.index, rotation=45)
    guardar_grafica(os.path.join(carpeta, "registros_grafica_2.png"))
    return por_mes


def grafica_top_retos(df, carpeta):
    """Gráfica 3 (barras horizontales): los 10 retos con más participantes."""
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10)
    plt.figure(figsize=(10, 5))
    # Se invierte para que el reto con más participantes quede arriba.
    top_retos.iloc[::-1].plot(kind="barh")
    plt.title("Top 10 retos con más participantes")
    plt.xlabel("Cantidad de participantes")
    plt.ylabel("Reto (id)")
    guardar_grafica(os.path.join(carpeta, "registros_grafica_3.png"))
    return top_retos


def imprimir_conclusiones(df, top_retos, por_mes):
    """Imprime las conclusiones: reto más popular, mes pico y duplicados."""
    print("\n=== CONCLUSIONES ===")

    # 1. Reto más popular
    reto = top_retos.idxmax()
    print(f"1. El reto más popular es {reto}, con {int(top_retos.max())} participantes.")

    # 2. Mes con más inscripciones
    periodo = por_mes.idxmax()
    mes_num = int(periodo.split("-")[1])
    n_pico = int(por_mes.max())
    print(f"2. El mes con más inscripciones fue {MESES[mes_num]} ({periodo}): "
          f"{n_pico} de {int(por_mes.sum())} participaciones ({n_pico / por_mes.sum():.0%}).")

    # 3. Inscripciones duplicadas (mismo usuario en el mismo reto)
    mascara = df.duplicated(subset=["id_usuario", "id_reto"], keep=False)
    sobrantes = int(df.duplicated(subset=["id_usuario", "id_reto"], keep="first").sum())
    pares = int(df[mascara].groupby(["id_usuario", "id_reto"]).ngroups)
    print(f"3. Se encontraron {sobrantes} inscripciones duplicadas "
          f"({int(mascara.sum())} filas en {pares} pares usuario-reto repetidos).")
    print("   El back debe bloquearlas con un error 409 (Conflict): un usuario no puede "
          "inscribirse dos veces al mismo reto; el recurso ya existe, así que el cliente "
          "no debe reintentar. Sin esa validación se inflan los conteos de participantes "
          "y el ranking de retos populares queda distorsionado.")


def generar_reporte(ruta_entrada=RUTA_ENTRADA, carpeta_reportes=CARPETA_REPORTES):
    """Crea las tres gráficas en reportes/ e imprime las conclusiones."""
    ruta_entrada = Path(ruta_entrada)
    if not ruta_entrada.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta_entrada}. Ejecuta primero la limpieza (L01)."
        )
    carpeta_reportes = str(carpeta_reportes)
    os.makedirs("reportes", exist_ok=True)
    os.makedirs(carpeta_reportes, exist_ok=True)

    df = cargar_datos(ruta_entrada)
    print(f"Filas leídas: {len(df)}")
    grafica_estados(df, carpeta_reportes)
    por_mes = grafica_por_mes(df, carpeta_reportes)
    top_retos = grafica_top_retos(df, carpeta_reportes)
    imprimir_conclusiones(df, top_retos, por_mes)


if __name__ == "__main__":
    generar_reporte()

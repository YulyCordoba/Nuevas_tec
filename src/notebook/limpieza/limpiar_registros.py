from pathlib import Path

import pandas as pd

RUTA_ENTRADA = Path("data/crudo/registros_sucio.csv")
RUTA_SALIDA = Path("data/limpio/registros_limpio.csv")


def leer_csv(ruta):
    return pd.read_csv(ruta)


def imprimir_diagnostico(df, titulo):
    print("=" * 60)
    print(titulo)
    print("=" * 60)
    print(f"df.shape: {df.shape}")
    print("\ndf.info():")
    df.info()
    print("\ndf.isna().sum():")
    print(df.isna().sum())
    print(f"\ndf.duplicated().sum(): {df.duplicated().sum()}\n")

def quitar_duplicados(df):
    """Elimina las filas idénticas."""
    return df.drop_duplicates()


def convertir_fechas(df):
    """Convierte fecha_registro (texto en dos formatos) a fecha real."""
    iso = pd.to_datetime(df["fecha_registro"],
                         format="%Y-%m-%d %H:%M:%S", errors="coerce")
    latino = pd.to_datetime(df["fecha_registro"],
                            format="%d/%m/%Y %H:%M", errors="coerce")
    df["fecha_registro"] = iso.fillna(latino)
    return df


def unificar_estado(df):
    """Quita espacios, pasa a mayúsculas y cambia espacios internos por guion bajo
    (INSCRITO, EN_PROCESO, FINALIZADO), igual que en retos."""
    df["estado"] = df["estado"].str.strip().str.upper().str.replace(" ", "_")
    return df


def crear_mes(df):
    """Crea la columna mes (AAAA-MM) a partir de fecha_registro, para el groupby."""
    df["mes"] = df["fecha_registro"].dt.to_period("M").astype(str)
    return df


def rellenar_observaciones(df):
    """Pone 'Sin observacion' donde no hay texto."""
    df["observacion"] = df["observacion"].fillna("Sin observacion")
    return df

def guardar_csv(df, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Archivo guardado en: {ruta}")


def limpiar_registros(ruta_entrada=RUTA_ENTRADA, ruta_salida=RUTA_SALIDA):
    df = leer_csv(ruta_entrada)
    imprimir_diagnostico(df, "DIAGNOSTICO ANTES DE LIMPIAR")

    df = quitar_duplicados(df)
    df = convertir_fechas(df)
    df = unificar_estado(df)
    df = rellenar_observaciones(df)
    df = crear_mes(df)
    # OJO: ya no se llama quitar_inscripciones_dobles(df). Los pares usuario-reto
    # repetidos se dejan en el CSV limpio a propósito: la consulta 2 y las
    # conclusiones del reporte necesitan verlos (el back los bloqueará con 409).

    imprimir_diagnostico(df, "DIAGNOSTICO DESPUES DE LIMPIAR")
    guardar_csv(df, ruta_salida)
    return df

def quitar_inscripciones_dobles(df):
    """Deja una sola inscripción por usuario y reto (la más antigua)."""
    df = df.sort_values("fecha_registro")
    df = df.drop_duplicates(subset=["id_usuario", "id_reto"], keep="first")
    return df.sort_index()


if __name__ == "__main__":
    limpiar_registros()
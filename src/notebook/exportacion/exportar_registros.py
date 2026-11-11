import os
from simulacion.simular_registros import generar_registros
from pathlib import Path

CARPETA = "data/crudo"


def exportar(df, carpeta=CARPETA):
    os.makedirs(carpeta, exist_ok=True)

    ruta_csv = os.path.join(carpeta, "registros_sucio.csv")
    ruta_xlsx = os.path.join(carpeta, "registros_sucio.xlsx")
    ruta_json = os.path.join(carpeta, "registros_sucio.json")

    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    df.to_excel(ruta_xlsx, index=False, sheet_name="registros")
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)

    return [ruta_csv, ruta_xlsx, ruta_json]

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from simulacion.simular_registros import generar_registros

    df = generar_registros()
    for ruta in exportar(df):
        print(ruta, df.shape)
import random
import uuid
import pandas as pd
from faker import Faker

# 1. Configuración de Faker y semillas
fake = Faker("es_CO")

# 2. Sembrar semillas para tener coherencia en los datos simulados
Faker.seed(42)
random.seed(42)

# 3. Constantes
ESTADOS = ["Inscrito", "En proceso", "Finalizado"]

FILAS = 800

def nuevo_uuid():
    return str(uuid.UUID(int=random.getrandbits(128), version=4))

IDS_USUARIO = [str(uuid.uuid4()) for _ in range(100)]
IDS_RETO = [str(uuid.uuid4()) for _ in range(50)]


# 4. Función para generar registros
def generar_registros(n=800):

    # Pares usuario-reto únicos: así los únicos repetidos son los que
    # se introducen a propósito en ensuciar() (10%)
    pares = random.sample(
        [(u, r) for u in IDS_USUARIO for r in IDS_RETO], n
    )

    filas = []

    for id_usuario, id_reto in pares:
        filas.append({
            "id": str(uuid.uuid4()),
            "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": id_usuario,
            "id_reto": id_reto,
        })

    df = pd.DataFrame(filas)

    return ensuciar(df)


# 5. Función para ensuciar los datos
def ensuciar(datos_df):
    datos_df = datos_df.copy()
    n = len(datos_df)
    indices = list(datos_df.index)

    # 1. 20% de observaciones vacías
    idx = random.sample(indices, round(n * 0.20))
    datos_df.loc[idx, "observacion"] = None

    # 2. Estados con formatos inconsistentes
    idx = random.sample(indices, round(n * 0.05))
    variantes = ["inscrito", "EN PROCESO", " Finalizado "]
    datos_df.loc[idx, "estado"] = [
        random.choice(variantes) for _ in idx
    ]

    # 3. Fechas con dos formatos diferentes
    iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")

    datos_df["fecha_registro"] = iso
    idx = random.sample(indices, round(n * 0.40))
    datos_df.loc[idx, "fecha_registro"] = latino.loc[idx]

    # 4. 10% con pares usuario-reto repetidos
    idx_pares = random.sample(indices, round(n * 0.10))
    disponibles = [i for i in indices if i not in idx_pares]
    fuentes = random.sample(disponibles, len(idx_pares))

    for destino, fuente in zip(idx_pares, fuentes):
        datos_df.loc[destino, ["id_usuario", "id_reto"]] = (
            datos_df.loc[fuente, ["id_usuario", "id_reto"]].values
        )

    # 5. 5% de duplicados exactos
    disponibles = [i for i in indices if i not in idx_pares]
    idx_duplicados = random.sample(disponibles, round(n * 0.05))
    fuentes = random.sample(
        [i for i in indices if i not in idx_duplicados],
        len(idx_duplicados)
    )

    for destino, fuente in zip(idx_duplicados, fuentes):
        datos_df.loc[destino] = datos_df.loc[fuente].values

    return datos_df


# 6. Ejecución del script
if __name__ == "__main__":

    df = generar_registros(n=FILAS)

    print(df.shape)
    print(df.head())
    print(df.isna().sum())
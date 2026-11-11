from pathlib import Path

from simulacion.simular_registros import generar_registros
from exportacion.exportar_registros import exportar
from limpieza.limpiar_registros import limpiar_registros
from consultas.consultas_registros import ejecutar_consultas
from graficacion.reporte_registros import generar_reporte

# 1. Simulación (F01)
print("***SIMULACION DE REGISTROS***")
registros_df = generar_registros(800)
print(registros_df.shape)

# 2. Exportación (X01)
print("***EXPORTANDO DATOS***")
rutas = exportar(registros_df)
for ruta in rutas:
    print(f"{ruta} | shape={registros_df.shape} | creado={Path(ruta).exists()}")

# 3. Limpieza (L01): lee el CSV recién exportado
print("***LIMPIEZA***")
entrada = Path("data/crudo/registros_sucio.csv")
salida = Path("data/limpio/registros_limpio.csv")
df_limpio = limpiar_registros(entrada, salida)
print(f"registros_limpio.csv | shape={df_limpio.shape} | creado={salida.exists()}")

# 4. Consultas (Q01): lee el CSV limpio y guarda registros_consulta_N.csv
print("***CONSULTAS***")
ejecutar_consultas(salida, Path("data/limpio"))

# 5. Gráficas y conclusiones (G01): lee el CSV limpio y guarda PNG en reportes/
print("***GRAFICAS Y CONCLUSIONES***")
generar_reporte(salida, Path("reportes"))
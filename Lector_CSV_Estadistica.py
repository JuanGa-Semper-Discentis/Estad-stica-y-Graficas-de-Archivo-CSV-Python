import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
#funciones de estadistica de scipy
import tkinter as tk
from tkinter import scrolledtext #hacer scroll en ventana tkinter
#import matplotlib as 

#Ruta del archivo CSV
#seleccionar archivo
ruta_csv = r"C:\Users\User\Downloads\Archivo_CSV_Original.csv" #ORIGINAL
#ruta_csv = r"C:\Users\User\Downloads\Archivo_CSV_Escenario_X.csv" #ESCENARIO
#         ^ solo recibe un unico CSV
#         ^ Cuidado con la direccion

#carga y lectura del csv en dataframe
df = pd.read_csv(ruta_csv) # uso de pd

# convertir fecha de str a fecha util para librerias
df["Fecha"] = pd.to_datetime(df["Fecha"])

# buscar columna de precipitacion
if "Precipitacion" in df.columns: #verificacion de existencia de columna
    data = df["Precipitacion"].dropna() #dropna elimina espacios vacios
#segun el IMN el minio de lectura es de 0.1 a 0.2mm de agua
else:
    columnas_numericas = df.select_dtypes(include=np.number).columns
    #                          ^^^^ solo columnas con valores numericos => columns retorna nombres
    if len(columnas_numericas) == 0:
        raise ValueError("No hay columnas numericas en el archivo CSV")
    #   ^ detiene todo si no encuentra nada
    data = df[columnas_numericas[0]].dropna()
    # ^ usar primera con datos

total_dias = data.count()

dias_secos = (data <= 0.1).sum()
dias_lluvia = (data > 0.1).sum()

precipitacion_total = data.sum()

intensidad_media_lluvia = data[data > 0.1].mean()


#tendencia central de los datos
#revisar datos en graficadora

media = data.mean()
#            ^ promedio aritmetico sensible de pandas
mediana = data.median()
#              ^ valor central no sensible
moda_series = data.mode()
#                  ^ serie de mas frecuentes, puede existir empates
moda = moda_series.iloc[0] if len(moda_series) > 0 else np.nan
#                  ^ desempate, primer elemento por posicion
#                                                       ^ funcion not a number nulo de numpy
#                                                       ^ se debe usar si no existe moda

#dispersion de los datos

desviacion = data.std()
#                 ^ desviacion estandar por defecto de pandas
varianza = data.var()
#               ^ varianza de muestra, (std())^2

p10 = data.quantile(0.10)
p90 = data.quantile(0.90)

#p25 = data.quantile(0.25)
#p75 = data.quantile(0.75) #datos debajo de este %
#en estudios de este tipo segun las referencias se recomiendan percentiles 10% y 95%
#     ^^^ es normal que el P10 de NaN, debido a las cualidadesd e las series Gamma

rango_p10_p90 = p90 - p10
# dentro del 80% de los datos

#forma de los datos

asimetria = skew(data)
#           ^ asimetria de distribucion
#   skew>0 : cola larga derecha, muchos dias secos + pocos dias lluviosos
#   skew<0 : cola larga izquierda
#   skew =aprox= 0 : simetrica


curt = kurtosis(data) #<<<< documentar y refernciar
#      ^ de spicy stats, es para ver el apuntamiento de la distribucion
#   kurtosis>0 : mas fina que la normal, muchos valores en la media
#   kurtosis<0 : mas plana
#   kurtosis = 0 : igual a distribucion normal
#                ^^^ en el casode Gamma-Thom no es necesaria

"""
#estadisticas por año
df["Año"] = df["Fecha"].dt.year
precipitacion_anual = df.groupby("Año")["Precipitacion"].sum()
promedio_anual = df.groupby("Año")["Precipitacion"].mean()
total_mm = data.sum()
"""

# resumen de datos
resumen = pd.DataFrame({
    "Medida":[
        "Total de dias analizados",
        "Dias secos (≤0.1 mm)",
        "Dias con lluvia (>0.1 mm)",
        #"Precip. Anual",
        #"Promedio Anual",
        "Precipitacion total acumulada (mm)",
        "Intensidad media de lluvia (mm/dia lluvioso)",
        "Media",
        "Mediana",
        "Moda",
        "Desviacion estandar",
        "Varianza",
        "Percentil 10 (P10)",
        "Percentil 90 (P90)",
        "Rango P90-P10",
        "Asimetria (Skewness)",
        "Curtosis"
    ],
    "Valor":[
        total_dias,
        dias_secos,
        dias_lluvia,
        #precipitacion_anual,
        #promedio_anual,
        precipitacion_total,
        intensidad_media_lluvia,
        media,
        mediana,
        moda,
        desviacion,
        varianza,
        p10,
        p90,
        rango_p10_p90,
        asimetria,
        curt
    ]
})

"""
resumen2 = pd.DataFrame({
    "Medida":[
        "Precipitacion Total Año",
        "Promedio Total por Año"
    ]
    "Valor":[
        precipitacion_anual,
        promedio_anual
    ]
})

"""

# impresion en terminal

print("\n===== ANALISIS ESTADISTICO DE PRECIPITACION =====\n")
print(resumen)

#estadisticas por año
df["Año"] = df["Fecha"].dt.year
precipitacion_anual = df.groupby("Año")["Precipitacion"].sum()
promedio_anual = df.groupby("Año")["Precipitacion"].mean()
total_mm = data.sum()

print("\n===== PRECIPITACION TOTAL POR AÑO =====\n")
print(precipitacion_anual)

print("\n===== PROMEDIO DIARIO POR AÑO =====\n")
print(promedio_anual)


# tkinter1-----------------------------
texto = resumen.to_string(index=False)
#texto2 = resumen2.to_string(index=False)

ventana = tk.Tk()
ventana.title("Analisis Estadistico de Precipitacion")
ventana.geometry("500x400")

area = scrolledtext.ScrolledText(ventana, width=60, height=20)
area.pack(padx=10, pady=10)

#area.insert(tk.END, texto, precipitacion_anual, promedio_anual)
area.insert(tk.END, texto)
area.config(state="disabled")

ventana.mainloop()

#tkinter2-------------------------------
#definicion de texto
texto2 = (
    f"Precipitacion Total (mm): {total_mm: .2f}\n"
    f"\n===== PRECIPITACION TOTAL POR AÑO =====\n\n"
    f"{precipitacion_anual.to_string()}\n"
    f"\n===== PROMEDIO DIARIO POR AÑO (mm) =====\n\n"
    f"{promedio_anual.to_string()}\n"
)
ventana2 = tk.Tk() #definicion de segunda ventana en tkinter
ventana2.title("Estadisticas Precipitacion por Año")
ventana2.geometry("420x400") # === error en tramano

"""
tk.Label(
    ventana2,
    text="Estadisticas por Año",
    font=("Arial", 12, "bold")
).pack(pady=(10, 0))
"""

area2 = scrolledtext.ScrolledText(ventana2, width=50, height=20)
area2.pack(padx=10, pady=10)
area2.insert(tk.END, texto2)
area2.config(state="disabled")
ventana2.mainloop()

"""
Autor: Juan Gabriel Perez Acuña

Fuentes y documentacion:
pandas      :   https://pandas.pydata.org/docs/
numpy       :   https://numpy.org/doc/
scipy       :   https://docs.scipy.org/doc/scipy/
matplotlib  :   https://matplotlib.org/stable/index.html
seaborn     :   https://seaborn.pydata.org/
tkinter     :   https://docs.python.org/3/library/tkinter.html
calendar    :   https://docs.python.org/3/library/calendar.html
datetime    :   https://docs.python.org/3/library/datetime.html
os          :   https://docs.python.org/3/library/os.html

"""
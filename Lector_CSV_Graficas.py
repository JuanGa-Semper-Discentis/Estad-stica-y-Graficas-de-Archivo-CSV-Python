import pandas as pd
import matplotlib.pyplot as plt  
#      ^ libreria principal para graficar  de python
import seaborn as sns
#      ^ libreria de graficas de estadisticas sobre matplotlib, version actualizada, ojo a la version
import tkinter as tk
from tkinter import scrolledtext

#def ruta del csv modificado
#seleccionar archivo
ruta_csv = r"C:\Users\User\Downloads\Archivo_CSV_Original.csv" #ORIGINAL
#ruta_csv = r"C:\Users\User\Downloads\Archivo_CSV_Escenario_X.csv" #ESCENARIO
#         ^ solo recibe un unico CSV
#         ^ Cuidado con la direccion

#lectura de datos
df = pd.read_csv(ruta_csv)
#    ^ carga el archivo CSV en un DataFrame

#
if "Fecha" in df.columns:
    df["Fecha"] = pd.to_datetime(df["Fecha"])
#                 ^ pasar fecha de str a fecha real para matplotlib


#filtracion de columnas numericas
if "Precipitacion" in df.columns:
    data = df["Precipitacion"]
#          ^ selecciona columna con nombre precipitaciones
else:
    data = df.select_dtypes(include="number").iloc[:, 0]
#                                             ^ usa columna con numeros disponible


#definicio y config de graficas

sns.set_style("whitegrid")
#   ^ estilo cisual de graficos de libreria seaborn, fondo blanco

# histograma de frecuencia
plt.figure() # creacion una nueva figura (ventana de grafica) en blanco


sns.histplot(
    data,
    bins=50,
    kde=False
)
#   ^ crear histograma, data : la Serie de pandas con los valores, bins=50 : divide el rango de datos en 50 barras, kde=False : NO dibuja la curva de densidad (solo barras)

#etiquetas de ejes y ventanas
plt.xlabel("Precipitacion (mm)")
plt.ylabel("Frecuencia (dias)")
plt.title("Histograma de Precipitacion Diaria")

# plt.show() => muestra la figura en pantalla y pausa el script hasta cerrarla
plt.show()

#histograma y KDE =>>> mas boniro que el de seipre

plt.figure()

sns.histplot(
    data,
    bins=50,
    kde=True
)
#   ^ crear histograma, data : la Serie de pandas con los valores, bins=50 : divide el rango de datos en 50 barras, kde=False : dibuja la curva de densidad (solo barras)

plt.xlabel("Precipitacion (mm)")
# la densidad en el eje Y cambia de frecuencia a probabilidad cuando kde=True <= datos trecnicos de ejecucion de pandas
plt.ylabel("Densidad")
plt.title("Distribucion de Precipitacion")
plt.show()

#grafico de caja
plt.figure()

sns.boxplot(x=data)

plt.xlabel("Precipitacion (mm)")
plt.title("Grafico de Caja de Precipitacion")
plt.show()
#   ^genera diagrama de caja, x=data : orientacion horizontal (eje X = valores de precipitacion), os puntos fuera de los bigotes son valores atipicos (outliers)


# serie temporal
# error no grafica hasta verificar que fecha no sea str
if "Fecha" in df.columns:
    plt.figure()

    plt.plot(
        df["Fecha"],
        data,
        linewidth=0.5
    )
#       ^ grafica de lineas, eje x con fechas reales, y con valores de precipitacion y configuracion de lineas

    plt.xlabel("Fecha")
    plt.ylabel("Precipitacion (mm)")
    plt.title("Serie Temporal de Precipitacion")
    plt.show()



#resumen del tkinter------------------
texto = """
Graficas generadas:
1 Histograma de frecuencia
2 Histograma con densidad KDE
3 Grafico de caja de precipitacion
4 Serie temporal

Estas graficas permiten analizar:
- distribucion de lluvia, sus fechas
- presencia de eventos extremos
- dispersion de datos historicos
- patron temporal de precipitacion
- entrenar y generar un modelo estocastico
"""
# ^^^^^ se podria imprimir solo en la terminal
#ojo con la actualizacion de seaborn y kde

ventana = tk.Tk()
ventana.title("Visualizacion Estadistica")
area = scrolledtext.ScrolledText(ventana, width=60, height=15)
area.pack(padx=10, pady=10)
area.insert(tk.END, texto)
area.config(state="disabled")
ventana.mainloop()
#       ^deja abierta la ventana

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
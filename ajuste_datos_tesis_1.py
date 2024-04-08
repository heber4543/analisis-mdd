#%%
import glob as gl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

direc = 'D:\SelNet\Tesis\Simulacion\*'

def nombres_archivos(direc):  
    patron = f'{direc}'
    return gl.glob(patron)

nombres_carpetas = nombres_archivos(direc)
print(nombres_carpetas)

fase = 'Adquisición'
red = 'shd'
estimulo = 'Tono'
AoW = 'Acts'

def nombres_archivos2(fase, red, estimulo, AoW):
    l = []
    for i in nombres_carpetas:
        l.extend(gl.glob(f'{i}\\{fase}\\{red}_*\\{estimulo}\\{AoW}\\*'))
    return l

nombres = nombres_archivos2(fase, red, estimulo, AoW)
print(nombres)

datos = [] 
df = pd.DataFrame()

for nombre in nombres:
    if '(mot,cr)' in nombre:
        print(nombre)
        df_tmp = pd.read_table(nombre, header=None, sep='\s+')
        df_tmp.columns = ['data']
        df_tmp['unidad'] = nombre.split('\\')[-1]
        df_tmp['red'] = nombre.split('\\')[6]
        df_tmp['fase'] = fase
        df_tmp['estimulo'] = estimulo
        df_tmp['carpeta']  = nombre.split('\\')[4]
       
        if nombre.split('\\')[4] == 'ch_data' or nombre.split('\\')[4] == 'ch7_data':
            nuevos_nombres_filas = {'6(mot,cr)': 'M\''}
        else:
            nuevos_nombres_filas = {'5(mot,cr)': 'M\''}
        datos.append(df_tmp)
        df_tmp['unidad'] = df_tmp['unidad'].replace(nuevos_nombres_filas)

df = pd.concat(datos)
df = df.reset_index(drop=True)

def analisis_penultimo_t(df, init=1, step=3):
    vec_index = np.arange(init, len(df), step)
    penultimo_t = df.iloc[vec_index]
    return penultimo_t

x2 = df.groupby(['red', 'unidad']).apply(analisis_penultimo_t, init=1)
x2 = x2.reset_index(drop=True)
longitud_columna = len(x2)
secuencia = [str(i % 100 + 1) for i in range(longitud_columna)]
x2['Ensayo'] = np.nan 
x2['Ensayo'] = secuencia
x2['Ensayo'] = x2['Ensayo'].astype(int)  # Convierte la columna 'Ensayo' a tipo numérico
x2 = x2.sort_values(by=['carpeta', 'unidad', 'Ensayo']).reset_index(drop=True)

y = x2.groupby(['carpeta', 'Ensayo', 'unidad']).mean('data').reset_index()
y['Ensayo'] = y['Ensayo'].astype(int)

# Función Sigmoid
def sigmoid(t, k, to):
    return 1 / (1 + np.exp(-k * (t - to)))

# Ajuste de curva utilizando curve_fit
z = np.unique(y['carpeta'])

# for carpeta in z:
#     data_carpeta = y[y['carpeta'] == carpeta]
    
#     # Proporcionar valores iniciales razonables para los parámetros k y to
#     p0 = [1, 50]  # Debes ajustar estos valores según tus datos
    
#     # Ajustar utilizando el método 'dogbox'
#     try:
#         popt, pcov = curve_fit(sigmoid, data_carpeta['Ensayo'], data_carpeta['data'], p0=p0, method='dogbox')
#     except Exception as e:
#         print(f"No se pudo ajustar la curva para {carpeta}. Error: {e}")
#         continue
    
#     plt.figure(figsize=(10, 6), dpi=600)
#     plt.plot(data_carpeta['Ensayo'], sigmoid(data_carpeta['Ensayo'], *popt), label=f'Carpeta: {carpeta}')
#     plt.xlabel('Trials')
#     plt.ylabel('Learning Index')
#     plt.legend()
#     plt.show()

# Crear una figura y ejes fuera del bucle
fig, ax = plt.subplots(figsize=(10, 6), dpi=600)

# Definir colores
lineas = ['blue', 'red', 'green', 'black']

# Iterar sobre las carpetas y colores
for i, carpeta in enumerate(z):
    data_carpeta = y[y['carpeta'] == carpeta]
    
    # Proporcionar valores iniciales razonables para los parámetros k y to
    p0 = [.0001
          , 50]  # Debes ajustar estos valores según tus datos
    
    # Ajustar utilizando el método 'dogbox'
    try:
        popt, pcov = curve_fit(sigmoid, data_carpeta['Ensayo'], data_carpeta['data'], p0=p0, method='dogbox')
    except Exception as e:
        print(f"No se pudo ajustar la curva para {carpeta}. Error: {e}")
        continue
    
    # Agregar cada gráfica a los ejes con colores específicos
    ax.plot(data_carpeta['Ensayo'], sigmoid(data_carpeta['Ensayo'], *popt), label=f'{carpeta}'.split('_')[0], linestyle='-', color=lineas[i])

# Ajustar los ticks del eje y de 0 a 1 con incrementos de 0.2
plt.yticks(np.arange(0, 1.2, 0.2))

# Agregar etiquetas y leyenda
ax.set_xlabel('Ensayos')
ax.set_ylabel('Activación')
#ax.set_title('Curvas de aprendizaje ajustadas')
ax.legend()

# Mostrar la figura
#plt.show()

#guardar la figura
fig.savefig('curvas_ajustadas.png', dpi=600,bbox_inches='tight')





# %%

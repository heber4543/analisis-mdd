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

# # Ajuste de curva utilizando curve_fit
# z = np.unique(y['carpeta'])

# for carpeta in z:
#     data_carpeta = y[y['carpeta'] == carpeta]
    
#     # Proporcionar valores iniciales razonables para los parámetros k y to
#     p0 = [0, 50]  # Debes ajustar estos valores según tus datos
    
#     # Ajustar utilizando el método 'dogbox'
#     try:
#         popt, pcov = curve_fit(sigmoid, data_carpeta['Ensayo'], data_carpeta['data'], p0=p0, method='dogbox')
#     except Exception as e:
#         print(f"No se pudo ajustar la curva para {carpeta}. Error: {e}")
#         continue
    
#     plt.figure(figsize=(10, 6), dpi=600)
#     plt.scatter(data_carpeta['Ensayo'], data_carpeta['data'], color='gray')# label='Datos originales')
#     plt.plot(data_carpeta['Ensayo'], sigmoid(data_carpeta['Ensayo'], *popt), color='black') #label='Curva ajustada')
    
#     # Agregar líneas de conexión entre los puntos del scatter plot
#     plt.plot(data_carpeta['Ensayo'], data_carpeta['data'], color='gray', linestyle='-', linewidth=0.5)
    
#     plt.title(f'{carpeta}'.split('_')[0])
#     plt.xlabel('Ensayos')
#     plt.ylabel('Promedio de activación')
#     plt.ylim(0, 1)
#     plt.yticks(np.arange(0, 1.2, 0.2))
#     plt.legend()
#     # plt.show()
#     plt.savefig(f'{carpeta}.png', dpi=600, bbox_inches='tight')

fig, axs = plt.subplots(2, 2, figsize=(10, 6), dpi=600)  # Ajusta el tamaño según necesites
fig.subplots_adjust(hspace=0.4, wspace=0.4)  # Ajusta el espaciamiento si es necesario

# Iterar sobre las carpetas para generar las gráficas
z = np.unique(y['carpeta'])
axs_flat = axs.flatten()  # Para facilitar el acceso a los ejes como una lista plana

for idx, carpeta in enumerate(z):
    if idx < 4:  # Asegura que solo se dibujen las primeras 4 gráficas
        ax = axs_flat[idx]  # Selecciona el subplot correspondiente
        data_carpeta = y[y['carpeta'] == carpeta]

        # Intenta ajustar la curva
        p0 = [0, 50]  # Valores iniciales
        try:
            popt, pcov = curve_fit(sigmoid, data_carpeta['Ensayo'], data_carpeta['data'], p0=p0, method='dogbox')
        except Exception as e:
            print(f"No se pudo ajustar la curva para {carpeta}. Error: {e}")
            continue

        # Dibuja los datos y la curva ajustada en el subplot
        ax.scatter(data_carpeta['Ensayo'], data_carpeta['data'], color='gray')
        ax.plot(data_carpeta['Ensayo'], sigmoid(data_carpeta['Ensayo'], *popt), color='black')
        
        # Agregar líneas de conexión entre los puntos del scatter plot
        ax.plot(data_carpeta['Ensayo'], data_carpeta['data'], color='red', linestyle='-', linewidth=0.5)

        ax.set_title(f'{carpeta}'.split('_')[0])
        ax.set_xlabel('Ensayos')
        ax.set_ylabel('Promedio de activación')
        ax.set_ylim(0, 1)
        ax.set_yticks(np.arange(0, 1.2
                                , 0.2))
        ax.set_xlim(0, 100)
        ax.legend()

# %%

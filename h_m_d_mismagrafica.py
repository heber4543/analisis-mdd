#%%
import glob as gl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
mt = [1, 2, 3]  # Cambiado a valores numéricos

for nombre in nombres:
    #if '(mot,cr)' in nombre:
    print(nombre)
    df_tmp = pd.read_table(nombre, header=None, sep='\s+')
    df_tmp.columns = ['data']
    df_tmp['unidad'] = nombre.split('\\')[-1]
    df_tmp['red'] = nombre.split('\\')[6]
    df_tmp['fase'] = fase
    df_tmp['estimulo'] = estimulo
    df_tmp['carpeta']  = nombre.split('\\')[4]
    df_tmp['momento_temporal'] = np.tile(mt, df_tmp.shape[0]//3)
   
    datos.append(df_tmp)

df = pd.concat(datos)
df = df.reset_index(drop=True)

df['unidad'] = df['unidad'].replace({'5(mot,cr)': 'M\''})
df['unidad'] = df['unidad'].replace({'6(mot,cr)': 'M\''})
df['unidad'] = df['unidad'].replace({'3(sen,H)': 'H'})
df['unidad'] = df['unidad'].replace({'5(mot,D)': 'D'})
df['unidad'] = df['unidad'].replace({'4(mot,D)': 'D'})

# Filtrar filas donde la columna 'unidad' sea 'M\'' o 'H'
df_filtrado = df[df['unidad'].isin(['M\'','H','D'])].copy()

# Mostrar el DataFrame resultante
print(df_filtrado)

media_por_carpeta = df_filtrado.groupby(['carpeta', 'unidad','momento_temporal'])['data'].mean().reset_index()

print(media_por_carpeta)

# Crear una figura con subgráficas (2 filas, 2 columnas)
fig, axs = plt.subplots(2, 2, figsize=(15, 10), sharex=True)

for i, (carpeta, datos_carpeta) in enumerate(media_por_carpeta.groupby('carpeta')):
    fila_actual = i // 2
    columna_actual = i % 2
    
    for unidad, datos_unidad in datos_carpeta.groupby('unidad'):
        #linestyle = '-' if unidad == "M'" else ':' if unidad == 'H' else '--'
        color = 'red' if unidad == "M'" else 'black' if unidad == 'H' else 'blue' 
        axs[fila_actual, columna_actual].plot(datos_unidad['momento_temporal'], datos_unidad['data'].values, marker='o', label=f'{unidad}', linestyle='-', color=color)

    #axs[fila_actual, columna_actual].set_title(f'Activación promedio para {carpeta}')
    axs[fila_actual, columna_actual].set_xlabel('Momentos Temporales')
    axs[fila_actual, columna_actual].set_ylabel('Promedio de activación')
    axs[fila_actual, columna_actual].set_xticks([1, 2, 3])  # Cambiado a valores numéricos
    #axs[fila_actual, columna_actual].set_xlim(0, 4)  # Establecer límites del eje x
    axs[fila_actual, columna_actual].set_ylim(0, 1.1)  # Establecer límites del eje y
    axs[fila_actual, columna_actual].legend()

# Ajustar el diseño de la figura
plt.tight_layout()
plt.savefig('figure_subplots_2x2.png', dpi=600, bbox_inches='tight')
plt.show()

# %%

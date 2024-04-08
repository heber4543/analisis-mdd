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
mt= ['t1', 't2', 't3']

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
        df_tmp['momento_temporal'] = np.tile(mt,df_tmp.shape[0]//3)
       
        # if nombre.split('\\')[4] == 'ch_data' or nombre.split('\\')[4] == 'ch7_data':
        #     nuevos_nombres_filas = {'6(mot,cr)': 'M\''}
        # else:
        #     nuevos_nombres_filas = {'5(mot,cr)': 'M\''}
        datos.append(df_tmp)
        # df_tmp['unidad'] = df_tmp['unidad'].replace(nuevos_nombres_filas)

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

for carpeta, datos_carpeta in media_por_carpeta.groupby('carpeta'):
    plt.figure(figsize=(10, 6))
    for unidad, datos_unidad in datos_carpeta.groupby('unidad'):
        #linestyle = '-' if unidad == "M'" else ':' if unidad == 'H' else '--'
        color= 'red' if unidad == "M'" else 'black' if unidad == 'H' else 'blue'
        plt.plot(datos_unidad['momento_temporal'], datos_unidad['data'].values, marker='o', label=unidad, linestyle='-', color=color)
    
    plt.title(f'{carpeta}')
    plt.xlabel('Momentos Temporales')
    plt.ylabel('Promedio de activación')
    plt.xticks(['t1', 't2', 't3'])
    
    # Ajustar los ticks del eje y de 0 a 1 con incrementos de 0.2
    plt.yticks(np.arange(0, 1.2, 0.2))
    
    plt.legend()
    #plt.show()
    plt.savefig(f'{carpeta}.png', dpi=600, bbox_inches='tight')




    


# %%

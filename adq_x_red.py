#%%
import glob as gl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


direc='D:\SelNet\Tesis\Simulacion\*'

def nombres_archivos(direc):  
    patron= f'{direc}'
    return gl.glob(patron)

nombres_carpetas=nombres_archivos(direc)
print(nombres_carpetas)

fase='Adquisición'
red='shd'
estimulo='Tono'
AoW='Acts'

def nombres_archivos2(fase, red, estimulo, AoW):
    l=[]
    for i in nombres_carpetas:
        l.extend(gl.glob(f'{i}\\{fase}\\{red}_*\\{estimulo}\\{AoW}\\*'))
    return l
nombres=nombres_archivos2(fase, red, estimulo, AoW)
print(nombres)

datos= [] 
df=pd.DataFrame()

for nombre in nombres:
    if '(mot,cr)' in nombre:
        print(nombre)
        df_tmp = pd.read_table(nombre, header = None, sep = '\s+')
        df_tmp.columns = ['data']
        df_tmp['unidad'] =nombre.split('\\')[-1]
        df_tmp['red'] = nombre.split('\\')[6]
        df_tmp['fase'] = fase
        df_tmp['estimulo'] = estimulo
        df_tmp['carpeta']  = nombre.split('\\')[4]
       
        if nombre.split('\\')[4]=='ch_data' or nombre.split('\\')[4]=='ch7_data':
            nuevos_nombres_filas={
            '6(mot,cr)':'M\''}
        else :
            nuevos_nombres_filas={
        '5(mot,cr)':'M\''}
        datos.append(df_tmp)
        df_tmp['unidad'] = df_tmp['unidad'].replace(nuevos_nombres_filas)

df = pd.concat(datos)
df=df.reset_index(drop=True)
def analisis_penultimo_t(df, init=1, step=3):
    vec_index = np.arange(init, len(df), step)
    penultimo_t = df.iloc[vec_index]
    return penultimo_t

x2=df.groupby(['red','unidad']).apply(analisis_penultimo_t, init=1)
x2.reset_index(drop=True, inplace=True)
longitud_columna=len(x2)
secuencia =[str(i % 100 + 1) for i in range(longitud_columna)]

x2['Ensayo'] = x2.groupby(['carpeta', 'unidad']).cumcount() % 100 + 1
        
for red in x2['red'].unique():
    for experimento in x2[x2['red'] == red][['carpeta', 'unidad']].drop_duplicates().itertuples(index=False):
        plt.figure(figsize=(10, 6))
        
        # Filtrar datos para el experimento actual y la red actual
        datos_experimento = x2[(x2['carpeta'] == experimento.carpeta) & (x2['unidad'] == experimento.unidad) & (x2['red'] == red)]
        
        for unidad, datos_unidad in datos_experimento.groupby('unidad'):
            print(f'Red: {red}, Experimento: {experimento.carpeta}, Unidad: {unidad}')
            print(datos_unidad)
            
            # Graficar los datos sin cálculo de media
            plt.plot(datos_unidad['Ensayo'], datos_unidad['data'], marker='o', color= 'black')
        
        plt.title(f'{red}, {experimento.carpeta}'.split(',')[0].split('-')[1]+','+f'{red}, {experimento.carpeta}'.split(',')[1].split('_')[0])
        plt.xlabel('Ensayos')
        plt.ylabel('Activación')
        
        #plt.legend()
        #plt.show()
        plt.savefig(f'{red}_{experimento.carpeta}.png', dpi=600, bbox_inches='tight')



    









# %%

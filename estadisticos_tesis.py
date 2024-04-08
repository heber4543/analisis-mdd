#Análisis estadístico tesis
#%%
import numpy as np
import pandas as pd
import glob as gl
import scipy.stats as stats
from scikit_posthocs import posthoc_dunn

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
        
x2['Ensayo']=np.nan 
x2['Ensayo'] = secuencia
x2['Ensayo'] = x2['Ensayo'].astype(int)  # Convierte la columna 'Ensayo' a tipo numérico
x2 = x2.sort_values(by=['carpeta', 'unidad', 'Ensayo']).reset_index(drop=True)

y=x2.groupby(['carpeta','Ensayo','unidad']).mean('data').reset_index()
y['Ensayo'] = y['Ensayo'].astype(int)
print (y)

# Crear grupos
grupo_ch = []
grupo_ch7 = []
grupo_sh = []
grupo_sh7 = []

for i in y['carpeta'].unique():
    datos_grupo = y[y['carpeta'] == i]['data'].tolist()  # Filtrar datos para cada grupo
    if i == 'ch_data':
        grupo_ch.append(datos_grupo)
    elif i == 'ch7_data':
        grupo_ch7.append(datos_grupo)
    elif i == 'sh_data':
        grupo_sh.append(datos_grupo)
    elif i == 'sh7_data':
        grupo_sh7.append(datos_grupo)

# Verificar que cada lista tenga 100 datos
#print(len(grupo_ch[0]))  # Debería imprimir 100
#print(len(grupo_ch7[0]))  # Debería imprimir 100
#print(len(grupo_sh[0]))  # Debería imprimir 100
#print(len(grupo_sh7[0]))  # Debería imprimir 100

# Realizar la prueba de Kruskal-Wallis
estadistica_kruskal, valor_p = stats.kruskal(grupo_ch[0], grupo_ch7[0], grupo_sh[0], grupo_sh7[0])

# Imprimir resultados
print("Estadística de prueba de Kruskal-Wallis:", estadistica_kruskal)
print("Valor p:", valor_p)

# Interpretar los resultados
nivel_significancia = 0.05

if valor_p < nivel_significancia:
    print("Hay evidencia para rechazar la hipótesis nula.")
    print("Existen diferencias significativas entre al menos dos grupos.")

    # Crear un DataFrame ordenado por grupos
    grupos_ordenados = ['ch_data', 'ch7_data', 'sh_data', 'sh7_data']
    df_ordenado = y[y['carpeta'].isin(grupos_ordenados)]

    # Realizar la prueba post hoc de Dunn
    dunn_result = posthoc_dunn(df_ordenado, val_col='data', group_col='carpeta', p_adjust='bonferroni')

    # Imprimir la matriz de resultados de la prueba de Dunn
    print("\nMatriz de comparaciones de Dunn:")
    print(dunn_result)

else:
    print("No hay evidencia para rechazar la hipótesis nula.")
    print("No hay diferencias significativas entre los grupos.")

# %%

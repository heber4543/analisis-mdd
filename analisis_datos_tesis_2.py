#%%
import glob as gl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#aqui se definen los parametros de la busqueda de archivos
#carpeta es la carpeta donde se encuentran los archivos
#fase es la fase de entrenamiento que se quiere analizar
#red es el nombre general que arroja selnet de la red, antes del guion y el número de la red
#estimulo es el nombre del estimulo que se quiere analizar
#el parametro estimulo es S', en selnet le puedes poner nombre (p.ej. verde, LL, SS, tono, rojo, etc)
carpeta='sh7_data'
fase='Prueba'
red='shd_sh'
estimulo='Tono'

#se define la funcion y sus parametros
#el parametro AoW es si quieres revisar pesos o revisar activaciones
#para activaciones= 'Acts'. Para pesos= 'Wgts'

def nombres_archivos(carpeta,fase, red, estimulo, AoW='Acts'):  
    if AoW =='Acts':
        patron= f'{carpeta}\{fase}\{red}-*\{estimulo}\{AoW}\*'
    else:
        patron= f'{carpeta}\{fase}\{red}-*\{estimulo}\{AoW}\*\**'
    
    return gl.glob(patron)

nombres=nombres_archivos(carpeta,fase,red,estimulo)
print(nombres)

#asignación de los nombres del archivo en un data frame
datos= [] 
for nombre in nombres:
    df=pd.read_table(nombre, header = None, sep = '\s+')
    df.columns = ['data']
    df['unidad'] = nombre.split('\\')[-1]
    df['red'] = nombre.split('\\')[2]
    df['fase'] = fase
    df['estimulo'] = estimulo 
    df['carpeta']  = carpeta
    datos.append(df)   
datos = pd.concat(datos)
print(datos)

#función para analizar 1 dato cada 3 datos
def analisis_penultimo_t(df, init=1, step=3):
    vec_index = np.arange(init, len(df), step)
    penultimo_t = df.iloc[vec_index]
    return penultimo_t 
#agrupar por red y unidad y aplicar la función analisis_penultimo_t
#por red y por unidad recogera 1 dato cada 3
x2=datos.groupby(['red','unidad']).apply(analisis_penultimo_t, init=1)
# remover index para usarlo como columna
x2.reset_index(drop=True, inplace=True)
print(x2)

#Funcion para calcular el promedio de cada unidad
def mean_unit_net(df):
    return df['data'].mean()
    data_mean = x2.groupby(['red','unidad']).apply(mean_unit_net)
# convert red and unit to columns
    data_mean = data_mean.reset_index()
# renamme columns
    data_mean.columns = ['red', 'unidad', 'mean']
x2.groupby('unidad').describe()
#analizar la desviación estandar de cada unidad y el promedio que se asignan al df 'y'
y=x2.groupby('unidad').describe()
y.reset_index(inplace=True)

if carpeta=='ch_data' or carpeta=='ch7_data':
    nuevos_nombres_filas={
    '2(sen,e)':'S\'\'',
    '3(sen,H)':'H',
    '4(mot,e)':'M\'\'',
    '5(mot,D)':'D',
    '6(mot,cr)':'M\''
    }
else :
    nuevos_nombres_filas={
    '2(sen,e)':'S\'\'',
    '3(mot,e)':'M\'\'',
    '4(mot,D)':'D',
    '5(mot,cr)':'M\''
    }

y['unidad'] = y['unidad'].replace(nuevos_nombres_filas)
#ciclo for para eliminar los subniveles de los encabezados. 
#Recordatorio: data y unidad estaban como encabezado pero mean y std estaban como subencabezado
#con este ciclo for se eliminan los subencabezados y se juntan con su encabezado
y.columns=[f"{level1}_{level2}" for level1, level2 in y.columns]
y['error_estandard']=y['data_std']/np.sqrt(y['data_count'])
print(y)

#plotear los datos
fonta= {'family': 'serif',  # Fuente Times New Roman
        'weight': 'bold',    # Negritas
        'style': 'italic',   # Cursiva
        'size': 12}          # Tamaño de fuente

fontb= {'family': 'serif',  # Fuente Times New Roman
        'weight': 'bold',    # Negritas
        'size': 12}          # Tamaño de fuente

y.plot(kind='bar', x='unidad_',y=('data_mean'), yerr=('error_estandard'), 
       color='white', edgecolor='black', legend=False, capsize=5)

plt.xlabel('')
plt.xticks(rotation=360, fontproperties=fonta)
plt.ylabel('Activación promedio $\pm$ SE', fontdict=fontb)
plt.ylim(0,1)
plt.tight_layout()
#en esta linea se guarda la figura en la carpeta donde se encuentran los datos, escoge el nombre que le darás
plt.savefig('Activación_promedio_sh7.png', dpi=600)

#%%

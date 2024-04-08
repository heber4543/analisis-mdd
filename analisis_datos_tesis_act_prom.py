#%%
import glob as gl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#se defines variables fuera de la función para que los lea
#carpeta es el nombre de la carpeta que crea selnet
#fase es el cómo nombraste a las condiciones dentro de la simulacion en selnet
#red es el nombre que tienen las redes antes del guion con numero
#ejemplo en red: comunmente arroja red-1, red-2, red-3- Solo poner lo que va
#antes del guion, en este ejemplo 'red'
direc='D:\SelNet\Tesis\Simulacion'
carpeta='ch_data'
fase='Prueba'
red='shd_ch'
estimulo='Tono'

#se define la funcion y sus parametros
#el parametro estimulo es S', en selnet le puedes poner nombre (p.ej. verde, LL, SS, tono, rojo, etc)
#el parametro AoW es si quieres revisar pesos o revisar activaciones
#para activaciones= 'Acts'. Para pesos= 'Wgts'

def nombres_archivos(direc,carpeta,fase, red, estimulo, AoW='Acts'):  
    if AoW =='Acts':
        patron= f'{direc}\{carpeta}\{fase}\{red}-*\{estimulo}\{AoW}\*'
    else:
        patron= f'{direc}\{carpeta}\{fase}\{red}-*\{estimulo}\{AoW}\*\**'
    
    return gl.glob(patron)

nombres=nombres_archivos(direc,carpeta,fase,red,estimulo)
print(nombres)

#asignación de los nombres del archivo en un data frame
datos= [] 
df=pd.DataFrame()
for nombre in nombres:
    df=pd.read_table(nombre, header = None, sep = '\s+')
    df.columns = ['data']
    df['unidad'] =nombre.split('\\')[-1]
    df['red'] = nombre.split('\\')[6]
    df['fase'] = fase
    df['estimulo'] = estimulo 
    df['carpeta']  = carpeta
    datos.append(df)   
datos = pd.concat(datos)



def analisis_penultimo_t(df, init=1, step=3):
    vec_index = np.arange(init, len(df), step)
    penultimo_t = df.iloc[vec_index]
    return penultimo_t
x2=datos.groupby(['red','unidad']).apply(analisis_penultimo_t, init=1)
# remove index
x2.reset_index(drop=True, inplace=True)
print(x2)

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

longitud_columna=len(x2)
secuencia =[str(i % 100 + 1) for i in range(longitud_columna)]
        
x2['unidad'] = x2['unidad'].replace(nuevos_nombres_filas)
x2['Ensayo']=np.nan 
x2['Ensayo']= secuencia
print(x2)

def mean_unit_net(df):
    return df['data'].mean()

data_mean = x2.groupby(['red','unidad']).apply(mean_unit_net)

# convert red and unit to columns
data_mean = data_mean.reset_index()
# renamme columns
data_mean.columns = ['red', 'unidad', 'mean']
x2.groupby('unidad').describe()
y=x2.groupby('unidad').describe()
    
y.reset_index(inplace=True)
y.columns=[f"{level1}_{level2}" for level1, level2 in y.columns]

error=[]
for i in y['data_std']:
    error.append(i/(75**.5))
y['error_std']=error
    
    


y.plot(kind='bar', x='unidad_',y=('data_mean'), yerr=('error_std'), 
       color='white', edgecolor='black', legend=False, capsize=5)

fonta= {'family': 'serif',  # Fuente Times New Roman
        'weight': 'bold',    # Negritas
        'style': 'italic',   # Cursiva
        'size': 12}          # Tamaño de fuente

fontb= {'family': 'serif',  # Fuente Times New Roman
        'weight': 'bold',    # Negritas
        'size': 12}          # Tamaño de fuente

plt.title(carpeta, fontdict=fontb, pad=20)
plt.xlabel('')
plt.xticks(rotation=0,font=fonta)
plt.ylabel('Activación promedio por unidad',font=fontb)
plt.tight_layout()
plt.savefig('peso_promedio_'+carpeta, dpi=600)


# %%

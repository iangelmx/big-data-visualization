#In[1]:
import pandas as pd


#In[2]:
archivo = pd.read_excel( 'Religion_03.xlsx' )
archivo = archivo.set_index(['ESTADO', 'SEXO'])
nuevo = archivo.stack()

#In[3]:
type(nuevo)

nuevo.to_csv( nuevo, 'salida.csv' )


# %%

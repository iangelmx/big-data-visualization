"""
Script to get some analytics from a FB page and save it to MongoDB

This script was developed according the Visualization Big data's course in FCS.
This script helps people of marketing to get more information about the
activity in their social media page in Facebook in a free way.
To make it run you need to make an app in FB for developers, then get a TOKEN with
the permissions of page read/manage posts.

Created by: Ángel Negib Ramírez Álvarez
        Github:     iangelmx
        Email:      angel@ninjacom.space

Version: Alpha

First release: 2020-06-23
Last modification: 2020-06-24
"""



#In[1]
import facebook
import requests
import json
import pandas as pd
import datetime
from libs.mongo_lib import Bd

#In[2]:

def get_reaction_from_post( row : pd.core.series.Series ) -> pd.core.series.Series:
    
    post_id = row['id']
    reactions = graph.get_connections(post_id, 'reactions', fields='pic,name,pic_large,profile_type,pic_crop,can_post,type,link,id')
    #Para irnos moviendo entre las páginas
    paging = reactions.get('paging')
    reactions = reactions['data']

    for react in reactions:
        row[ react['type'].lower() ] +=1
        row[ 'users_likes' ].append( react['name'] )
    return row
    
    
#In[3]

settings = json.loads(open("settings.json").read())
CANT_COMMENTS = 10
ACCESS_TOKEN = settings.get('access_token')
PAGE_ID = settings.get('id_fb_page')

graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="3.1")

cuenta_likes = 0
lista_comments = []
flag = False


#In[4]

comments = graph.get_connections(PAGE_ID, 'feed')
paging = comments['paging']
comments = comments['data']
comments


#In[5]:

# Esto lo hice, porque al ejecutar likes_post = { ... } me daba{
# un error, de que había posts sin 'messages', se trata de publicaciones
# sin un cuerpo de texto. Sólo notificaciones o algo como eso ~}
with_no_message = filter( lambda x: 'message' not in x, comments )
with_no_message = tuple(with_no_message)

#In[6]:

#Convertimos esto a un bonito diccionario para poderle meter mano con pandas
likes_post = [
    {
        'id' : item['id'],
        'post':item['message'] if 'message' in item else item['story'], 
        'users_likes':[], 
        'like':0, 
        'love':0, 
        'haha':0, 
        'angy':0, 
        'care':0, 
        'wow':0, 
        'sad':0,
        'created_time':datetime.datetime.strptime( item['created_time'], "%Y-%m-%dT%H:%M:%S+0000" )
    }
    for item in comments 
]
likes_post

posts = pd.DataFrame.from_dict(likes_post)
posts

#In[7]:
posts_with_reactions = posts.apply( get_reaction_from_post, axis='columns' )
posts_with_reactions

#In[8]:
## Change CSV/XLSX to MongoDB
#posts_with_reactions.to_csv( 'salida_reactions.csv' )
#posts_with_reactions.to_excel( 'salida_reactions.xlsx' )

# Ahorita lo hice de forma imperativa :c
# Estoy un poco traumatizado con eso desde #Resuelve, jaja...

# Cuando pueda, lo cambiaré a funcional...
to_mongo = posts_with_reactions.to_dict()
to_mongo

#In[9]:
bd = Bd('localhost', 'aramirez', 'iangelmx', 'test')
#bd.insert_in_db('example', to_mongo)

#In[10]:

print(to_mongo.keys())

big_collection = []
big_collection

#In[11]:


for key in to_mongo:
    if key == 'id':
        for sub_key in to_mongo[key]:
            document = { 
                key : to_mongo[key][sub_key]
            }
            big_collection.append( document )
    else:
        for sub_key in to_mongo[key]:
            big_collection[ sub_key ][ key ] = to_mongo[key][sub_key]


big_collection

# Cuando terminé de hacerlo así, se me ocurrió cómo
# hacerlo un poco más funcional con pandas...
# No cabe duda de que aprendí a programar de forma imperativa.

#In[12]:

bd.insert_in_db('facebook_insights', big_collection )

# %%

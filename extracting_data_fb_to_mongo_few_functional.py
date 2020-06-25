"""
Script to get some analytics from a FB page and save it to MongoDB

This script was developed according the Visualization Big data's course in FCS.
This script helps people of marketing to get more information about the
activity in their social media page in Facebook in a free way.
To make it run you need to make an app in FB for developers, then get a TOKEN with
the permissions of page read/manage posts.

This was done from a imperative form to a more functional way

Created by: Ángel Negib Ramírez Álvarez
        Github:     iangelmx
        Email:      angel@ninjacom.space

Version: Beta

First release: 2020-06-23
Last modification: 2020-06-25
"""



#In[1]
import facebook
import requests
import json
import pandas as pd
import datetime
from libs.mongo_lib import Bd
from libs.fb_functions import *

#In[3]

settings = json.loads(open("settings.json").read())
#CANT_COMMENTS = 10
ACCESS_TOKEN = settings.get('access_token')
PAGE_ID = settings.get('id_fb_page')

graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="3.1")

#In[4]

comments = graph.get_connections(PAGE_ID, 'feed')
paging = comments['paging']
comments = comments['data']
comments


#In[5]: No es necesario ejecutar.

# Esto lo hice, porque al ejecutar likes_post = { ... } me daba
# un error, de que había posts sin 'messages', se trata de publicaciones
# sin un cuerpo de texto. Sólo notificaciones o algo como eso ~
# No es necesario para la ejecución... 
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
        'angry':0, 
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

#In[9]:
bd = Bd('localhost', 'aramirez', 'iangelmx', 'test')


#In[13]: Forma alternativa al procesamiento imperativo
#Esto es mucho más funcional que imperativo, aunque aún tengo mis dudas.

posts_with_reactions['documents'] = posts_with_reactions.apply( lambda row: row.to_dict() , axis='columns' )

#In[14]: Obtenemos los documentos y los guardamos en forma de lista
to_mongo_2 = posts_with_reactions['documents'].to_list()

#Instanciamos Mongo
bd = Bd('localhost', 'aramirez', 'iangelmx', 'test')
# Enviamos a guardar en la collection 'facebook_insights_2' nuestra colección de documentos.
bd.insert_in_db('facebook_insights_2', to_mongo_2 )



# %%

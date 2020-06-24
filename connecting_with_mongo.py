#In[1]:

import pymongo
from pymongo import MongoClient

#In[2]:
client = MongoClient()
db = client.test

#In[3]:
#Inserción:
db.users.insert_one({ 'name' : 'Cristal P' })

#In[4]:

users_to_create = [ {'name':'Holly'}, {'name':'Pete'} ]

db.users.insert_many( users_to_create )

#In[5]:
result = db.users.insert_one(
    {
        'name' : 'Vella',
        'address' : {
            'street' : '2 Avenue',
            'zip_code' : 44550,
            'building' : 1480
        },
        'phones' : [ 5523749038, 5542359985 ]
    }
)


#In[6]: Ver y consultar:

print('Consulta:')
cursor = db.users.find()

[ print(documento) for documento in cursor ]

#In[7]: Modificación
to_modify = { 'name':'Cristal P' }
new_doc = {'name' : 'Cris P'}
db.users.update_one( to_modify, {'$set':new_doc} )

print("Actualizado:")
cursor = db.users.find()

[ print(documento) for documento in cursor ]


# %%


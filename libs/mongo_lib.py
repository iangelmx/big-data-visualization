#In[1]:
import pymongo
from pymongo import MongoClient
from typing import Union
import urllib.parse
import typing
import bson

#In[2]:
class Bd(  ):
	__hostname = ''
	__user = ''
	__pass = ''
	__port = ''
	__database = ''
	__db_object = None
	def __init__(self, hostname:str, user:str, passw:str, database:str, method:Union[str,None] = None, port:Union[int,None] = None):
		self.__hostname = hostname
		self.__user = user
		self.__pass = passw
		self.__database = database
		self.__port = port if port else 27017

		#uri = "mongodb://%s:%s@%s" % (self.__user, self.__pass,self.__hostname)
		#client = MongoClient(uri)

		self.__client = MongoClient(
			self.__hostname,
			username = self.__user,
			password = self.__pass,
			authSource = self.__database ,
			authMechanism = method if method else 'SCRAM-SHA-256'
		)
		self.__db_object = self.__client[ self.__database ]

	def insert_in_db(self, collection:str,object_to_insert:Union[list, dict]) -> bson.objectid.ObjectId:
		if isinstance(object_to_insert, list) :
			self.__db_object[ collection ].insert_many( object_to_insert )
		elif isinstance(object_to_insert, dict):
			return self.__db_object[ collection ].insert_one( object_to_insert ).inserted_id
	
	def get_docs(self, collection:str) -> tuple:
		return tuple(self.__db_object[ collection ].find())

	def change_database(self, database : str):
		self.__db_object = self.__client[ self.__database ]
	
	def find_where( self, collection:str, where:dict) -> tuple:
		return tuple(self.__db_object[ collection ].find( where ))
		
		

#In[3]:

bd = Bd( '127.0.0.1', 'aramirez', 'iangelmx', 'test' )

#In[4]:

a = bd.insert_in_db( 'users', {'name':'Angel Rmz', 'age':23} )
type(a)

#In[5]:

cursor = bd.get_docs( 'users' )
print(cursor)
# %%
[print(document) for document in cursor]

# %%
c = bd.find_where( 'users', {'age':23} )
print(c)

# %%

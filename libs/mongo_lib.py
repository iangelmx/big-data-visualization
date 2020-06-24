"""
Library to support pymongodb's use

This was developed to improve and save time in futures developments
that requires the MongoDB database.
Also, this was created to homogenize the work way in a dev team

Developed by: Ángel Negib Ramírez Álvarez

Version: 1.0

First release: 2020-06-23
Last modification: 2020-06-23

Some help for all the people that know how to work with SQL, but
no with MongoDB

https://docs.mongodb.com/manual/reference/sql-comparison/
"""



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
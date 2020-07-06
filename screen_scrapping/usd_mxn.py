"""
Script to get the actual value of exchange USD to MXN

This script was developed according the Visualization Big data's course in FCS.
I hope this script helps people to know a little of web scrapping, although
this example is not as powerful as other techniques.
I used to work with Selenium...
Whatever, this script should be executed by a cron job or scheduled task, 'cause
if you use a while True loop, surely in a moment It will stop even if
it doesn't appear.

Created by: Ángel Negib Ramírez Álvarez
		Github:     iangelmx
		Email:      angel@ninjacom.space

Version: 1.0

First release: 2020-06-29
Last modification: 2020-07-06
"""
#In[1]:
import requests
import json
import re

from typing import Union
from bs4 import BeautifulSoup

PATH_FILE_TO_UPDATE = './exchange_rate_usd_to_mxn.json'

#In[2]:
def get_last_exchange_rate() -> Union[float, None]:
	file = json.loads( open( PATH_FILE_TO_UPDATE ).read() )
	return file.get('exchange_usd_to_mxn')

def get_current_value() -> Union[float, None]:
	try:
		# We have to put these headers on the requests 'cause Bloomberg was detecting that
		# the program was a bot. And was blocking my requests.
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
			'From': 'contacto@ninjacom.space'  # This is another valid field
		}
		r = requests.get('https://www.bloomberg.com/quote/USDMXN:CUR', headers=headers)
		if r.status_code == 200:
			soup = BeautifulSoup( r.text )
			span_value = soup.find('span', attrs={'class':'priceText__1853e8a5'})
			#print(span.string)
			new_value = float( span_value.string )
			return new_value
		
	except Exception as ex:
		print("Exception getting value of webpage:", ex)

def write_result( new_exchange_rate : float ):
	new = {
		'exchange_usd_to_mxn' : new_exchange_rate
	}
	file = open( PATH_FILE_TO_UPDATE, "w" )
	file.write( json.dumps(new) )
	file.close()

def check_if_write( current_exch_rate:float, new_usd_to_mxn_rate:float ):
	if new_usd_to_mxn_rate > current_exch_rate:
		write_result( new_usd_to_mxn_rate )

#In[3]:

def main():
	current_exch_rate = get_last_exchange_rate()
	new_usd_to_mxn_rate = get_current_value( )
	check_if_write( current_exch_rate, new_usd_to_mxn_rate )	


if __name__ == "__main__":
	main()

# %%


# %%

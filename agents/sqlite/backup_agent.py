import requests
from settings import *

try:
	# send request to 
	TRIGGERAPI = SERVER_URL + '/backup_erp_sqlitedb/'
	response = requests.post(TRIGGERAPI, data={})
except:
	print("Exception")

response = requests.post(ROUTINEAPI, 
							 data={
				             'hash_code': HASH_CODE, 
				             'name': NAME,
				             'location': LOCATION,
				             'description': DESCRIPTION,
				             })
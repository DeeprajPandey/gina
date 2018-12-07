#!/usr/bin/env python

"""Musings with the Google Cloud Natural Language API syntax analysis"""

import json, sys
from google.oauth2 import service_account
import googleapiclient.discovery

text = ''#figured out a way to take a multi-word input from the command line and pass it to the python script
t_index=0 #to keep track of the index of the program name so that it isn't taken into account as a string
for x in sys.argv: #taking the text from the command line and storing into a variable
    if(t_index != 0): #this is required to skip the name of the program "pos.py" from the command line
        text = text + x + ' '
    t_index=1

body = {
	'document': {
		'type': 'PLAIN_TEXT',
		'content': text,
	},
	'encoding_type': 'UTF32'
}

credentials = service_account.Credentials.from_service_account_file('JSON/file.json')
service = googleapiclient.discovery.build('language', 'v1', credentials=credentials)

request = service.documents().analyzeSyntax(body=body)
response = request.execute()

with open('JSON/partsOfSpeech.json', 'w') as fp:
	json.dump(response, fp, indent=2)

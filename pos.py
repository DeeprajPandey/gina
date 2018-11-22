#!/usr/bin/env python

"""Musings with the Google Cloud Natural Language API syntax analysis"""

import json
import googleapiclient.discovery
from interface import usrInput

text = usrInput

body = {
	'document': {
		'type': 'PLAIN_TEXT',
		'content': text,
	},
	'encoding_type': 'UTF32'
}

service = googleapiclient.discovery.build('language', 'v1')

request = service.documents().analyzeSyntax(body=body)
response = request.execute()

with open('JSON/partsOfSpeech.json', 'w') as fp:
	json.dump(response, fp, indent=2)

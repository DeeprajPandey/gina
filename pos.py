#!/usr/bin/env python

"""Musings with the Google Cloud Natural Language API syntax analysis"""

import json
import googleapiclient.discovery

text = 'The quick brown fox jumps over the lazy dog. The octopus was running a marathon with his friend, Ms. Cat. Interestingly, Mr. Octopus won the race.'

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
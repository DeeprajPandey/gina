#!/usr/bin/env python

"""Musings with the Google Cloud Natural Language API syntax analysis"""

import json
import googleapiclient.discovery

text = 'The quick brown fox jumps over the lazy dog.'

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

print(json.dumps(response, indent=2))
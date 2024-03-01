import json
import logging
import requests


class ElasticsearchHandler(logging.Handler):
    def __init__(self, url):
        logging.Handler.__init__(self)
        self.url = url

    def emit(self, data):
        try:
            headers = {'Content-Type': 'application/json'}
            requests.post(self.url, headers=headers, data=json.dumps(data))
        except:
            print("No logger setting")

import requests
import json

class OSSAPIClient():

    def get_facility_status(self, url):
        try:
            response = requests.get(url).json()
        except json.decoder.JSONDecodeError:
            response = None
        return response

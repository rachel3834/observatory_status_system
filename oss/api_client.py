import requests
import json
from django.conf import settings

class OSSAPIClient():

    def get_facility_status(self, url):

        # First check if the system is running:
        try:
            response = requests.get(settings.DEPLOYED_URL)
            print('API CLIENT: ',response)
            if request.status_code == 200:
                try:
                    response = requests.get(url).json()
                except json.decoder.JSONDecodeError:
                    response = None
        except requests.exceptions.ConnectionError:
            response = None

        return response

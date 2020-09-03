import requests

class OSSAPIClient():

    def get_facility_status():
        url = url_tools.concat_urls(config['OSS_URL'],config['facility_status_endpoint'], trailing_slash=True)
        response = requests.get(url).json()
        return response

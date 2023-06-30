import requests

def get_http_status_code(url : str):
    r = requests.get(url)
    return r.status_code

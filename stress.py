import requests

params = {
    'range_start': 1,
    'range_end': 2
}

r = requests.get('http://35.196.226.41:8000/list', params=params)

print(r._content)

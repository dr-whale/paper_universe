from flask import Flask
from src.yandex import Client

app = Flask(__name__)
base_url = 'https://api.weather.yandex.ru/v2'
data_url = '/forecast'
params = {'lat': '59.9386', 'lon': '30.3141', 'hours': 'false', 'extra': 'false', 'limit': 1}
key = '9da62402-b240-4ad0-9f68-7e9d8a5c4028'

@app.route('/')
def index():
    inx_client = Client()
    return inx_client.client_print()

@app.route('/hello')
def hello_world():
    hello_client = Client(base_url, key)
    return hello_client.weather_req(data_url, params)

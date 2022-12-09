from flask import Flask
from flask import json
from src.yandex import Client
from src.yandex import ClientError
from src.yandex import InvalidMethodError
from src.yandex import BadConfigError
from src.yandex import InvalidArgumentError

def test_decorator(func):
    def test_wrapper():
        code = 500
        message = 'Error'
        try:
            return func()
        except InvalidArgumentError as exp:
            code = 404
            message = str(exp)
        except BadConfigError as exp:
            code = 403
            message = str(exp)
        except InvalidMethodError as exp:
            code = 412
            message = str(exp)
        except ClientError as exp:
            code = 400
            message = str(exp)
        except Exception as exp:
            code = 500
            message = str(exp)
        return json.jsonify({"status": "error", "message": message, "code": code})
    test_wrapper.__name__ = func.__name__
    return test_wrapper

weather_client = None

def client_create():
    global weather_client
    if not weather_client:
        weather_client = Client(base_url, key)
    return weather_client

app = Flask(__name__)
base_url = 'https://api.weather.yandex.ru/v2'
data_url = '/forecast'
params = {'lat': '59.9386', 'lon': '30.3141', 'hours': 'false', 'extra': 'false', 'limit': 1}
key = '9da62402-b240-4ad0-9f68-7e9d8a5c4028'

@app.route('/condition')
@test_decorator
def condition():
    return json.jsonify(dict(status = 'ok', condition = client_create().weather_req(data_url, params)['fact']['condition']))

@app.route('/temperature')
@test_decorator
def temperature():
    return json.jsonify(dict(status = 'ok', temperature = client_create().weather_req(data_url, params)['fact']['temp']))

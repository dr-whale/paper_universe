from flask import Flask, json
from src.yandex import Client, ClientError, InvalidMethodError, BadConfigError, InvalidArgumentError
from config import yandex

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
        weather_client = Client(yandex.BASE_URL, yandex.API_KEY)
    return weather_client

app = Flask(__name__)

@app.route('/condition')
@test_decorator
def condition():
    return json.jsonify(dict(status = 'ok', condition = client_create().weather_req(yandex.DATA_URL, yandex.PARAMS)['fact']['condition']))

@app.route('/temperature')
@test_decorator
def temperature():
    return json.jsonify(dict(status = 'ok', temperature = client_create().weather_req(yandex.DATA_URL, yandex.PARAMS)['fact']['temp']))

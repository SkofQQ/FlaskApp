#from os import environ
from discogr import app

if __name__ == '__main__':
    # HOST = environ.get('SERVER_HOST', 'localhost')
    # try:
    #     PORT = int(environ.get('SERVER_PORT', '5555'))
    # except ValueError:
    #     PORT = 5555
    # app.run(HOST, PORT)

    app.run(host='127.0.0.1')


from flask import Flask

SECRET_PATH = './secret_key'

app = Flask('name')
app.secret_key = open(SECRET_PATH, 'rb').read()

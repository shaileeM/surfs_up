from flask import Flask
app = Flask(__name__)

#define the starting point, also known as the root
@app.route('/')
def hello_world():
    return 'Hello World'


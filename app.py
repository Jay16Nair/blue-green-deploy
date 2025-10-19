from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    color = os.getenv("APP_COLOR", "blue")
    return f"<h1 style='color:{color}'>Hello from {color} version!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

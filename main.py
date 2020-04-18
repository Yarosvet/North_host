from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')

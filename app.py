from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bomb')
def bomb():
    return render_template('bomb.html')


if __name__ == '__main__':
    app.debug = True
    app.run()


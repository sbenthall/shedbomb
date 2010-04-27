from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bomb',methods=['GET','POST'])
def bomb():

    if request.method == 'POST':
        question=request.form['question']
    else:
        question=request.args.get('question','Did you forget to ask a question?')
    return render_template('bomb.html',question=question)

if __name__ == '__main__':
    app.debug = True
    app.run()


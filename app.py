from flask import Flask
from flask import render_template
from flask import request
from mongokit import *

app = Flask(__name__)


class Bikeshed(Document):
    structure = {
        'question':unicode,
        'answers': [unicode]
        }
    # required_fields = ['question']
    # default_values = {'question':u''}    

con = Connection()
con.register([Bikeshed])

shedbombdb = con.shedbomb
bikesheds = shedbombdb.bikesheds

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bomb',methods=['GET','POST'])
def bomb():
    if request.method == 'POST':
        question=request.form['question']
    else:
        question=request.args.get('question','Did you forget to ask a question?')

    bikesheds.Bikeshed({
            'question': question,
            'answers' : []
            }).save()

    return render_template('bomb.html',question=question)

@app.route('/answer',methods=['GET','PUT','DELETE'])
def answer():
    shed = bikesheds.Bikeshed.find_one({
            'question': request.values['question']
            })

    question = request.values['question']
    answer = request.values['answer']

    if request.method == 'PUT':
        shed['answers'].append(answer)
        shed.save();

    elif request.method == 'DELETE':
        shed['answers'].remove(answer)
        shed.save();

    return  request.method + ' - ' + question + ' - ' + answer


if __name__ == '__main__':
    app.debug = True
    app.run()


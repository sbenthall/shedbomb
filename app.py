from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import os.path
import json
from mongokit import *

app = Flask(__name__)

### FIX THIS LATER -- should persist this in a file ##
sitedata = "sitedata.txt"

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

def new_shed_id():

    if not os.path.isfile(sitedata):
        file = open(sitedata,"w")
        file.write("0")
        file.close()

    file = open(sitedata,'r')
    shed_id = int(file.read())
    file.close()
    shed_id += 1

    file = open(sitedata,'w')
    file.write(str(shed_id))
    file.close()
    return shed_id
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bomb',methods=['POST'])
def new_bomb():
    if request.method == 'POST':
        question=request.form['question']
    else:
        question=request.args.get('question','Did you forget to ask a question?')

    shed_id = new_shed_id()

    bikesheds.Bikeshed({
            'question': question,
            'answers' : [], 
            '_id' : shed_id,
            }).save()

    print bikesheds.Bikeshed.find_one({
            'question': request.values['question']
            })


    return redirect("/bomb/" + str(shed_id))

@app.route('/bomb/<int:shed_id>',methods=['GET','POST'])
def bomb(shed_id):
    shed = bikesheds.Bikeshed.find_one({
            '_id' : shed_id
            })

    question = shed['question']
    answers = shed['answers']

    return render_template('bomb.html',question=question,shed_id=shed_id, answers=json.dumps(answers))



@app.route('/bomb/<int:shed_id>/answer',methods=['GET','PUT'])
def answer(shed_id):
    shed = bikesheds.Bikeshed.find_one({
            '_id': shed_id
            })

    answer = request.values['answer']

    if request.method == 'PUT':
        shed['answers'].append(answer)
        shed.save();
        
        return request.method + ' - ' + shed['question'] + ' - ' + answer

    elif request.method == 'GET':
        return shed['answers']


@app.route('/bomb/<int:shed_id>/<answer>',methods=['DELETE'])
def remove_answer(shed_id, answer):
    shed = bikesheds.Bikeshed.find_one({
            '_id': shed_id
            })

    shed['answers'].remove(answer)
    shed.save();

    return str(shed['answers'])



if __name__ == '__main__':
    app.debug = True
    app.run()


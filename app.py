from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import os.path
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

    file = open(sitedata,'r+')
    shed_id = int(file.read())
    shed_id += 1
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

@app.route('/bomb/<int:id>',methods=['GET','POST'])
def bomb(id):
    shed = bikesheds.Bikeshed.find_one({
            '_id' : id
            })

    question = shed['question']

    return render_template('bomb.html',question=question,shed_id=id)



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

    return request.method + ' - ' + question + ' - ' + answer


if __name__ == '__main__':
    app.debug = True
    app.run()


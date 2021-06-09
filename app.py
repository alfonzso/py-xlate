from flask import Flask
from flask import render_template
from flask import request
from boxes import boxes

app = Flask(__name__)


@app.route('/')
def hello_world():
    # return 'Hello, World!'
    return render_template('index.html', boxes=boxes)


@app.route('/text', methods=['POST'])
def its_a_text():
    print(
        request.form
    )

from xlate import a85_decode, ascii_to_xlate, b32_decode, b64_decode, bindecode, decdecode, hexdecode, octaldecode
from flask import Flask, render_template, request, redirect, session, url_for
from boxes import boxes
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def hello_world():
    messages = {}
    if 'messages' in session:
        messages = json.loads(session['messages'])

    for x in boxes:
        x.textarea.value = messages.get(x.id, "")

    session.clear()
    return render_template('index.html', boxes=boxes)


@app.route('/text', methods=['POST'])
def its_a_text():
    text = request.form.get('ascii')
    messages = json.dumps(ascii_to_xlate(text))
    session['messages'] = messages
    return redirect(request.referrer)


@app.route('/bin', methods=['POST'])
def bin():
    messages = json.dumps(
        ascii_to_xlate(
            bindecode(request.form.get('bin'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@app.route('/oct', methods=['POST'])
def oct():
    messages = json.dumps(
        ascii_to_xlate(
            octaldecode(request.form.get('oct'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@app.route('/hex', methods=['POST'])
def hex():
    messages = json.dumps(
        ascii_to_xlate(
            hexdecode(request.form.get('hex'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@app.route('/b32', methods=['POST'])
def b32():
    messages = json.dumps(
        ascii_to_xlate(
            b32_decode(request.form.get('b32'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@app.route('/b64', methods=['POST'])
def b64():
    messages = json.dumps(
        ascii_to_xlate(
            b64_decode(request.form.get('b64'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@app.route('/a85', methods=['POST'])
def a85():
    messages = json.dumps(
        ascii_to_xlate(
            a85_decode(request.form.get('a85'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@app.route('/char', methods=['POST'])
def char():
    messages = json.dumps(
        ascii_to_xlate(
            decdecode(request.form.get('char'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)

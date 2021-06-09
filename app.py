from flask import Flask, render_template, request, redirect, session, url_for
from boxes import boxes
import json
from xlate import *

app = Flask(__name__)
app.debug = True
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True

# [session.pop(key) for key in list(session.keys())]


@app.route('/')
def hello_world():
    # session.clear()
    # return 'Hello, World!'

    print(
        request.args
    )
    messages = {}
    # if 'messages' in request.args:
    if 'messages' in session:
        # messages = json.loads(request.args['messages']).get("main")
        # messages = json.loads(request.args['messages'])
        messages = json.loads(session['messages'])
        print(
            messages
        )

    for x in boxes:
        # print(x.id)
        # x.textarea.value = messages
        x.textarea.value = messages.get(x.id, "")

    session.clear()
    return render_template('index.html', boxes=boxes)


@app.route('/text', methods=['POST'])
def its_a_text():
    text = request.form.get('ascii')
    messages = json.dumps(ascii_to_xlate(text)
                          # {
                          #     "text": text,
                          #     "bin": binencode(text),
                          #     "oct": oct_encode(text),
                          #     "hex": hexencode(text),
                          #     "b32": base64.b32encode(bytes(text, encoding='utf8')).decode("utf-8"),
                          #     "b64": base64.b64encode(bytes(text, encoding='utf8')).decode("utf-8"),
                          #     "a85": base64.a85encode(bytes(text, encoding='utf8')).decode("utf-8"),
                          #     "char": decencode(text),
                          #     "hash": "\n".join(text_to_all_hash_method(text)),
                          # }
                          )
    session['messages'] = messages
    return redirect(request.referrer)


@app.route('/bin', methods=['POST'])
def bin():
    pass

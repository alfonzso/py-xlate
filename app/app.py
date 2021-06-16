from app.xlate import a85_decode, ascii_to_xlate, b32_decode, b64_decode, bindecode, decdecode, hexdecode, octaldecode
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from app.boxes import boxes
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.run(threaded=True)

# @app.route('/', methods=['GET', 'POST']))


def dummy_ascii(x):
    return x


decode_map = {
    "bin": bindecode,
    "ascii": dummy_ascii,
    "oct": octaldecode,
    "hex": hexdecode,
    "b32": b32_decode,
    "b64": b64_decode,
    "a85": a85_decode,
    "char": decdecode,
}

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # messages = {}
    # if 'messages' in session:
    # messages = json.loads(session['messages'])

    # data = json.loads(request.args.get('data'))
    # # bindecode(request.form.get('bin'))
    # if data:
    #   d_func = decode_map.get(data.get("dtype"))
    #   messages = json.dumps(
    #       ascii_to_xlate(
    #           d_func(data.get("val"))
    #       )
    #   )
    #   for x in boxes:
    #       x.textarea.value = messages.get(x.id, "")

    # session.clear()
    f = request.form
    data = {}
    for key, val in f.items():

        # if data:
        d_func = decode_map.get(key)
        # messages = json.dumps(
        messages = ascii_to_xlate(
            d_func(val)
        )
        # )
        print(
            messages
        )
        for x in boxes:
            x.textarea.value = messages.get(x.id, "")
    return render_template('index.html', boxes=boxes)


@app.route('/text', methods=['POST'])
def ascii():
    # messages = json.dumps(
    #     ascii_to_xlate(request.form.get('ascii'))
    # )
    # session['messages'] = messages
    # return redirect(request.referrer)
    # return redirect(url_for('hello_world', dtype=json.dumps(request.endpoint)))
    # data = json.dumps({"dtype": request.endpoint, "val": request.form.get(request.endpoint)})
    data = {"dtype": request.endpoint, "val": request.form.get(request.endpoint)}
    # data = json.loads(request.args.get('data'))
    # bindecode(request.form.get('bin'))
    print(
        data
    )
    if data:
        d_func = decode_map.get(data.get("dtype"))
        # messages = json.dumps(
        messages = ascii_to_xlate(
            d_func(data.get("val"))
        )
        # )
        print(
            messages
        )
        for x in boxes:
            x.textarea.value = messages.get(x.id, "")
    # return render_template('index.html', boxes=boxes)
    return jsonify(json.dumps(boxes))
    # return redirect(url_for('hello_world', data=json.dumps({"dtype": request.endpoint, "val": request.form.get(request.endpoint)})))


@ app.route('/bin', methods=['POST'])
def bin():
    # messages = json.dumps(
    #     ascii_to_xlate(
    #         bindecode(request.form.get('bin'))
    #     )
    # )
    # session['messages'] = messages
    # return redirect(request.referrer)
    # return redirect(url_for('hello_world', json=json.dumps(messages)), code=307)
    return redirect(url_for('hello_world', data=json.dumps({"dtype": request.endpoint, "val": request.form.get(request.endpoint)})))
    # return requests.post(request.url_root + '/', data={"test": True})
    # resp = requests.post(request.url_root , data={"test": True})
    # return r
    # resp.headers['location'] = '/votes/1'
    # resp.autocorrect_location_header = False
    # return (resp.text, resp.status_code, resp.headers.items())


@ app.route('/oct', methods=['POST'])
def oct():
    messages = json.dumps(
        ascii_to_xlate(
            octaldecode(request.form.get('oct'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@ app.route('/hex', methods=['POST'])
def hex():
    messages = json.dumps(
        ascii_to_xlate(
            hexdecode(request.form.get('hex'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@ app.route('/b32', methods=['POST'])
def b32():
    messages = json.dumps(
        ascii_to_xlate(
            b32_decode(request.form.get('b32'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@ app.route('/b64', methods=['POST'])
def b64():
    messages = json.dumps(
        ascii_to_xlate(
            b64_decode(request.form.get('b64'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@ app.route('/a85', methods=['POST'])
def a85():
    messages = json.dumps(
        ascii_to_xlate(
            a85_decode(request.form.get('a85'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)


@ app.route('/char', methods=['POST'])
def char():
    messages = json.dumps(
        ascii_to_xlate(
            decdecode(request.form.get('char'))
        )
    )
    session['messages'] = messages
    return redirect(request.referrer)

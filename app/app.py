from app.xlate import a85_decode, ascii_to_xlate, b32_decode, b64_decode, bindecode, decdecode, hexdecode, octaldecode
from flask import Flask, render_template, request
from app.boxes import boxes

app = Flask(__name__)
app.debug = True
app.secret_key = 'super secret key'

decode_map = {
    "bin": bindecode,
    "ascii": lambda a: a,
    "oct": octaldecode,
    "hex": hexdecode,
    "b32": b32_decode,
    "b64": b64_decode,
    "a85": a85_decode,
    "char": decdecode,
}


@app.route('/', methods=['GET', 'POST'])
def root():
    for key, val in request.form.items():
        try:
            messages = ascii_to_xlate(
                decode_map.get(key)(val)
            )
        except Exception as e:
            messages = {key: str(e)}
        for x in boxes:
            x.textarea.value = messages.get(x.id, "")
    return render_template('index.html', boxes=boxes)

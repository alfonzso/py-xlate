from flask import Flask, render_template, request

from app.boxes import get_boxes
from app.xlate.helpers import ascii_to_xlate
from app.xlate import encdec

flskapp = Flask(__name__)
flskapp.debug = True
flskapp.secret_key = "super secret key"

decode_map = {
    "bin": encdec.bin_decode,
    "ascii": lambda a: a,
    "oct": encdec.octal_decode,
    "hex": encdec.hex_decode,
    "b32": encdec.b32_decode,
    "b64": encdec.b64_decode,
    "a85": encdec.a85_decode,
    "char": encdec.dec_decode,
}


@flskapp.route("/", methods=["GET", "POST"])
def root():
    _boxes = get_boxes()
    for key, val in request.form.items():
        try:
            messages = ascii_to_xlate(decode_map.get(key)(val))
        except Exception as e:
            messages = {key: str(e)}

        for x in _boxes:
            x.textarea.value = messages.get(x.id, "")
    return render_template("index.html", boxes=_boxes)

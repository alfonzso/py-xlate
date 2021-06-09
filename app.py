from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


class SaveAllKwargs(object):
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            # assert(k in self.__class__.__allowed)
            setattr(self, k, v)

    def get_html_attrs(self):
        # _attrs = ""
        # _attrs = " ".join([f"{key}='{val}'  " for key, val in self.__dict__.items()])
        _cls = {}
        for key, val in self.__dict__.items():
            _cls.update({key: val})
        # _cls = f"class={self.cls}" if self.cls else ""
        # _cls = f"class='{self.cls}'" if hasattr(self, 'cls') else ""
        _cls.update({"class": f"{self.cls}"} if hasattr(self, 'cls') else {"": ""})
        # print(
        # f"{_cls} {_attrs}"
        # )
        return _cls


class Boxes(SaveAllKwargs):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Li(SaveAllKwargs):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Form(SaveAllKwargs):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Address(SaveAllKwargs):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Input(SaveAllKwargs):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Textarea(SaveAllKwargs):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    # def get_html_attrs(self):
    #     # _attrs = ""
    #     _attrs = " ".join([f"{key}={val} " for key, val in self.__dict__.items()])
    #     return f""" class={self.cls} {_attrs}"""


boxes = [
    Boxes(
        li=Li(
            cls="box full",
            id="text",
        ),
        form=Form(
            method="POST",
            action="/text",
        ),
        href=Address(
            url="https://www.paulschou.com/tools/ascii/",
            content="TEXT",
        ),
        textarea=Textarea(
            cols="80",
            rows="10",
            wrap="virtual",
            name="ascii",
            id="text_input",
            cls="box-text",
        ),
        input=Input(
            type="submit",
            cls="btn",
            value="< ENCODE >"
        )
    ), Boxes(
        li=Li(
            cls="box",
            id="bin",
        ),
        form=Form(
            method="POST",
            action="/bin",
        ),
        href=Address(
            url="https://en.wikipedia.org/wiki/Binary_numeral_system",
            content="BINARY",
        ),
        textarea=Textarea(
            cols="35", rows="10", wrap="virtual", name="bin", id="bin_input", cls="box-text"
        ),
        input=Input(
            type="submit",
            cls="btn",
            value="< DECODE >"
        )
    ), Boxes(
        li=Li(
            cls="box",
            id="oct",
        ),
        form=Form(
            method="POST",
            action="/oct",
        ),
        href=Address(
            url="https://en.wikipedia.org/wiki/Octal",
            content="OCT",
        ),
        textarea=Textarea(
            cols="35", rows="10", wrap="virtual", name="oct", id="oct_input", cls="box-text"
        ),
        input=Input(
            type="submit",
            cls="btn",
            value="< DECODE >"
        )
    ), Boxes(
        li=Li(
            cls="box",
            id="hex",
        ),
        form=Form(
            method="POST",
            action="/hex",
        ),
        href=Address(
            url="https://en.wikipedia.org/wiki/Hexidecimal",
            content="HEX",
        ),
        textarea=Textarea(
            cols="35", rows="10", wrap="virtual", name="hex", id="hex_input", cls="box-text"
        ),
        input=Input(
            type="submit",
            cls="btn",
            value="< DECODE >"
        )
    ), Boxes(
        li=Li(
            cls="box",
            id="b32",
        ),
        form=Form(
            method="POST",
            action="/b32",
        ),
        href=Address(
            url="https://en.wikipedia.org/wiki/Base32",
            content="BASE32",
        ),
        textarea=Textarea(
            cols="35", rows="10", wrap="virtual", name="b32", id="b32_input", cls="box-text"
        ),
        input=Input(
            type="submit",
            cls="btn",
            value="< DECODE >"
        )
    ), Boxes(
        li=Li(
            cls="box",
            id="b64",
        ),
        form=Form(
            method="POST",
            action="/b64",
        ),
        href=Address(
            url="https://en.wikipedia.org/wiki/Base64",
            content="BASE64",
        ),
        textarea=Textarea(
            cols="35", rows="10", wrap="virtual", name="b64", id="b64_input", cls="box-text"
        ),
        input=Input(
            type="submit",
            cls="btn",
            value="< DECODE >"
        )
    ), Boxes(
        li=Li(
            cls="box",
            id="a85",
        ),
        form=Form(
            method="POST",
            action="/a85",
        ),
        href=Address(
            url="https://en.wikipedia.org/wiki/Ascii85",
            content="ASCII85",
        ),
        textarea=Textarea(
            cols="35", rows="10", wrap="virtual", name="a85", id="a85_input", cls="box-text"
        ),
        input=Input(
            type="submit",
            cls="btn",
            value="< DECODE >"
        )
    ), Boxes(
        li=Li(
            cls="box",
            id="char",
        ),
        form=Form(
            method="POST",
            action="/char",
        ),
        href=Address(
            url="https://en.wikipedia.org/wiki/ASCII",
            content="CHAR / DEC",
        ),
        textarea=Textarea(
            cols="35", rows="10", wrap="virtual", name="char", id="char_input", cls="box-text"
        ),
        input=Input(
            type="submit",
            cls="btn",
            value="< DECODE >"
        )
    ), Boxes(
        li=Li(
            cls="box",
            id="hash",
        ),
        form=Form(
            method="POST",
            # action="/hash",
        ),
        href=Address(
            url="",
            content="TEXT INFO",
        ),
        textarea=Textarea(
            cols="35", rows="10", wrap="off", name="hash", id="hash_input", readonly="true", cls="box-text"
        ),
        input=Input(
            # type="submit",
            # cls="btn",
            # value="< DECODE >"
        )
    ),
]


@app.route('/')
def hello_world():
    # return 'Hello, World!'
    return render_template('index.html', boxes=boxes)


@app.route('/text', methods=['POST'])
def its_a_text():
    print(
        request.form
    )

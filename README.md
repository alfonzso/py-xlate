## Resources

Original idea from https://paulschou.com/tools/xlate/
<br>
Encoder and Decoder functions: https://github.com/Iansus/xlate

# xlate

Original functionality taken from https://paulschou.com/tools/xlate/ and whole site impleted in python 3 .

## Usage

### 1) Install deps with poetry

```shell
curl -sSL https://install.python-poetry.org | python3 -
poetry install --no-root
```

### 2) Run flask

```shell
flask --app app/main run --host 0.0.0.0
```

### 3) Profit !!!

# Examples for flask and for xlate

flask --app app/main run --host 0.0.0.0 --debug

echo "keke" | python -m app.xlate -i ascii -o b64 | python -m app.xlate -i b64 -o ascii

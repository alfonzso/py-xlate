# DECODE/ENCODE FUNCS
def return_self(s):
    return s


# DEFAULTS
DEFAULT_NAME = "ascii"
DEFAULT_ENC_FUNCTION = return_self
DEFAULT_DEC_FUNCTION = return_self

# GLOBAL OPTIONS
OPT_NO_INPUT_SPACE = False
OPT_NO_OUTPUT_SPACE = False
OPT_NO_INPUT_NAME = "--no-input-spaces"
OPT_NO_OUTPUT_NAME = "--no-output-spaces"


class FormatException(RuntimeError):
    pass


class DecodeException(RuntimeError):
    pass


class EncodeException(RuntimeError):
    pass

import base64
import hashlib

from . import (
    OPT_NO_INPUT_NAME,
    OPT_NO_INPUT_SPACE,
    OPT_NO_OUTPUT_SPACE,
    DecodeException,
)


def hex_decode(s) -> str:
    if not OPT_NO_INPUT_SPACE:
        s = s.replace(" ", "")

    return bytes.fromhex(s).decode("utf-8")


def octal_decode(s) -> str:
    """
    It takes an octal string and return a string
        :octal_str: octal str like "110 145 154"
    """
    str_converted = ""
    for octal_char in s.split(" "):
        str_converted += chr(int(octal_char, 8))
    ret = " ".join(
        map(str, map(ord, [str_converted[i] for i in range(0, len(str_converted))]))
    )
    return "".join(map(chr, map(int, ret.strip().split(" "))))


def oct_encode(s) -> str | list:
    ret = []
    for i in s:
        ret.append(str(oct(ord(i))[2:]))
    if not OPT_NO_OUTPUT_SPACE:
        ret = " ".join(ret)
    return ret


def hex_encode(s) -> str:
    # ret = s.encode('hex')
    ret = s.encode("utf-8").hex()
    if not OPT_NO_OUTPUT_SPACE:
        ret = " ".join(ret[i : i + 2] for i in range(0, len(ret), 2))

    return ret


def ashex_decode(s) -> str:
    return hex_decode(s.replace("\\x", ""))


def ashex_encode(s) -> str:
    ret = "\\x".join([hex(ord(e))[2:].zfill(2) for e in s])

    return "" if ret == "" else "\\x" + ret


def dec_decode(s) -> str:
    if OPT_NO_INPUT_SPACE:
        raise DecodeException(
            "Option %s is not supported with decimal decoding" % OPT_NO_INPUT_NAME
        )
    # s = clean_and_set_spacing(s, 3)
    return "".join(map(chr, map(int, s.strip().split(" "))))


def dec_encode(s) -> str:
    return " ".join(map(str, map(ord, [s[i] for i in range(0, len(s))])))


def bin_decode(s) -> str:
    if not OPT_NO_INPUT_SPACE:
        s = s.replace(" ", "")

    s = s.strip()
    return "".join([chr(int(s[i : i + 8], 2)) for i in range(0, len(s), 8)])


def bin7_decode(s) -> str:
    if not OPT_NO_INPUT_SPACE:
        s = s.replace(" ", "")

    s = s.strip()
    return "".join([chr(int(s[i : i + 7], 2)) for i in range(0, len(s), 7)])


def bin_encode(s) -> str:
    j = "" if OPT_NO_OUTPUT_SPACE else " "
    return j.join([bin(ord(s[i]))[2:].zfill(8) for i in range(0, len(s))])


def revhex64(s) -> str:
    j = "" if OPT_NO_OUTPUT_SPACE else " "
    return j.join(
        ["0x" + s[i : i + 8][::-1].encode("hex") for i in range(0, len(s), 8)]
    )


def revhex(s) -> str:
    j = "" if OPT_NO_OUTPUT_SPACE else " "
    return j.join(
        ["0x" + s[i : i + 4][::-1].encode("hex") for i in range(0, len(s), 4)]
    )


def b32_encode(s) -> str:
    return base64.b32encode(bytes(s, encoding="utf8")).decode("utf-8")


def a85_encode(s) -> str:
    return base64.a85encode(bytes(s, encoding="utf8")).decode("utf-8")


def b32_decode(s) -> str:
    return base64.b32decode(bytes(s, encoding="utf8")).decode("utf-8")


def b64_encode(s) -> str:
    return base64.b64encode(bytes(s, encoding="utf8")).decode("utf-8")


def b64_decode(s) -> str:
    return base64.b64decode(bytes(s, encoding="utf8")).decode("utf-8")


def a85_decode(s) -> str:
    return base64.a85decode(bytes(s, encoding="utf8")).decode("utf-8")


def md5(s) -> str:
    return hashlib.md5(s).hexdigest()


def sha1(s) -> str:
    return hashlib.sha1(s).hexdigest()


def sha224(s) -> str:
    return hashlib.sha224(s).hexdigest()


def sha256(s) -> str:
    return hashlib.sha256(s).hexdigest()


def sha384(s) -> str:
    return hashlib.sha384(s).hexdigest()


def sha512(s) -> str:
    return hashlib.sha512(s).hexdigest()

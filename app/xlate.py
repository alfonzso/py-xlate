#!/usr/bin/python

import base64
import hashlib
import argparse
import sys


class FormatException(RuntimeError):
    pass


class DecodeException(RuntimeError):
    pass


class EncodeException(RuntimeError):
    pass


def clean_and_set_spacing(s, space):
    s = s.replace(" ", "")
    return ' '.join(s[i:i + space] for i in range(0, len(s), space))
    # return s


# GLOBAL OPTIONS
OPT_NO_INPUT_SPACE = False
OPT_NO_OUTPUT_SPACE = False
OPT_NO_INPUT_NAME = '--no-input-spaces'
OPT_NO_OUTPUT_NAME = '--no-output-spaces'

# DECODE/ENCODE FUNCS


def identity(s):
    return s


def hexdecode(s):
    if not OPT_NO_INPUT_SPACE:
        s = s.replace(' ', '')

    return bytes.fromhex(s).decode('utf-8')


def octaldecode(s):
    '''
    It takes an octal string and return a string
        :octal_str: octal str like "110 145 154"
    '''
    print(s)
    str_converted = ""
    t_list_f = []
    t_list_ff = []
    # s = clean_and_set_spacing(s, 3)
    for octal_char in s.split(" "):
        f = int(octal_char, 8)
        ff = chr(f)
        t_list_f.append(f)
        t_list_ff.append(ff)
        str_converted += ff
        # print(f, end='')
        # print(ff, end='')
    print(t_list_f)
    print(t_list_ff)
    # return str_converted
    ret = ' '.join(map(str, map(ord, [str_converted[i] for i in range(0, len(str_converted))])))
    return ''.join(map(chr, map(int, ret.strip().split(' '))))


def oct_encode(s):
    ret = []
    for i in s:
        ret.append(str(oct(ord(i))[2:]))
    if not OPT_NO_OUTPUT_SPACE:
        ret = ' '.join(ret)
    return ret


def hexencode(s):
    # ret = s.encode('hex')
    ret = s.encode("utf-8").hex()
    if not OPT_NO_OUTPUT_SPACE:
        ret = ' '.join(ret[i:i + 2] for i in range(0, len(ret), 2))

    return ret


def ashexdecode(s):
    return hexdecode(s.replace('\\x', ''))


def ashexencode(s):
    ret = '\\x'.join([hex(ord(e))[2:].zfill(2) for e in s])

    return '' if ret == '' else '\\x' + ret


def decdecode(s):
    if OPT_NO_INPUT_SPACE:
        raise DecodeException('Option %s is not supported with decimal decoding' % OPT_NO_INPUT_NAME)
    # s = clean_and_set_spacing(s, 3)
    return ''.join(map(chr, map(int, s.strip().split(' '))))


def decencode(s):
    return ' '.join(map(str, map(ord, [s[i] for i in range(0, len(s))])))


def bindecode(s):
    if not OPT_NO_INPUT_SPACE:
        s = s.replace(' ', '')

    s = s.strip()
    return ''.join([chr(int(s[i:i + 8], 2)) for i in range(0, len(s), 8)])


def bin7decode(s):
    if not OPT_NO_INPUT_SPACE:
        s = s.replace(' ', '')

    s = s.strip()
    return ''.join([chr(int(s[i:i + 7], 2)) for i in range(0, len(s), 7)])


def binencode(s):
    j = '' if OPT_NO_OUTPUT_SPACE else ' '
    return j.join([bin(ord(s[i]))[2:].zfill(8) for i in range(0, len(s))])


def revhex64(s):
    j = '' if OPT_NO_OUTPUT_SPACE else ' '
    sw = s + '\x00'
    return j.join(['0x' + s[i:i + 8][::-1].encode('hex') for i in range(0, len(s), 8)])


def revhex(s):
    j = '' if OPT_NO_OUTPUT_SPACE else ' '
    sw = s + '\x00'
    return j.join(['0x' + s[i:i + 4][::-1].encode('hex') for i in range(0, len(s), 4)])


def b32_decode(s):
    return base64.b32decode(bytes(s, encoding='utf8')).decode("utf-8")


def b64_decode(s):
    return base64.b64decode(bytes(s, encoding='utf8')).decode("utf-8")


def a85_decode(s):
    return base64.a85decode(bytes(s, encoding='utf8')).decode("utf-8")


def ascii_to_xlate(s):
    return {
        "text": s,
        "bin": binencode(s),
        "oct": oct_encode(s),
        "hex": hexencode(s),
        "b32": base64.b32encode(bytes(s, encoding='utf8')).decode("utf-8"),
        "b64": base64.b64encode(bytes(s, encoding='utf8')).decode("utf-8"),
        "a85": base64.a85encode(bytes(s, encoding='utf8')).decode("utf-8"),
        "char": decencode(s),
        "hash": "\n".join(ascii_to_all_hash_method(s)),
    }

# ONE WAY FUNCS


def ascii_to_all_hash_method(s):
    hashes = []
    algos = sorted(hashlib.algorithms_available)
    for algo in algos:
        h = hashlib.new(algo)
        h.update(bytes(s, encoding='utf8'))
        if algo == 'shake_128':
            hashes.append(f"{algo}: {h.hexdigest(64)}")
        elif algo == 'shake_256':
            hashes.append(f"{algo}: {h.hexdigest(128)}")
        else:
            hashes.append(f"{algo}: {h.hexdigest()}")
    return hashes


def md5(s):
    return hashlib.md5(s).hexdigest()


def sha1(s):
    return hashlib.sha1(s).hexdigest()


def sha224(s):
    return hashlib.sha224(s).hexdigest()


def sha256(s):
    return hashlib.sha256(s).hexdigest()


def sha384(s):
    return hashlib.sha384(s).hexdigest()


def sha512(s):
    return hashlib.sha512(s).hexdigest()


# DEFAULTS
DEFAULT_NAME = 'ascii'
DEFAULT_ENC_FUNCTION = identity
DEFAULT_DEC_FUNCTION = identity


# INPUT AND OUTPUT FORMATS
INPUT_FORMATS = [
    ([DEFAULT_NAME], DEFAULT_DEC_FUNCTION, DEFAULT_ENC_FUNCTION),
    (['base64', 'b64'], base64.b64decode, base64.b64encode),
    (['hex'], hexdecode, hexencode),
    (['antislash-hex'], ashexdecode, ashexencode),
    (['dec'], decdecode, decencode),
    (['bin'], bindecode, binencode),
    (['bin7'], bin7decode, None),
]


ONE_WAY_FUNCS = [
    (['md5'], None, md5),
    (['sha1'], None, sha1),
    (['sha224'], None, sha224),
    (['sha256'], None, sha256),
    (['sha384'], None, sha384),
    (['sha512'], None, sha512),
    (['revhex64'], None, revhex64),
    (['revhex'], None, revhex),
]

OUTPUT_FORMATS = INPUT_FORMATS + ONE_WAY_FUNCS

if __name__ == '__main__':

    p = argparse.ArgumentParser(description='Encoding converter')

    p.add_argument('--input-format', '-i', dest='iformat', default=DEFAULT_NAME, metavar='INPUT_FORMAT', help='Formatting of the input, default=%s' % DEFAULT_NAME)
    p.add_argument('--output-format', '-o', dest='oformat', default=DEFAULT_NAME, metavar='OUTPUT_FORMAT', help='Formatting of the output, default=%s' % DEFAULT_NAME)

    p.add_argument('--list', '-l', action='store_true', dest='list', help='Lists input & output formats')

    p.add_argument(OPT_NO_INPUT_NAME, action='store_true', dest='ispace', default=False, help='Tells the program to consider no spaces in the input')
    p.add_argument(OPT_NO_OUTPUT_NAME, action='store_true', dest='ospace', default=False, help='Tells the program to consider no spaces in the output')

    args = p.parse_args()

    if args.list:
        print('Input formats:')
        for format in INPUT_FORMATS:
            print('\t' + '/'.join(format[0]))
        print('')

        print('Output formats:')
        for format in OUTPUT_FORMATS:
            print('\t' + '/'.join(format[0]))
        print()

    else:
        OPT_NO_INPUT_SPACE = args.ispace
        OPT_NO_OUTPUT_SPACE = args.ospace

        try:
            inputFormat = None
            outputFormat = None

            for f in INPUT_FORMATS:
                if args.iformat in f[0]:
                    inputFormat = f
                    break

            if inputFormat is None:
                raise FormatException('Format %s not found' % args.iformat)

            for f in OUTPUT_FORMATS:
                if args.oformat in f[0]:
                    outputFormat = f
                    break

            if outputFormat is None:
                raise FormatException('Format %s not found' % args.oformat)

            ecData = sys.stdin.read()
            dcData = inputFormat[1](ecData)
            recData = outputFormat[2](dcData)

            sys.stdout.write(recData)
            sys.stdout.flush()

        except FormatException as e:
            sys.stderr.write('[X] Error encountered while searching format: %s' % str(e))
            sys.stderr.flush()
            sys.exit(1)

        except DecodeException as e:
            sys.stderr.write('[X] Error encountered during decoding : %s' % str(e))
            sys.stderr.flush()
            sys.exit(1)

        except EncodeException as e:
            sys.stderr.write('[X] Error encountered during decoding : %s' % str(e))
            sys.stderr.flush()
            sys.exit(1)

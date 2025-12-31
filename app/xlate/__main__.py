import argparse
import sys
from typing import Callable, List

from . import (
    DEFAULT_DEC_FUNCTION,
    DEFAULT_ENC_FUNCTION,
    DEFAULT_NAME,
    OPT_NO_INPUT_NAME,
    OPT_NO_INPUT_SPACE,
    OPT_NO_OUTPUT_NAME,
    OPT_NO_OUTPUT_SPACE,
    DecodeException,
    EncodeException,
    FormatException,
    encdec,
)

# import types


class XLFormats:
    # name: str
    # alias: list[str]
    _name: List[str]
    _decoder: Callable
    _encoder: Callable

    def __init__(
        # self, name: list[str], decoder: types.FunctionType, encoder: types.FunctionType
        self,
        name: List[str],
        decoder: Callable,
        encoder: Callable,
    ):
        self._name = name
        self._decoder = decoder
        self._encoder = encoder

    def get_names(self):
        return "|".join(self._name)


class XLate:
    _inputs: List[XLFormats]
    _outputs: List[XLFormats]
    _hashes: XLFormats
    _default: XLFormats

    def __init__(self):
        self._default = XLFormats(
            [DEFAULT_NAME], DEFAULT_DEC_FUNCTION, DEFAULT_ENC_FUNCTION
        )
        self._inputs = [
            XLFormats(["base64", "b64"], encdec.b64_decode, encdec.b64_encode),
            XLFormats(["hex"], encdec.hex_decode, encdec.hex_encode),
            XLFormats(["antislash-hex"], encdec.ashex_decode, encdec.ashex_encode),
            XLFormats(["dec"], encdec.dec_decode, encdec.dec_encode),
            XLFormats(["bin"], encdec.bin_decode, encdec.bin_encode),
            XLFormats(["bin7"], encdec.bin7_decode, None),
        ]
        self._hashes = [
            XLFormats(["md5"], None, encdec.md5),
            XLFormats(["sha1"], None, encdec.sha1),
            XLFormats(["sha224"], None, encdec.sha224),
            XLFormats(["sha256"], None, encdec.sha256),
            XLFormats(["sha384"], None, encdec.sha384),
            XLFormats(["sha512"], None, encdec.sha512),
            XLFormats(["revhex64"], None, encdec.revhex64),
            XLFormats(["revhex"], None, encdec.revhex),
        ]
        self._outputs = self._inputs + self._outputs


# # INPUT AND OUTPUT FORMATS
# INPUT_FORMATS = [
#     ([DEFAULT_NAME], DEFAULT_DEC_FUNCTION, DEFAULT_ENC_FUNCTION),
#     (["base64", "b64"], encdec.b64_decode, encdec.b64_encode),
#     (["hex"], encdec.hex_decode, encdec.hex_encode),
#     (["antislash-hex"], encdec.ashex_decode, encdec.ashex_encode),
#     (["dec"], encdec.dec_decode, encdec.dec_encode),
#     (["bin"], encdec.bin_decode, encdec.bin_encode),
#     (["bin7"], encdec.bin7_decode, None),
# ]


# ONE_WAY_FUNCS = [
#     (["md5"], None, encdec.md5),
#     (["sha1"], None, encdec.sha1),
#     (["sha224"], None, encdec.sha224),
#     (["sha256"], None, encdec.sha256),
#     (["sha384"], None, encdec.sha384),
#     (["sha512"], None, encdec.sha512),
#     (["revhex64"], None, encdec.revhex64),
#     (["revhex"], None, encdec.revhex),
# ]

# OUTPUT_FORMATS = INPUT_FORMATS + ONE_WAY_FUNCS

if __name__ == "__main__":

    xlate = XLate()
    p = argparse.ArgumentParser(description="Encoding converter")

    p.add_argument(
        "--input-format",
        "-i",
        dest="iformat",
        default=DEFAULT_NAME,
        metavar="INPUT_FORMAT",
        help="Formatting of the input, default=%s" % DEFAULT_NAME,
    )
    p.add_argument(
        "--output-format",
        "-o",
        dest="oformat",
        default=DEFAULT_NAME,
        metavar="OUTPUT_FORMAT",
        help="Formatting of the output, default=%s" % DEFAULT_NAME,
    )

    p.add_argument(
        "--list",
        "-l",
        action="store_true",
        dest="list",
        help="Lists input & output formats",
    )

    p.add_argument(
        OPT_NO_INPUT_NAME,
        action="store_true",
        dest="ispace",
        default=False,
        help="Tells the program to consider no spaces in the input",
    )
    p.add_argument(
        OPT_NO_OUTPUT_NAME,
        action="store_true",
        dest="ospace",
        default=False,
        help="Tells the program to consider no spaces in the output",
    )

    args = p.parse_args()

    if args.list:
        print("Input formats:")
        for __output in xlate._inputs:
            print(f"\t{__output.get_names()}")
        print("")

        print("Output formats:")
        for __output in xlate._outputs:
            print(f"\t{__output.get_names()}")
        print()

    else:
        OPT_NO_INPUT_SPACE = args.ispace
        OPT_NO_OUTPUT_SPACE = args.ospace

        try:
            input = None
            output = None

            for __output in xlate._inputs:
                if args.iformat in __output.get_names():
                    input = __output
                    break

            if input is None:
                raise FormatException("Format %s not found" % args.iformat)

            # for output_format in OUTPUT_FORMATS:
            #     if args.oformat in output_format[0]:
            #         outputFormat = output_format
            #         break
            for __output in xlate._outputs:
                if args.oformat in __output.get_names():
                    input = __output
                    break

            if output is None:
                raise FormatException("Format %s not found" % args.oformat)

            input_data = sys.stdin.read()
            decoded_data = input[1](input_data)
            recData = output[2](decoded_data)

            sys.stdout.write(recData)
            sys.stdout.flush()

        except FormatException as e:
            sys.stderr.write(
                "[X] Error encountered while searching format: %s" % str(e)
            )
            sys.stderr.flush()
            sys.exit(1)

        except DecodeException as e:
            sys.stderr.write("[X] Error encountered during decoding : %s" % str(e))
            sys.stderr.flush()
            sys.exit(1)

        except EncodeException as e:
            sys.stderr.write("[X] Error encountered during decoding : %s" % str(e))
            sys.stderr.flush()
            sys.exit(1)

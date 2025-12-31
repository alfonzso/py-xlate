import argparse
import sys
from typing import Callable, List, Optional

from . import (
    DEFAULT_DEC_FUNCTION,
    DEFAULT_ENC_FUNCTION,
    DEFAULT_NAME,
    OPT_NO_INPUT_NAME,
    OPT_NO_OUTPUT_NAME,
    DecodeException,
    EncodeException,
    FormatException,
    encdec,
)


class XLFormats:
    _name: List[str]
    _decoder: Optional[Callable[[str], str]]
    _encoder: Optional[Callable[[str], str]]

    def __init__(
        self,
        name: List[str],
        decoder: Optional[Callable],
        encoder: Optional[Callable],
    ) -> None:
        self._name = name
        self._decoder = decoder
        self._encoder = encoder

    def get_names(self) -> str:
        return "|".join(self._name)


class XLate:
    _inputs: List[XLFormats]
    _outputs: List[XLFormats]
    _hashes: List[XLFormats]

    def __init__(self) -> None:
        self._inputs = [
            XLFormats([DEFAULT_NAME], DEFAULT_DEC_FUNCTION, DEFAULT_ENC_FUNCTION),
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
        self._outputs = self._inputs + self._hashes


def args_manager():
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
        "--formats",
        "-f",
        action="store_true",
        dest="formats",
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
    return args


if __name__ == "__main__":

    _xlate = XLate()
    args = args_manager()

    if args.formats:
        print("Input formats:")
        for __output in _xlate._inputs:
            print(f"\t{__output.get_names()}")
        print("")

        print("Output formats:")
        for __output in _xlate._outputs:
            print(f"\t{__output.get_names()}")
        print()

    else:
        OPT_NO_INPUT_SPACE = args.ispace
        OPT_NO_OUTPUT_SPACE = args.ospace

        try:
            input = None
            output = None

            for __input in _xlate._inputs:
                if args.iformat in __input.get_names():
                    input = __input
                    break

            if input is None:
                raise FormatException("Format %s not found" % args.iformat)

            for __output in _xlate._outputs:
                if args.oformat in __output.get_names():
                    output = __output
                    break

            if output is None:
                raise FormatException("Format %s not found" % args.oformat)

            if input._decoder is None:
                raise Exception("Decoder shouldnt be None, but it is")
            if output._encoder is None:
                raise Exception("Encoder shouldnt be None, but it is")

            input_data = sys.stdin.read()
            input_data_as_str = input._decoder(input_data)
            encoded_input_data = output._encoder(input_data_as_str)

            sys.stdout.write(encoded_input_data)
            sys.stdout.flush()
        except Exception as e:
            match e:
                case FormatException():
                    sys.stderr.write(
                        f"[X] Error encountered while searching format: {str(e)}\n"
                    )
                case DecodeException():
                    sys.stderr.write(
                        f"[X] Error encountered during decoding: {str(e)}\n"
                    )
                case EncodeException():
                    sys.stderr.write(
                        f"[X] Error encountered during encoding: {str(e)}\n"
                    )
                case _:
                    sys.stderr.write(f"[X] Unexpected error: {e}\n")
            sys.stderr.flush()
            sys.exit(1)

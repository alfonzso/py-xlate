import argparse
import sys

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

# INPUT AND OUTPUT FORMATS
INPUT_FORMATS = [
    ([DEFAULT_NAME], DEFAULT_DEC_FUNCTION, DEFAULT_ENC_FUNCTION),
    (["base64", "b64"], encdec.b64_decode, encdec.b64_encode),
    (["hex"], encdec.hex_decode, encdec.hex_encode),
    (["antislash-hex"], encdec.ashex_decode, encdec.ashex_encode),
    (["dec"], encdec.dec_decode, encdec.dec_encode),
    (["bin"], encdec.bin_decode, encdec.bin_encode),
    (["bin7"], encdec.bin7_decode, None),
]


ONE_WAY_FUNCS = [
    (["md5"], None, encdec.md5),
    (["sha1"], None, encdec.sha1),
    (["sha224"], None, encdec.sha224),
    (["sha256"], None, encdec.sha256),
    (["sha384"], None, encdec.sha384),
    (["sha512"], None, encdec.sha512),
    (["revhex64"], None, encdec.revhex64),
    (["revhex"], None, encdec.revhex),
]

OUTPUT_FORMATS = INPUT_FORMATS + ONE_WAY_FUNCS

if __name__ == "__main__":

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
        for input_format in INPUT_FORMATS:
            print("\t" + "/".join(input_format[0]))
        print("")

        print("Output formats:")
        for output_format in OUTPUT_FORMATS:
            print("\t" + "/".join(output_format[0]))
        print()

    else:
        OPT_NO_INPUT_SPACE = args.ispace
        OPT_NO_OUTPUT_SPACE = args.ospace

        try:
            inputFormat = None
            outputFormat = None

            for input_format in INPUT_FORMATS:
                if args.iformat in input_format[0]:
                    inputFormat = input_format
                    break

            if inputFormat is None:
                raise FormatException("Format %s not found" % args.iformat)

            for output_format in OUTPUT_FORMATS:
                if args.oformat in output_format[0]:
                    outputFormat = output_format
                    break

            if outputFormat is None:
                raise FormatException("Format %s not found" % args.oformat)

            ecData = sys.stdin.read()
            dcData = inputFormat[1](ecData)
            recData = outputFormat[2](dcData)

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

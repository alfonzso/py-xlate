import hashlib
from . import encdec

def clean_and_set_spacing(s, space):
    s = s.replace(" ", "")
    return " ".join(s[i : i + space] for i in range(0, len(s), space))


def ascii_to_xlate(s):
    return {
        "text": s,
        "bin": encdec.bin_encode(s),
        "oct": encdec.oct_encode(s),
        "hex": encdec.hex_encode(s),
        "b32": encdec.b32_encode(s),
        "b64": encdec.b64_encode(s),
        "a85": encdec.a85_encode(s),
        "char": encdec.dec_encode(s),
        "hash": "\n".join(ascii_to_all_hash_method(s)),
    }


def ascii_to_all_hash_method(s):
    hashes = []
    algos = sorted(hashlib.algorithms_available)
    for algo in algos:
        h = hashlib.new(algo)
        h.update(bytes(s, encoding="utf8"))
        if algo == "shake_128":
            hashes.append(f"{algo}: {h.hexdigest(64)}")
        elif algo == "shake_256":
            hashes.append(f"{algo}: {h.hexdigest(128)}")
        else:
            hashes.append(f"{algo}: {h.hexdigest()}")
    return hashes


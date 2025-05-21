BINARY_DICT = {
    "01000001": "A",
    "01000010": "B",
    "01000011": "C",
    "01000100": "D",
    "01000101": "E",
    "01000110": "F",
    "01000111": "G",
    "01001000": "H",
    "01001001": "I",
    "01001010": "J",
    "01001011": "K",
    "01001100": "L",
    "01001101": "M",
    "01001110": "N",
    "01001111": "O",
    "01010000": "P",
    "01010001": "Q",
    "01010010": "R",
    "01010011": "S",
    "01010100": "T",
    "01010101": "U",
    "01010110": "V",
    "01010111": "W",
    "01011000": "X",
    "01011001": "Y",
    "01011010": "Z",
    "01100001": "a",
    "01100010": "b",
    "01100011": "c",
    "01100100": "d",
    "01100101": "e",
    "01100110": "f",
    "01100111": "g",
    "01101000": "h",
    "01101001": "i",
    "01101010": "j",
    "01101011": "k",
    "01101100": "l",
    "01101101": "m",
    "01101110": "n",
    "01101111": "o",
    "01110000": "p",
    "01110001": "q",
    "01110010": "r",
    "01110011": "s",
    "01110100": "t",
    "01110101": "u",
    "01110110": "v",
    "01110111": "w",
    "01111000": "x",
    "01111001": "y",
    "01111010": "z",
}

OCTAL_DICT = {
    "101": "A",
    "102": "B",
    "103": "C",
    "104": "D",
    "105": "E",
    "106": "F",
    "107": "G",
    "110": "H",
    "111": "I",
    "112": "J",
    "113": "K",
    "114": "L",
    "115": "M",
    "116": "N",
    "117": "O",
    "120": "P",
    "121": "Q",
    "122": "R",
    "123": "S",
    "124": "T",
    "125": "U",
    "126": "V",
    "127": "W",
    "130": "X",
    "131": "Y",
    "132": "Z",
    "141": "a",
    "142": "b",
    "143": "c",
    "144": "d",
    "145": "e",
    "146": "f",
    "147": "g",
    "150": "h",
    "151": "i",
    "152": "j",
    "153": "k",
    "154": "l",
    "155": "m",
    "156": "n",
    "157": "o",
    "160": "p",
    "161": "q",
    "162": "r",
    "163": "s",
    "164": "t",
    "165": "u",
    "166": "v",
    "167": "w",
    "170": "x",
    "171": "y",
    "172": "z",
}

DECIMAL_DICT = {
    "65": "A",
    "66": "B",
    "67": "C",
    "68": "D",
    "69": "E",
    "70": "F",
    "71": "G",
    "72": "H",
    "73": "I",
    "74": "J",
    "75": "K",
    "76": "L",
    "77": "M",
    "78": "N",
    "79": "O",
    "80": "P",
    "81": "Q",
    "82": "R",
    "83": "S",
    "84": "T",
    "85": "U",
    "86": "V",
    "87": "W",
    "88": "X",
    "89": "Y",
    "90": "Z",
    "97": "a",
    "98": "b",
    "99": "c",
    "100": "d",
    "101": "e",
    "102": "f",
    "103": "g",
    "104": "h",
    "105": "i",
    "106": "j",
    "107": "k",
    "108": "l",
    "109": "m",
    "110": "n",
    "111": "o",
    "112": "p",
    "113": "q",
    "114": "r",
    "115": "s",
    "116": "t",
    "117": "u",
    "118": "v",
    "119": "w",
    "120": "x",
    "121": "y",
    "122": "z",
}


HEX_DICT = {
    "41": "A",
    "42": "B",
    "43": "C",
    "44": "D",
    "45": "E",
    "46": "F",
    "47": "G",
    "48": "H",
    "49": "I",
    "4A": "J",
    "4B": "K",
    "4C": "L",
    "4D": "M",
    "4E": "N",
    "4F": "O",
    "50": "P",
    "51": "Q",
    "52": "R",
    "53": "S",
    "54": "T",
    "55": "U",
    "56": "V",
    "57": "W",
    "58": "X",
    "59": "Y",
    "5A": "Z",
    "61": "a",
    "62": "b",
    "63": "c",
    "64": "d",
    "65": "e",
    "66": "f",
    "67": "g",
    "68": "h",
    "69": "i",
    "6A": "j",
    "6B": "k",
    "6C": "l",
    "6D": "m",
    "6E": "n",
    "6F": "o",
    "70": "p",
    "71": "q",
    "72": "r",
    "73": "s",
    "74": "t",
    "75": "u",
    "76": "v",
    "77": "w",
    "78": "x",
    "79": "y",
    "7A": "z",
}

def ascii_encode(text):
    encoded = {"Binary": [], "Decimal": [], "Octal": [], "Hex": []}
    for c in text:
        encoded["Binary"].append(bin(ord(c))[2:].zfill(8))
        encoded["Decimal"].append(str(ord(c)))
        encoded["Octal"].append(oct(ord(c))[2:])
        encoded["Hex"].append(hex(ord(c))[2:])

    for key in encoded:
        encoded[key] = " ".join(encoded[key])

    return encoded

def ascii_decode(text):
    decoded_chars = []
    for part in text.split():
        if part in BINARY_DICT:
            decoded_chars.append(BINARY_DICT[part])
        elif part in OCTAL_DICT:
            decoded_chars.append(OCTAL_DICT[part])
        elif part in DECIMAL_DICT:
            decoded_chars.append(DECIMAL_DICT[part])
        elif part in HEX_DICT:
            decoded_chars.append(HEX_DICT[part])
        else:
            return "Invalid ASCII input"

    return "".join(decoded_chars)


def ascii_decode_all(text):
    parts = text.split()
    results = {}

    # Try binary dict
    try:
        decoded_binary = []
        for part in parts:
            if part in BINARY_DICT:
                decoded_binary.append(BINARY_DICT[part])
            else:
                decoded_binary.append("?")
        results["Binary"] = "".join(decoded_binary)
    except Exception:
        results["Binary"] = "Error decoding binary"

    # Try octal dict
    try:
        decoded_octal = []
        for part in parts:
            if part in OCTAL_DICT:
                decoded_octal.append(OCTAL_DICT[part])
            else:
                decoded_octal.append("?")
        results["Octal"] = "".join(decoded_octal)
    except Exception:
        results["Octal"] = "Error decoding octal"

    # Try decimal dict
    try:
        decoded_decimal = []
        for part in parts:
            if part in DECIMAL_DICT:
                decoded_decimal.append(DECIMAL_DICT[part])
            else:
                decoded_decimal.append("?")
        results["Decimal"] = "".join(decoded_decimal)
    except Exception:
        results["Decimal"] = "Error decoding decimal"

    # Try hex dict (case insensitive keys)
    try:
        decoded_hex = []
        for part in parts:
            key = part.upper()
            if key in HEX_DICT:
                decoded_hex.append(HEX_DICT[key])
            else:
                decoded_hex.append("?")
        results["Hex"] = "".join(decoded_hex)
    except Exception:
        results["Hex"] = "Error decoding hex"

    return results
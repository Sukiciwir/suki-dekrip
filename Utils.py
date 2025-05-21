import codecs
import base64
import re
from decoder import (
    vigenere_decode,
    reverse_decode,
    whitespace_decode,
    xor_decode,
    affine_decode,
    substitution_cipher_decode,
    base32_decode,
    url_decode,
    morse_decode,
    ascii_decode,
    caesar_decode,
    atbash_decode,
)

def is_readable(text):
    if not text:
        return False
    printable = sum(1 for c in text if c.isprintable())
    threshold = 0.75 if len(text) < 50 else 0.9
    return printable / len(text) > threshold


# Fungsi untuk menghitung skor kecocokan bahasa Inggris
def score_english(text):
    common_letters = set("ETAOINSHRDLUetoainshrdlu ")
    return sum(1 for ch in text if ch in common_letters) / len(text) * 100

def Cipher_detector(text):
    suggestions = {}

    # Base64
    if len(text) % 4 == 0 and re.fullmatch(r"^[A-Za-z0-9+/=]+$", text):
        try:
            decoded = base64.b64decode(text).decode("utf-8", "ignore")
            if is_readable(decoded):
                if "=" in text:
                    suggestions["Base64"] = 100
                else:
                    suggestions["Base64"] = 95
            else:
                suggestions["Base64"] = 40
        except:
            suggestions["Base64"] = 0

    # Base32
    if len(text) % 8 == 0 and re.fullmatch(r"^[A-Z2-7=]+$", text):
        try:
            decoded = base32_decode(text)
            if is_readable(decoded) and score_english(decoded) > 40:
                if "=" in text:
                    suggestions["Base32"] = 100
                else:
                    suggestions["Base32"] = int(score_english(decoded))
            else:
                suggestions["Base32"] = 30
        except:
            suggestions["Base32"] = 0

    # ROT13
    decoded = codecs.decode(text, "rot_13")
    if is_readable(decoded) and score_english(decoded) > 50:
        suggestions["ROT13"] = int(score_english(decoded))
    else:
        suggestions["ROT13"] = 20

    # Morse
    if set(text).issubset({".", "-", " ", "/"}) and len(text) > 5:
        decoded = morse_decode(text)
        if decoded and score_english(decoded) > 40:
            if set(text).issubset({".", "-"}):
                suggestions["Morse"] = 100
            else:
                suggestions["Morse"] = int(score_english(decoded))
        else:
            suggestions["Morse"] = 25

    # ASCII
    parts = text.split()
    if all(part.isdigit() for part in parts) and len(parts) > 1:
        decoded = ascii_decode(text)
        if decoded and is_readable(decoded):
            suggestions["ASCII"] = 100
        else:
            suggestions["ASCII"] = 30

    # Caesar
    if all(c.isalpha() or c.isspace() for c in text):
        best_shift, best_score = best_caesar_shift(text)
        if best_score > 40:
            suggestions["Caesar"] = int(best_score)
        else:
            suggestions["Caesar"] = 30

    # Vigenere (try with key "KEY")
    try:
        decoded = vigenere_decode(text, "KEY")
        if is_readable(decoded) and score_english(decoded) > 40:
            suggestions["Vigenere"] = int(score_english(decoded))
        else:
            suggestions["Vigenere"] = 30
    except:
        suggestions["Vigenere"] = 0

    # Reverse
    decoded = reverse_decode(text)
    if is_readable(decoded) and score_english(decoded) > 40:
        suggestions["Reverse"] = int(score_english(decoded))
    else:
        suggestions["Reverse"] = 25

    # Whitespace
    if set(text).issubset({" ", "\t"}):
        suggestions["Whitespace"] = 100
    else:
        decoded = whitespace_decode(text)
        if is_readable(decoded) and score_english(decoded) > 40:
            suggestions["Whitespace"] = int(score_english(decoded))
        else:
            suggestions["Whitespace"] = 20

    # XOR (try with key 42)
    try:
        decoded = xor_decode(text, 42)
        if is_readable(decoded) and score_english(decoded) > 40:
            suggestions["XOR"] = int(score_english(decoded))
        else:
            suggestions["XOR"] = 20
    except:
        suggestions["XOR"] = 0

    # Affine (try with a=5, b=8)
    try:
        decoded = affine_decode(text, 5, 8)
        if is_readable(decoded) and score_english(decoded) > 40:
            suggestions["Affine"] = int(score_english(decoded))
        else:
            suggestions["Affine"] = 20
    except:
        suggestions["Affine"] = 0

    # Substitution cipher (try with identity map)
    try:
        identity_map = {chr(i): chr(i) for i in range(65, 91)}
        decoded = substitution_cipher_decode(text, identity_map)
        if is_readable(decoded) and score_english(decoded) > 40:
            suggestions["Substitution"] = int(score_english(decoded))
        else:
            suggestions["Substitution"] = 20
    except:
        suggestions["Substitution"] = 0

    # URL decode
    try:
        decoded = url_decode(text)
        if is_readable(decoded) and score_english(decoded) > 40:
            if "%" in text and re.search(r"%\d", text):
                suggestions["URL"] = 100
            else:
                suggestions["URL"] = int(score_english(decoded))
        else:
            suggestions["URL"] = 20
    except:
        suggestions["URL"] = 0

    return suggestions

def best_caesar_shift(text):
    best_score = 0
    best_shift = 0
    for shift in range(26):
        decoded = caesar_decode(text, shift)
        score = score_english(decoded)
        if score > best_score:
            best_score = score
            best_shift = shift
    return best_shift, best_score


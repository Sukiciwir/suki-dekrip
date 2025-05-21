import base64
import urllib.parse
import pandas as pd
import streamlit as st 
from morse import * 
from ascii import *


def base64_encode(text):
    return base64.b64encode(text.encode()).decode()


def caesar_encode(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result


def vigenere_encode(text, key):
    result = ""
    key_idx = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
            key_idx += 1
        else:
            result += ch
    return result


def rot13_encode(text):
    return caesar_encode(text, 13)


def atbash_encode(text):
    return "".join(
        chr(155 - ord(c)) if c.isupper() else chr(219 - ord(c)) if c.islower() else c
        for c in text
    )


def reverse_encode(text):
    return text[::-1]


def xor_encode(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)

def url_encode(text):
    return urllib.parse.quote(text)


def base32_encode(text):
    try:
        return base64.b32encode(text.encode()).decode()
    except:
        return "Invalid Base32 input"


def substitution_cipher_encode(text, key_map):
    return "".join(key_map.get(char, char) for char in text)


def affine_encode(text, a, b):
    ciphertext = ""
    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            encoded_char = chr(((a * (ord(char) - base) + b) % 26) + base)
            ciphertext += encoded_char
        else:
            ciphertext += char

    return ciphertext

def base64_decode(text):
    try:
        return base64.b64decode(text).decode()
    except:
        return "Invalid Base64 input"


def vigenere_decode(text, key):
    result = ""
    key_idx = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base - shift) % 26 + base)
            key_idx += 1
        else:
            result += ch
    return result


def caesar_decode(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base - shift) % 26 + base)
        else:
            result += ch
    return result


def rot13_decode(text):
    return caesar_decode(text, 13)


def reverse_decode(text):
    return text[::-1]


def atbash_decode(text):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr(base + 25 - (ord(ch) - base))
        else:
            result += ch
    return result


def whitespace_decode(cipher):
    binary_string = ""
    i = 0

    while i < len(cipher):
        if cipher[i] == " " and (i + 1 < len(cipher) and cipher[i + 1] == " "):
            binary_string += "1"
            i += 2
        elif cipher[i] == " ":
            binary_string += "0"
            i += 1
        elif cipher[i] == "\t":
            binary_string += "1"
            i += 1
        else:
            i += 1

    def binary_to_text(binary_string):
        plaintext = ""
        for i in range(0, len(binary_string), 8):
            chunk = binary_string[i : i + 8]
            if len(chunk) == 8:
                plaintext += chr(int(chunk, 2))
        return plaintext

    return binary_to_text(binary_string)

def xor_decode(text, key):
    try:
        return "".join(chr(ord(c) ^ key) for c in text)
    except:
        return "Error in XOR decoding"


def caesar_bruteforce(text):
    return [f"Shift {i}: {caesar_decode(text, i)}" for i in range(1, 26)]


def vigenere_bruteforce(text):
    return ["Brute-force not implemented yet."]


def xor_bruteforce(text):
    return [f"Key {i}: {xor_decode(text, i)}" for i in range(1, 256)]


def bruteforce_rot(txt):
    results = []
    for key in range(1, 26):
        rotate = str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            "".join(
                (
                    chr((ord(char) - key - 65) % 26 + 65)
                    if char.isupper()
                    else (
                        chr((ord(char) - key - 97) % 26 + 97)
                        if char.islower()
                        else (
                            chr((ord(char) - key - 48) % 10 + 48)
                            if char.isnumeric()
                            else char
                        )
                    )
                )
                for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            ),
        )
        results.append(f"Key {key}: {txt.translate(rotate)}")
    return results


def magic_decode(text):
    results = {}

    decoders = {
        "Base64": base64_decode,
        "ROT13": rot13_decode,
        "Reverse": reverse_decode,
        "Atbash": atbash_decode,
        "Whitespace": whitespace_decode,
        "ASCII": ascii_decode,
        "Morse": morse_decode,
    }

    for name, func in decoders.items():
        try:
            results[name] = func(text)
        except Exception as e:
            results[name] = f"Error: {str(e)}"

    try:
        results["XOR (key=42)"] = xor_decode(text, 42)
    except Exception as e:
        results["XOR (key=42)"] = f"Error: {str(e)}"

    try:
        results["Caesar (shift=3)"] = caesar_decode(text, 3)
    except Exception as e:
        results["Caesar (shift=3)"] = f"Error: {str(e)}"

    try:
        results["Vigenère (key=KEY)"] = vigenere_decode(text, "KEY")
    except Exception as e:
        results["Vigenère (key=KEY)"] = f"Error: {str(e)}"

    return results


def affine_decode(text, a, b):
    plaintext = ""
    try:
        a_inv = pow(a, -1, 26)  # Modular inverse of 'a'
    except ValueError:
        return "Nilai 'a' tidak memiliki inverse mod 26"

    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            decoded_char = chr((a_inv * ((ord(char) - base - b) % 26)) + base)
            plaintext += decoded_char
        else:
            plaintext += char

    return plaintext


def substitution_cipher_decode(text, key_map):
    reverse_map = {v: k for k, v in key_map.items()}
    return "".join(reverse_map.get(char, char) for char in text)


def substitution_key_input():
    """
    Displays a table input for substitution cipher key mapping.
    Returns a dictionary mapping plain characters to coded characters.
    """
    st.write("Masukkan pasangan karakter dalam tabel berikut:")
    import pandas as pd

    # Initialize dataframe with 26 rows for letters A-Z
    df = pd.DataFrame(
        {"Plain Item": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), "Coded Item": [""] * 26}
    )

    edited_df = st.data_editor(
        df, num_rows="dynamic", key="substitution_key_map_editor"
    )

    key_map = {}
    if edited_df is not None:
        for _, row in edited_df.iterrows():
            k = str(row["Plain Item"]).strip()
            v = str(row["Coded Item"]).strip()
            if len(k) == 1 and len(v) == 1:
                key_map[k] = v

    return key_map


def base32_decode(text):
    try:
        return base64.b32decode(text).decode()
    except:
        return "Invalid Base32 input"


def url_decode(text):
    try:
        return urllib.parse.unquote(text)
    except:
        return "Invalid URL input"
    


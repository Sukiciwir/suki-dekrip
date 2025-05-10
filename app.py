import streamlit as st
import base64
from string import ascii_uppercase, ascii_lowercase

# Fungsi Enkripsi
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
    return ''.join(chr(155 - ord(c)) if c.isupper() else chr(219 - ord(c)) if c.islower() else c for c in text)

def reverse_encode(text):
    return text[::-1]

def xor_encode(text, key):
    return ''.join(chr(ord(c) ^ key) for c in text)

# Fungsi Deteksi Otomatis
def is_readable(text):
    if not text:
        return False
    printable = sum(1 for c in text if c.isprintable())
    return printable / len(text) > 0.9

def score_english(text):
    common_letters = set("ETAOINSHRDLUetoainshrdlu ")
    return sum(1 for ch in text if ch in common_letters) / len(text) * 100

def Cipher_detector(text):
    suggestions = {}

    # Base64
    try:
        if len(text) % 4 == 0 and all(c in base64.b64encode(b'A').decode() for c in text.replace('=', '')):
            decoded = base64_decode(text)
            if is_readable(decoded):
                suggestions["Base64"] = 95
            else:
                suggestions["Base64"] = 40
        else:
            suggestions["Base64"] = 10
    except:
        suggestions["Base64"] = 0

    # ROT13
    try:
        decoded = rot13_decode(text)
        if is_readable(decoded) and score_english(decoded) > 50:
            suggestions["ROT13"] = int(score_english(decoded))
        else:
            suggestions["ROT13"] = 20
    except:
        suggestions["ROT13"] = 0

    # Morse
    try:
        if set(text).issubset({'.', '-', ' ', '/'}):
            decoded = morse_decode(text)
            if decoded and score_english(decoded) > 40:
                suggestions["Morse"] = int(score_english(decoded))
            else:
                suggestions["Morse"] = 25
        else:
            suggestions["Morse"] = 5
    except:
        suggestions["Morse"] = 0

    # ASCII
    try:
        parts = text.split()
        if all(part.isdigit() for part in parts) and len(parts) > 1:
            decoded = ascii_decode(text)
            if decoded and is_readable(decoded):
                suggestions["ASCII"] = 85
            else:
                suggestions["ASCII"] = 30
        else:
            suggestions["ASCII"] = 10
    except:
        suggestions["ASCII"] = 0

    # Caesar-like
    try:
        if all(c.isalpha() or c.isspace() for c in text):
            best_score = 0
            for shift in range(1, 26):
                decoded = caesar_decode(text, shift)
                score = score_english(decoded)
                if score > best_score:
                    best_score = score
            if best_score > 40:
                suggestions["Caesar"] = int(best_score)
            else:
                suggestions["Caesar"] = 30
        else:
            suggestions["Caesar"] = 15
    except:
        suggestions["Caesar"] = 0

    # Atbash
    try:
        decoded = atbash_decode(text)
        if is_readable(decoded) and score_english(decoded) > 40:
            suggestions["Atbash"] = int(score_english(decoded))
        else:
            suggestions["Atbash"] = 25
    except:
        suggestions["Atbash"] = 0

    # XOR (brute-force sederhana)
    try:
        decoded = xor_decode(text, 42)
        if is_readable(decoded) and score_english(decoded) > 40:
            suggestions["XOR"] = int(score_english(decoded))
        else:
            suggestions["XOR"] = 20
    except:
        suggestions["XOR"] = 0

    return suggestions

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


def whitespace_decode(text):
    return "Whitespaces removed: " + "".join(text.split())


def ascii_decode(text):
    try:
        return " ".join(chr(int(c)) for c in text.split())
    except:
        return "Invalid ASCII input"


def morse_decode(text):
    MORSE_CODE_DICT = {
        ".-": "A",
        "-...": "B",
        "-.-.": "C",
        "-..": "D",
        ".": "E",
        "..-.": "F",
        "--.": "G",
        "....": "H",
        "..": "I",
        ".---": "J",
        "-.-": "K",
        ".-..": "L",
        "--": "M",
        "-.": "N",
        "---": "O",
        ".--.": "P",
        "--.-": "Q",
        ".-.": "R",
        "...": "S",
        "-": "T",
        "..-": "U",
        "...-": "V",
        ".--": "W",
        "-..-": "X",
        "-.--": "Y",
        "--..": "Z",
        "-----": "0",
        ".----": "1",
        "..---": "2",
        "...--": "3",
        "....-": "4",
        ".....": "5",
        "-....": "6",
        "--...": "7",
        "---..": "8",
        "----.": "9",
    }
    return "".join(MORSE_CODE_DICT.get(code, "") for code in text.split(" "))


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

# === Pengaturan Halaman Streamlit ===
st.set_page_config(
    page_title="🧩 Suki Encoder & Decoder",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto :wght@400;700&display=swap');
    html, body, .main, .stApp {
    background-color: transparent !important;
    color: #A7D8FF !important;
    }
    /* Background Animasi Gradien Biru Futuristik */
    body {
        margin: 0;
        padding: 0;
        background: linear-gradient(-45deg, #001f3d, #003366, #0066cc, #0099ff);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #A7D8FF;
        font-family: 'Roboto', sans-serif;
        background-attachment: fixed;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main {
        backdrop-filter: blur(8px);
        background-color: rgba(0, 0, 50, 0.6);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(0, 100, 255, 0.3);
    }
    h1, h2, h3 {
        color: #00bfff;
        text-shadow: 0 0 5px #0077cc;
        transition: all 0.3s ease-in-out;
    }
    h1:hover {
        transform: scale(1.05);
    }
    .stSelectbox label, .stTextInput label, .stCheckbox label {
        color: #00bfff !important;
        font-weight: bold;
    }
    .stTextInput {
        transition: all 0.3s ease;
    }
    .stTextInput.hidden {
        opacity: 0;
        max-height: 0;
        pointer-events: none;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #004e8c;
        color: white;
        border-radius: 8px;
        border: 2px solid #0077cc;
        padding: 10px;
        transition: border 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00bfff;
        box-shadow: 0 0 5px #00bfff;
    }
    .stButton button {
        background-color: #006bb6;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #0099ff;
        transform: scale(1.05);
    }
    .result-box {
        background-color: rgba(0, 51, 102, 0.8);
        padding: 15px;
        border-left: 5px solid #00bfff;
        margin-top: 10px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 191, 255, 0.2);
    }
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #00bfff, transparent);
        margin: 30px 0;
    }
    .key-input {
    transition: all 0.3s ease;
    }
    .key-input.hidden {
        opacity: 0;
        max-height: 0;
        overflow: hidden;
        pointer-events: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# JavaScript Interaktif
st.markdown(
    """
<script>
document.addEventListener("DOMContentLoaded", function() {
    // Particle Effect
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '-1';
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;
    const particles = [];
    for (let i = 0; i < 100; i++) {
        particles.push({
            x: Math.random() * w,
            y: Math.random() * h,
            radius: Math.random() * 2 + 1,
            vx: -0.5 + Math.random(),
            vy: -0.5 + Math.random()
        });
    }
    function draw() {
        ctx.clearRect(0, 0, w, h);
        ctx.fillStyle = '#00bfff';
        for (let p of particles) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2);
            ctx.fill();
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > w) p.vx *= -1;
            if (p.y < 0 || p.y > h) p.vy *= -1;
        }
        requestAnimationFrame(draw);
    }
    draw();

    // Toggle Input Key
    function toggleKeyInput(show) {
        const keyInput = document.querySelector('.key-input');
        if (show) {
            keyInput.classList.remove('hidden');
        } else {
            keyInput.classList.add('hidden');
        }
    }

    const decoderSelect = document.querySelector('.stSelectbox input');
    const modeRadios = document.querySelectorAll('input[name="Mode"]');
    
    function updateKeyVisibility() {
        const selectedDecoder = decoderSelect.value.trim().toLowerCase();
        const selectedMode = document.querySelector('input[name="Mode"]:checked').value;

        if (selectedMode === "Decrypt" && ["cipher_detector", "magic"].includes(selectedDecoder)) {
            toggleKeyInput(false);
        } else if (["caesar", "vigenere", "xor"].includes(selectedDecoder)) {
            toggleKeyInput(true);
        } else {
            toggleKeyInput(false);
        }
    }

    decoderSelect.addEventListener('change', updateKeyVisibility);
    modeRadios.forEach(radio => radio.addEventListener('change', updateKeyVisibility));
    updateKeyVisibility();
});
</script>
""",
    unsafe_allow_html=True,
)

# Gambar Furina
furina_image = "./furina.png"
st.image(furina_image, caption="Gaskan bang !!", width=200)

# Judul
st.title("🧩 Suki Encoder & Decoder")

# Mode Pemilihan
mode = st.radio("Mode:", ["Encrypt", "Decrypt"], horizontal=True)

# Tentukan daftar decoder berdasarkan mode
if mode == "Decrypt":
    decoder_list = [
        "Cipher_detector",
        "Magic",
        "Base64",
        "Vigenere",
        "Caesar",
        "ROT13",
        "Reverse",
        "Atbash",
        "Whitespace",
        "ASCII",
        "Morse",
        "XOR",
    ]
else:
    decoder_list = [
        "Base64",
        "Vigenere",
        "Caesar",
        "ROT13",
        "Reverse",
        "Atbash",
        "XOR",
    ]

decoder = st.selectbox("Pilih Cipher:", decoder_list)

# Upload File
uploaded_file = st.file_uploader("📁 Upload File Cipher Text (.txt)", type=["txt"])
cipher_text = ""
if uploaded_file is not None:
    cipher_text = uploaded_file.read().decode("utf-8")
    cipher_text = st.text_area('Masukkan Cipher Text:', cipher_text, height=200)
else:
    cipher_text = st.text_area('Masukkan Cipher Text:', placeholder="Contoh: Hello / U2FsdGVkX1+...", height=200)

# Key Input
key = None
if decoder in ["Caesar", "Vigenere", "XOR"]:
    key = st.text_input("Masukkan Key (jika tersedia):", key="key_input")

# Brute Force
brute_force = st.checkbox("Gunakan Brute Force (jika tersedia)")

# Inisialisasi session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Tombol Proses
if st.button("Proses", key="process_button"):
    result = None

    if mode == "Encrypt":
        if decoder == "Base64":
            result = base64_encode(cipher_text)
        elif decoder == "Caesar" and key and key.isdigit():
            result = caesar_encode(cipher_text, int(key))
        elif decoder == "Vigenere" and key:
            result = vigenere_encode(cipher_text, key)
        elif decoder == "ROT13":
            result = rot13_encode(cipher_text)
        elif decoder == "Atbash":
            result = atbash_encode(cipher_text)
        elif decoder == "Reverse":
            result = reverse_encode(cipher_text)
        elif decoder == "XOR" and key and key.isdigit():
            result = xor_encode(cipher_text, int(key))
        else:
            result = "Parameter tidak valid untuk enkripsi ini."
    else:
        if decoder == "Cipher_detector":
            st.subheader("🔍 Hasil Deteksi Otomatis")
            suggestions = Cipher_detector(cipher_text)
            for cipher_name, percent in sorted(suggestions.items(), key=lambda x: x[1], reverse=True):
                st.markdown(f"- [{percent}%] {cipher_name}")
            if suggestions:
                top_guess = max(suggestions.items(), key=lambda x: x[1])[0]
                st.info(f"💡 Rekomendasi: Coba gunakan cipher '{top_guess}' untuk decrypt.")
            result = "\n".join([f"[{v}%] {k}" for k, v in suggestions.items()])
                
        elif decoder == "Magic":
            results = magic_decode(cipher_text)
            for method, output in results.items():
                st.subheader(f"🔍 {method}")
                st.code(output)
            result = "\n".join([f"[{k}]: {v}" for k, v in results.items()])

        # Tambahkan logika dekripsi untuk semua cipher lain
        elif decoder == "Base64":
            result = base64_decode(cipher_text)
        elif decoder == "Vigenere":
            if brute_force:
                result_list = vigenere_bruteforce(cipher_text)
                for res in result_list:
                    st.code(res)
                result = "\n".join(result_list)
            elif key:
                result = vigenere_decode(cipher_text, key)
            else:
                result = "Key harus diisi untuk Vigenère Cipher."
        elif decoder == "Caesar":
            if brute_force:
                result_list = caesar_bruteforce(cipher_text)
                for res in result_list:
                    st.code(res)
                result = "\n".join(result_list)
            elif key and key.isdigit():
                result = caesar_decode(cipher_text, int(key))
            else:
                result = "Key Caesar harus angka."
        elif decoder == "ROT13":
            result = rot13_decode(cipher_text)
        elif decoder == "Reverse":
            result = reverse_decode(cipher_text)
        elif decoder == "Atbash":
            result = atbash_decode(cipher_text)
        elif decoder == "Whitespace":
            result = whitespace_decode(cipher_text)
        elif decoder == "ASCII":
            result = ascii_decode(cipher_text)
        elif decoder == "Morse":
            result = morse_decode(cipher_text)
        elif decoder == "XOR":
            if brute_force:
                result_list = xor_bruteforce(cipher_text)
                for res in result_list:
                    st.code(res)
                result = "\n".join(result_list)
            elif key and key.isdigit():                     
                result = xor_decode(cipher_text, int(key))
            else:
                result = "Key XOR harus angka."
        else:
            result = "Decoder tidak dikenali."    

    if result:
        st.session_state.history.append({
            "decoder": f"{mode}: {decoder}",
            "input": cipher_text[:50] + ("..." if len(cipher_text) > 50 else ""),
            "output": str(result)[:100] + ("..." if len(str(result)) > 100 else "")
        })

    if isinstance(result, str):
        st.code(f"### Hasil:\n{result}")
        if "Error" in result or "Invalid" in result:
            st.error("❌ Gagal memproses.")
        else:
            st.success("✅ Berhasil diproses!")
            st.download_button(
                label="💾 Simpan Hasil",
                data=result,
                file_name=f"suki_{mode.lower()}_hasil.txt",
                mime="text/plain"
            )

# Riwayat
with st.expander("📜 Riwayat Operasi"):
    for item in reversed(st.session_state.history[-5:]):
        st.text(f"[{item['decoder']}] {item['input']} → {item['output']}")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#00bfff;'>Made with sigma by <strong>Suki</strong> | Powered by Streamlit | *There are still many bugs, you can report on my insta</p>",
    unsafe_allow_html=True,
)

import streamlit as st
import base64
from string import ascii_uppercase, ascii_lowercase


# === Deklarasi fungsi decode sederhana untuk demo ===
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
    page_title="Suki Decoder",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# === CSS Styling ===
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto :wght@400;700&display=swap');
    
    html, body, .main, .stApp {
    background-color: transparent !important;
    color: #A7D8FF !important;
    }

    /* Animasi Loading */
    .loader {
        --w: 10ch;
        font-weight: bold;
        font-family: monospace;
        font-size: 30px;
        letter-spacing: var(--w);
        width: var(--w);
        overflow: hidden;
        white-space: nowrap;
        color: #0000;
        animation: l40 2s infinite;
    }

    .loader:before {
        content: "Loading...";
    }

    @keyframes l40 {
        0%, 100% {
            text-shadow:
                calc(0 * var(--w)) 0 #000,
                calc(-1 * var(--w)) 0 #000,
                calc(-2 * var(--w)) 0 #000,
                calc(-3 * var(--w)) 0 #000,
                calc(-4 * var(--w)) 0 #000,
                calc(-5 * var(--w)) 0 #000,
                calc(-6 * var(--w)) 0 #000,
                calc(-7 * var(--w)) 0 #000,
                calc(-8 * var(--w)) 0 #000,
                calc(-9 * var(--w)) 0 #000;
        }
        9% {
            text-shadow:
                calc(0 * var(--w)) 0 #000,
                calc(-1 * var(--w)) 0 #000,
                calc(-2 * var(--w)) -20px transparent,
                calc(-3 * var(--w)) 0 #000,
                calc(-4 * var(--w)) 0 #000,
                calc(-5 * var(--w)) 0 #000,
                calc(-6 * var(--w)) 0 #000,
                calc(-7 * var(--w)) 0 #000,
                calc(-8 * var(--w)) 0 #000,
                calc(-9 * var(--w)) 0 #000;
        }
        18% {
            text-shadow:
                calc(0 * var(--w)) 0 #000,
                calc(-1 * var(--w)) 0 #000,
                calc(-2 * var(--w)) -20px transparent,
                calc(-3 * var(--w)) 0 #000,
                calc(-4 * var(--w)) 0 #000,
                calc(-5 * var(--w)) 0 #000,
                calc(-6 * var(--w)) -20px transparent,
                calc(-7 * var(--w)) 0 #000,
                calc(-8 * var(--w)) 0 #000,
                calc(-9 * var(--w)) 0 #000;
        }
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
    </style>
    """,
    unsafe_allow_html=True,
)

# === JavaScript Efek Partikel & Loader ===
st.markdown(
    """
<script>
document.addEventListener("DOMContentLoaded", function() {
    // === Particle Effect ===
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

    // === Toggle Input Key ===
    function toggleKeyInput(show) {
        const keyInput = document.querySelector('.key-input');
        if (show) {
            keyInput.classList.remove('hidden');
        } else {
            keyInput.classList.add('hidden');
        }
    }

    const decoderSelect = document.querySelector('.stSelectbox input');
    decoderSelect.addEventListener('change', function() {
        const selectedDecoder = this.value;
        if (selectedDecoder === 'Caesar' || selectedDecoder === 'Vigenere' || selectedDecoder === 'XOR') {
            toggleKeyInput(true);
        } else {
            toggleKeyInput(false);
        }
    });

    toggleKeyInput(%s);

    // === Loader Animation ===
    const loader = document.querySelector('.loader');
    const decodeButton = document.querySelector('.stButton button');

    function toggleLoader(show) {
        loader.style.display = show ? 'block' : 'none';
    }

    toggleLoader(true);

    decoderSelect.addEventListener('change', () => toggleLoader(false));
    decodeButton.addEventListener('click', () => toggleLoader(false));
});
</script>
"""
    % (
        "true"
        if st.session_state.get("decoder", "") in ["Caesar", "Vigenere", "XOR"]
        else "false"
    ),
    unsafe_allow_html=True,
)

# === Tampilkan Loader Saat Pertama Load ===
# st.markdown('<div class="loader"></div>', unsafe_allow_html=True)

# Gambar Furina
furina_image = "./furina.png"
st.image(furina_image, caption="Gaskan bang !!", width=200)

# Judul
st.title("🧩 Suki Decoder")

# Inisialisasi session state
if "decoder" not in st.session_state:
    st.session_state.decoder = "Base64"

# Form Input
decoder = st.selectbox(
    "Pilih Decoder:",
    [
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
        "Magic",
    ],
)

# Di bagian form input
uploaded_file = st.file_uploader("📁 Upload File Cipher Text (.txt)", type=["txt"])
if uploaded_file is not None:
    cipher_text = uploaded_file.read().decode("utf-8")
    st.text_area('Masukkan Cipher Text:', cipher_text, height=200)
else:
    cipher_text = st.text_area('Masukkan Cipher Text:')

# Simpan pilihan decoder ke session state
st.session_state.decoder = decoder

key = None
if decoder in ["Caesar", "Vigenere", "XOR"]:
    key = st.text_input("Masukkan Key (jika tersedia):")

brute_force = st.checkbox("Gunakan Brute Force (jika tersedia)")

# Inisialisasi session_state.history jika belum ada
if 'history' not in st.session_state:
    st.session_state.history = []

# Tampilkan riwayat di bawah footer atau sebelum tombol decode
with st.expander("📜 Riwayat Decode"):
    for item in st.session_state.history[-5:]:
        st.text(f"[{item['decoder']}] {item['input']} → {item['output']}")

# Tombol Decode
st.markdown("<hr>", unsafe_allow_html=True)

if st.button("🔓 Decode", key="decode_button"):
    result = None  # Inisialisasi awal

    if decoder == "Base64":
        result = base64_decode(cipher_text)
        st.code(f"### Hasil:\n{result}")

    elif decoder == "Vigenere":
        if brute_force:
            result = vigenere_bruteforce(cipher_text)
            for res in result:
                st.code(res)
            result = "\n".join(result)  # Untuk riwayat, jadikan string
        elif key:
            result = vigenere_decode(cipher_text, key)
            st.code(f"### Hasil:\n{result}")
        else:
            result = "Key harus diisi untuk Vigenère Cipher."
            st.warning(result)

    elif decoder == "Caesar":
        if brute_force:
            result = caesar_bruteforce(cipher_text)
            for res in result:
                st.code(res)
            result = "\n".join(result)
        elif key and key.isdigit():
            result = caesar_decode(cipher_text, int(key))
            st.code(f"### Hasil:\n{result}")
        else:
            result = "Key Caesar harus angka."
            st.warning(result)

    elif decoder == "ROT13":
        result = rot13_decode(cipher_text)
        st.code(f"### Hasil:\n{result}")

    elif decoder == "Reverse":
        result = reverse_decode(cipher_text)
        st.code(f"### Hasil:\n{result}")

    elif decoder == "Atbash":
        result = atbash_decode(cipher_text)
        st.code(f"### Hasil:\n{result}")

    elif decoder == "Whitespace":
        result = whitespace_decode(cipher_text)
        st.code(f"### Hasil:\n{result}")

    elif decoder == "ASCII":
        result = ascii_decode(cipher_text)
        st.code(f"### Hasil:\n{result}")

    elif decoder == "Morse":
        result = morse_decode(cipher_text)
        st.code(f"### Hasil:\n{result}")

    elif decoder == "XOR":
        if brute_force:
            result_list = xor_bruteforce(cipher_text)
            for res in result_list:
                st.code(res)
            result = "\n".join(result_list)
        elif key and key.isdigit():
            result = xor_decode(cipher_text, int(key))
            st.code(f"### Hasil:\n{result}")
        else:
            result = "Key XOR harus angka."
            st.warning(result)
    elif decoder == "Magic":
        results = magic_decode(cipher_text)

        for method, output in results.items():
            st.subheader(f"🔍 {method}")
            st.code(output)
        
        result = "\n\n".join([f"[{k}]\n{v}" for k, v in results.items()])


    # Setelah decode selesai, simpan ke history
    if result is not None:
        st.session_state.history.append({
            "decoder": decoder,
            "input": cipher_text[:50] + ("..." if len(cipher_text) > 50 else ""),
            "output": str(result)[:100] + ("..." if len(str(result)) > 100 else "")
        })

    # Tampilkan notifikasi sukses/error
    if isinstance(result, str):
        if result.startswith("Invalid") or result.startswith("Error"):
            st.error("❌ Gagal mendecode. Periksa input Anda.")
        elif result.strip() != "":
            st.success("✅ Berhasil mendecode!")

    # Tombol download
    if isinstance(result, str) and result.strip() != "" and not result.startswith("Key harus diisi"):
        st.download_button(
            label="💾 Simpan Hasil",
            data=result,
            file_name="suki_decoder_hasil.txt",
            mime="text/plain"
        )
    

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#00bfff;'>Made with 💙 by <strong>Suki</strong> | Powered by Streamlit</p>",
    unsafe_allow_html=True,
)

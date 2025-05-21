import streamlit as st
from string import ascii_uppercase, ascii_lowercase
from decoder import *
from ascii import *
from Utils import *
from morse import *


st.set_page_config(
    page_title="Suki enkripsi",
    page_icon="./furina.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS
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

# JS
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

    // Add Enter key listener to trigger "Proses" button click
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.innerText.toLowerCase().includes('proses')) {
                    btn.click();
                    break;
                }
            }
        }
    });
});
</script>
""",
    unsafe_allow_html=True,
)


furina_image = "./furina.png"
st.image(furina_image, caption="Gaskan bang !!", width=200)
st.title("Suki Encoder & Decoder")

# Mode
mode = st.radio("Mode:", ["Encrypt", "Decrypt"], horizontal=True)

# List Decoder
if mode == "Decrypt":
    decoder_list = [
        "Affine",
        "ASCII",
        "Atbash",
        "Base32",
        "Base64",
        "Caesar",
        "Cipher_detector",
        "Magic",
        "Morse",
        "Reverse",
        "ROT13",
        "Substitution",
        "URL",
        "Vigenere",
        "Whitespace",
        "XOR",
    ]
else:
    decoder_list = [
        "Affine",
        "ASCII",
        "Atbash",
        "Base32",
        "Base64",
        "Caesar",
        "Morse",
        "Reverse",
        "ROT13",
        "Substitution",
        "URL",
        "Vigenere",
        "Whitespace",
        "XOR",
    ]

decoder = st.selectbox("Pilih Cipher:", decoder_list)

# Upload File
uploaded_file = st.file_uploader("📁 Upload File Cipher Text (.txt)", type=["txt"])
cipher_text = ""
if uploaded_file is not None:
    cipher_text = uploaded_file.read().decode("utf-8")
    cipher_text = st.text_area("Masukkan Cipher Text:", cipher_text, height=200)
else:
    cipher_text = st.text_area(
        "Masukkan Cipher Text:",
        placeholder="Contoh: Hello / U2FsdGVkX1+...",
        height=200,
    )

# Key Input
key = None
key_map = None
if decoder in ["Caesar", "Vigenere", "XOR"]:
    key = st.text_input(
        "Masukkan Key (jika tersedia):", key=f"key_input_{decoder.lower()}"
    )
elif decoder == "Substitution":
    # Show substitution key input table only when decoder is Substitution
    key_map = substitution_key_input()
elif decoder == "Affine":
    a = st.number_input("Masukkan nilai 'a':", min_value=1)
    b = st.number_input("Masukkan nilai 'b':", min_value=0)

# Brute Force
brute_force = False
if decoder in ["Caesar", "ROT13", "XOR"]:
    brute_force = st.checkbox("Gunakan Brute Force (Jika sudah muak) ")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Proses", key="process_button"):
    result = None

    if mode == "Encrypt":
        if decoder == "Base64":
            result = base64_encode(cipher_text)
        elif decoder == "Caesar" and key and key.isdigit():
            result = caesar_encode(cipher_text, int(key))
        elif decoder == "Affine":
            result = affine_encode(cipher_text, a, b)
        elif decoder == "Base32":
            result = base32_encode(cipher_text)
            if result == "Invalid Base32 input":
                result = "Parameter tidak valid untuk Base32 enkripsi ini."
        elif decoder == "URL":
            result = url_encode(cipher_text)
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
        elif decoder == "Morse":
            result = morse_encode(cipher_text)
        elif decoder == "ASCII":
            encoded = ascii_encode(cipher_text)
            result_lines = []
            for format_type, values in encoded.items():
                result_lines.append(f"{format_type}: {values}")
            result = "\n".join(result_lines)
        elif decoder == "Substitution" and key_map:
            result = substitution_cipher_encode(cipher_text, key_map)
        else:
            result = "Parameter tidak valid untuk enkripsi ini."
    else:
        if decoder == "Cipher_detector":
            st.subheader("🔍 Hasil Deteksi Otomatis")
            suggestions = Cipher_detector(cipher_text)
            sorted_suggestions = sorted(
                suggestions.items(), key=lambda x: x[1], reverse=True
            )
            for cipher_name, percent in sorted_suggestions[:3]:
                st.markdown(f"- [{percent}%] {cipher_name}")
            if suggestions:
                top_guess = sorted_suggestions[0][0]
                st.info(
                    f"💡 Rekomendasi: Coba gunakan cipher '{top_guess}' untuk decrypt."
                )
            result = "\n".join([f"[{v}%] {k}" for k, v in sorted_suggestions[:3]])

        elif decoder == "Magic":
            results = magic_decode(cipher_text)
            for method, output in results.items():
                st.subheader(f"🔍 {method}")
                st.code(output)
            result = "\n".join([f"[{k}]: {v}" for k, v in results.items()])

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
            if brute_force:
                result_list = bruteforce_rot(cipher_text)
                for res in result_list:
                    st.code(res)
                result = "\n".join(result_list)
        elif decoder == "Reverse":
            result = reverse_decode(cipher_text)
        elif decoder == "Atbash":
            result = atbash_decode(cipher_text)
        elif decoder == "Affine":
            result = affine_decode(cipher_text, a, b)
        elif decoder == "Base32":
            result = base32_decode(cipher_text)
        elif decoder == "URL":
            result = url_decode(cipher_text)
        elif decoder == "Whitespace":
            result = whitespace_decode(cipher_text)
        elif decoder == "ASCII":
            ascii_results = ascii_decode_all(cipher_text)
            for fmt, output in ascii_results.items():
                st.subheader(f"ASCII Decode using {fmt} Dictionary")
                st.code(output)
            result = "\n".join(
                [f"{fmt}: {output}" for fmt, output in ascii_results.items()]
            )
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
        elif decoder == "Substitution":
            if key_map:
                result = substitution_cipher_decode(cipher_text, key_map)
            else:
                result = "Key Substitution harus diisi."
        else:
            result = "Decoder tidak dikenali."

    if result:
        st.session_state.history.append(
            {
                "decoder": f"{mode}: {decoder}",
                "input": cipher_text[:50] + ("..." if len(cipher_text) > 50 else ""),
                "output": str(result)[:100] + ("..." if len(str(result)) > 100 else ""),
            }
        )

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
                mime="text/plain",
            )

with st.expander("📜 Riwayat Operasi"):
    for item in reversed(st.session_state.history[-5:]):
        st.text(f"[{item['decoder']}] {item['input']} → {item['output']}")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <p style='text-align:center; color:#00bfff;'>
        Made with sigma by <strong>Suki</strong> | Powered by Streamlit | *this tools still have many bugs, please report to @ewrzqi*<br>
        <a href="https://github.com/Sukiciwir/suki-dekrip" target="_blank" style="color:#00bfff; text-decoration:none;">
            <svg height="24" width="24" viewBox="0 0 16 16" version="1.1" aria-hidden="true" fill="#00bfff" style="vertical-align: middle;">
                <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.65 7.65 0 012 0c1.53-1.03 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            &nbsp;GitHub
        </a>
    </p>
    """,
    unsafe_allow_html=True,
)

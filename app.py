import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
import pandas as pd
import urllib.parse
from youtube_transcript_api import YouTubeTranscriptApi
import re

# ==========================================
# 1. PENGATURAN HALAMAN (MOBILE OPTIMIZED)
# ==========================================
st.set_page_config(page_title="GOD MODE AI App", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ API Key belum dipasang di Streamlit Secrets!")
    st.stop()

# ==========================================
# 2. NAVIGASI SIDEBAR (10 MENU DEWA)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6873/6873405.png", width=80)
    st.markdown("### ⚡ GOD MODE v8.0")
    menu = st.radio("Pilih Fitur:",[
        "💘 AI Wingman (Romance)",   # <--- FITUR BARU KITA TARUH PALING ATAS!
        "💬 Chatbot Pintar", 
        "📺 YouTube Summarizer",   
        "🎙️ Telinga & Mata AI",      
        "🎬 AI Clipper (Gang Vibe)",
        "🎨 AI Image Studio",        
        "🗣️ Super Slang Translator",
        "📚 Chat with PDF",          
        "📊 Data Analyst (CSV)",
        "📝 Asisten Penulis"
    ])
    st.markdown("---")
    st.caption("The Casanova Update 🌹")

st.title(menu)

# ==========================================
# 3. LOGIKA FITUR
# ==========================================

# ------------------------------------------
# 💘 AI WINGMAN (KHUSUS INTROVERT) - FITUR BARU!
# ------------------------------------------
if menu == "💘 AI Wingman (Romance)":
    st.markdown("#### 🕶️ Asisten PDKT & Dating Coach (Anti-Jomblo)")
    st.write("Rahasia buat cowok introvert! Dapatkan contekan balasan chat, cara buka obrolan elegan, dan mindset *High-Value Gentleman* biar doi baper.")
    
    # Bikin 3 Sub-Menu pakai Tab biar rapi di HP
    tab_chat, tab_ice, tab_curhat = st.tabs(["📱 Balesin Chat Doi", "🧊 Buka Obrolan", "🧘‍♂️ Tanya Suhu"])
    
    with tab_chat:
        st.write("**Bingung mau bales apa? Biar AI yang mikir!**")
        chat_doi = st.text_area("Paste chat terakhir dari doi di sini:", "Wkwkwk iya nih, lagi bosen banget di rumah ga ngapa-ngapain.")
        
        if st.button("Bantuin Bales Bro! 🚀"):
            with st.spinner("Meracik balasan paling Rizz..."):
                prompt = f"""Lu adalah seorang 'Dating Coach' dan 'Wingman' jenius spesialis ngebantu cowok introvert.
                Gebetan user ngechat seperti ini: '{chat_doi}'.
                Tugas lu: Berikan 3 opsi balasan menggunakan bahasa Indonesia gaul/santai (gue/lu/aku/kamu tergantung konteks).
                1. Opsi Lucu/Humor (Bikin dia ketawa atau penasaran).
                2. Opsi Flirty Halus (Elegan, tarik-ulur, ga murahan).
                3. Opsi Cool/Misterius (Santai, ga keliatan ngarep/simp).
                Jelaskan juga sedikit kenapa balasan tersebut bagus secara psikologi."""
                res = model.generate_content(prompt).text
                st.success("Ini contekan lu, gas kirim! 🥶")
                st.info(res)

    with tab_ice:
        st.write("**Cara elegan mulai obrolan (Anti nanya 'Lagi ngapain?')**")
        konteks = st.text_input("Info tentang doi:", "Contoh: Dia suka kucing, anak indie, temen sekelas tapi jarang ngobrol.")
        
        if st.button("Generate Topik 💬"):
            with st.spinner("Mencari celah obrolan..."):
                prompt = f"""Lu adalah Wingman buat cowok introvert. User mau nge-chat cewek dengan info: '{konteks}'.
                Buatkan 5 kalimat pembuka (ice breaker) yang asik, natural, ga *creepy*, dan memancing cewek itu buat cerita panjang. Hindari pertanyaan klise kayak 'lagi apa' atau 'udah makan belum'. Pakai bahasa gaul santai."""
                res = model.generate_content(prompt).text
                st.success("Pilih satu dan langsung chat dia! 🎯")
                st.write(res)

    with tab_curhat:
        st.write("**Konsultasi Mindset, Cara Nge-Date, & Baca Kode Cewek**")
        curhat = st.text_area("Apa yang mau lu tanyain/curhatin?", "Gimana cara ngajak jalan cewek yang baru gue kenal 3 hari dari IG tanpa keliatan freak? Sama gimana cara ngetreat dia pas ketemu nanti?")
        
        if st.button("Minta Pencerahan Suhu 🧘‍♂️"):
            with st.spinner("Membaca psikologi wanita..."):
                prompt = f"""Lu adalah Dating Coach profesional. Jawab curhatan cowok introvert ini dengan sangat praktis, manjur, step-by-step, dan menampar realita (tapi suportif). 
                Ajarkan dia cara bersikap maskulin, gentleman, tidak *simp* (mengemis cinta), dan cara men-treat wanita dengan hormat tapi tetap punya *value* tinggi. 
                Curhatannya: '{curhat}'"""
                res = model.generate_content(prompt).text
                st.info(res)

# ------------------------------------------
# 💬 CHATBOT PINTAR
# ------------------------------------------
elif menu == "💬 Chatbot Pintar":
    col1, col2 = st.columns([3, 1])
    with col1: st.markdown("#### 🤖 Asisten Pribadi Lu")
    with col2:
        if st.button("🗑️ Hapus Chat"):
            st.session_state.messages =[]
            st.toast("Riwayat chat dibersihkan!", icon="🧹")
            st.rerun()

    if "messages" not in st.session_state: st.session_state.messages =[]
    if len(st.session_state.messages) > 20: st.session_state.messages = st.session_state.messages[-20:]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Tanya apa aja..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Berpikir..."):
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-6:]])
                res = model.generate_content(f"Riwayat:\n{history}\n\nBalas: {prompt}").text
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})

# ------------------------------------------
# 📺 YOUTUBE SUMMARIZER
# ------------------------------------------
elif menu == "📺 YouTube Summarizer":
    st.markdown("#### 🎥 Malas Nonton Video Panjang? Biar AI yang nonton!")
    yt_url = st.text_input("Paste Link YouTube di sini:", placeholder="https://www.youtube.com/watch?v=...")
    if st.button("Ekstrak & Ringkas 🚀"):
        if yt_url:
            with st.spinner("Mengekstrak subtitle video..."):
                try:
                    video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", yt_url).group(1)
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['id', 'en'])
                    teks_yt = " ".join([t['text'] for t in transcript_list])[:15000] 
                    res = model.generate_content(f"Buatkan ringkasan lengkap dari transkrip berikut:\n\n{teks_yt}").text
                    st.success("Berhasil dirangkum!")
                    st.info(res)
                except Exception as e:
                    st.error("Gagal! Pastikan videonya punya Subtitle (CC).")

# ------------------------------------------
# 🎙️ TELINGA & MATA AI
# ------------------------------------------
elif menu == "🎙️ Telinga & Mata AI":
    st.markdown("#### 👁️ Menganalisis Gambar & Suara")
    jenis_file = st.radio("Pilih tipe file:",["📸 Gambar (JPG/PNG)", "🎵 Audio/Voice Note (MP3/WAV)"])
    if "Gambar" in jenis_file:
        file = st.file_uploader("Upload Foto", type=["jpg", "png", "jpeg"])
        prompt_user = st.text_input("Instruksi AI:", "Jelaskan gambar ini.")
        if file and st.button("Scan 🔍"):
            with st.spinner("Memindai..."):
                res = model.generate_content([prompt_user, Image.open(file)]).text
                st.write(res)
    else:
        file = st.file_uploader("Upload Audio (Maks 10MB)", type=["mp3", "wav", "m4a"])
        prompt_user = st.text_input("Instruksi AI:", "Buatkan ringkasan dari rekaman ini.")
        if file and st.button("Dengarkan 🎧"):
            with st.spinner("Mendengarkan..."):
                audio_data = {"mime_type": file.type, "data": file.getvalue()}
                res = model.generate_content([prompt_user, audio_data]).text
                st.write(res)

# ------------------------------------------
# 📚 CHAT WITH PDF
# ------------------------------------------
elif menu == "📚 Chat with PDF":
    st.markdown("#### 📑 Tanya Jawab sama Dokumen")
    pdf_file = st.file_uploader("Upload PDF (Maks 10 halaman awal)", type=["pdf"])
    if pdf_file:
        with st.spinner("Membaca PDF..."):
            reader = PyPDF2.PdfReader(pdf_file)
            teks_pdf = "".join([reader.pages[i].extract_text() for i in range(min(len(reader.pages), 10))])
        st.success("✅ PDF berhasil masuk ke otak AI!")
        pertanyaan_pdf = st.text_input("Tanyakan sesuatu:", "Apa kesimpulan utama dari dokumen ini?")
        if st.button("Tanyakan 💬"):
            with st.spinner("Mencari jawaban..."):
                res = model.generate_content(f"Gunakan teks ini untuk menjawab.\n\nDokumen:\n{teks_pdf}\n\nPertanyaan: {pertanyaan_pdf}").text
                st.info(res)

# ------------------------------------------
# 🎨 AI IMAGE STUDIO
# ------------------------------------------
elif menu == "🎨 AI Image Studio":
    st.markdown("#### 🖼️ Bikin Gambar Aesthetic")
    deskripsi = st.text_area("Deskripsi Gambar:", "Mobil sport retro di jalanan neon tokyo saat hujan")
    rasio = st.selectbox("Ukuran:",["9:16 (Tiktok)", "16:9 (YouTube)", "1:1 (Square)"])
    if st.button("Generate Gambar 🪄"):
        with st.spinner("Menggambar..."):
            prompt_eng = model.generate_content(f"Translate to English: {deskripsi}").text.strip()
            safe_prompt = urllib.parse.quote(prompt_eng)
            width, height = (720, 1280) if "9:16" in rasio else (1280, 720) if "16:9" in rasio else (1080, 1080)
            st.image(f"https://image.pollinations.ai/prompt/{safe_prompt}?width={width}&height={height}&nologo=true", use_container_width=True)

# ------------------------------------------
# 🎬 AI CLIPPER (GANG VIBE)
# ------------------------------------------
elif menu == "🎬 AI Clipper (Gang Vibe)":
    st.markdown("#### 🎥 Sutradara Editan Jalanan")
    bahan = st.text_area("Video mentah lu tentang apa?", "Klip IShowSpeed lagi lompat.")
    vibe = st.selectbox("Vibe:",["Memphis Phonk", "UK Drill", "Opium / Playboi Carti"])
    lagu = st.text_input("Lagu:", "Yeat - Monëy so big")
    if st.button("Drop The Sauce! 🩸"):
        with st.spinner("Meracik editan..."):
            res = model.generate_content(f"Give a step-by-step editing blueprint in Indonesian slang for a '{vibe}' style edit. Topic: '{bahan}'. Song: '{lagu}'.").text
            st.info(res)

# ------------------------------------------
# 🗣️ SUPER SLANG TRANSLATOR
# ------------------------------------------
elif menu == "🗣️ Super Slang Translator":
    st.markdown("#### 🌍 Ahli Bahasa Jalanan")
    teks = st.text_area("Teks Biasa:", "Ayo kita nongkrong bro.")
    aksen = st.selectbox("Target Slang:",["AAVE (African American)", "UK Roadman", "Gen-Z Brainrot", "Indo Anak Jaksel"])
    if st.button("Translate 🔄"):
        with st.spinner("Translating..."):
            res = model.generate_content(f"Translate and adapt this text into authentic '{aksen}' slang. Text: '{teks}'.").text
            st.info(res)

# ------------------------------------------
# 📊 DATA ANALYST (CSV) & 📝 ASISTEN PENULIS
# ------------------------------------------
elif menu == "📊 Data Analyst (CSV)":
    st.markdown("#### 📈 Ilmuwan Data Otomatis")
    csv_file = st.file_uploader("Upload File .csv", type=["csv"])
    if csv_file:
        df = pd.read_csv(csv_file)
        st.dataframe(df.head(), use_container_width=True)
        if st.button("Analisis 📉"):
            res = model.generate_content(f"Berikan 3 wawasan dari data ini:\n{df.head(50).to_csv(index=False)}").text
            st.write(res)

elif menu == "📝 Asisten Penulis":
    st.markdown("#### ✍️ Copywriter AI")
    topik = st.text_area("Topik", "Naskah video tiktok fakta psikologi.")
    style = st.selectbox("Gaya Bahasa",["Gaul/Santai", "Profesional", "Persuasif"])
    if st.button("Generate 🚀"):
        res = model.generate_content(f"Buat tulisan bahasa Indonesia gaya {style} tentang: {topik}").text
        st.write(res)

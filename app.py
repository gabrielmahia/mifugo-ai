import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Mifugo AI — Mshauri wa Mifugo", page_icon="🐄", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0e08;color:#e8f5e9}
.mv-card{background:#0d1f0d;border:1px solid #2e7d32;border-radius:10px;padding:14px 18px;margin:8px 0}
.stButton>button{background:#388e3c;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")
SYSTEM = """Wewe ni daktari wa mifugo na mshauri wa kilimo Kenya. Jibu kwa Kiswahili rahisi.
Toa ushauri wa vitendo kuhusu: magonjwa, dawa, lishe, uzalishaji, soko.
Kama hali ni ya dharura ya mifugo, sema mkulima apige simu daktari wa mifugo mara moja.
Toa makadirio ya bei za soko Kenya kwa wakati huu."""

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.3,"maxOutputTokens":700}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown("# 🐄 Mifugo AI")
st.markdown("**Mshauri wa Mifugo kwa Wakulima Kenya**")
tab1,tab2,tab3,tab4 = st.tabs(["🏥 Magonjwa","💰 Bei za Soko","🌾 Lishe na Malisho","💊 Dawa za Mifugo"])

with tab1:
    animal = st.selectbox("Mnyama:", ["Ng'ombe","Mbuzi","Kondoo","Ngamia","Nguruwe","Kuku","Bata"])
    symp = st.text_area("Elezea dalili:", placeholder="Mfano: Ng'ombe wangu ana mwili moto, hawakuli na wanatoa mate mengi...", height=100)
    if st.button("🔍 Gundua", key="d_btn") and symp:
        with st.spinner("..."): result = ask(f"{animal} — Dalili: {symp}. Nini kinaweza kuwa? Jinsi ya kutibu?")
        st.markdown(f'<div class="mv-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    county = st.selectbox("Kaunti:", ["Nairobi","Nakuru","Kajiado","Narok","Laikipia","Marsabit","Turkana"])
    animal2 = st.selectbox("Mnyama:", ["Ng'ombe (grade)","Ng'ombe (local)","Mbuzi","Kondoo","Nguruwe"], key="a2")
    if st.button("📊 Angalia Bei", key="p_btn"):
        with st.spinner("..."): result = ask(f"Bei za soko za {animal2} katika {county} Kenya sasa hivi. Toa bei ya kununua na kuuza kwa kilo/kichwa.")
        st.markdown(f'<div class="mv-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    stage = st.selectbox("Hatua:", ["Ndama / Watoto","Kukomaa","Uzalishaji wa maziwa","Uzalishaji wa nyama","Uja uzito"])
    animal3 = st.selectbox("Mnyama:", ["Ng'ombe","Mbuzi","Kondoo"], key="a3")
    if st.button("🌾 Pata Ushauri wa Lishe", key="f_btn"):
        with st.spinner("..."): result = ask(f"Lishe sahihi ya {animal3} katika hatua ya {stage} Kenya. Toa: Chakula, Malisho, Maji, Ziada za lishe, Gharama za makadirio")
        st.markdown(f'<div class="mv-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab4:
    disease = st.text_input("Ugonjwa au dalili:", placeholder="Mfano: FMD, ECF, Newcastle...")
    if st.button("💊 Tafuta Dawa", key="m_btn") and disease:
        with st.spinner("..."): result = ask(f"Dawa inayotumiwa kutibu {disease} kwa mifugo Kenya. Toa: Jina la dawa, Kipimo, Jinsi ya kutoa, Tahadhari, Bei ya makadirio")
        st.markdown(f'<div class="mv-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🐄 Mifugo AI v1.0 | Dharura: Piga daktari wa mifugo | Maelezo ya DVS Kenya | CC BY-NC-ND 4.0")

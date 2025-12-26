import streamlit as st

# -------------------------
# CONFIG PAGINA
# -------------------------
st.set_page_config(
    page_title="Prompt Builder",
    page_icon="🧠",
    layout="centered",
)

# -------------------------
# PWA / iOS HOME ICON (HEAD INJECTION)
# -------------------------
PWA_HEAD = """
<link rel="manifest" href="/static/manifest.json">

<!-- Favicon classico -->
<link rel="icon" type="image/png" sizes="32x32" href="/static/icon-192.png">

<!-- iOS: icona quando fai "Aggiungi a Home" -->
<link rel="apple-touch-icon" sizes="180x180" href="/static/icon-180.png">

<!-- iOS: modalità app (standalone) -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Prompt Builder">

<!-- Colore barra / UI -->
<meta name="theme-color" content="#0b0b10">
"""

st.markdown(PWA_HEAD, unsafe_allow_html=True)

# -------------------------
# UI APP
# -------------------------
st.title("🧠 Prompt Builder")
st.caption("Crea prompt più chiari, completi e riutilizzabili — senza impazzire.")

with st.expander("⚙️ Impostazioni", expanded=True):
    lingua = st.selectbox("Lingua del prompt", ["Italiano", "English"], index=0)
    stile = st.selectbox("Stile output", ["Chiaro e pratico", "Tecnico", "Creativo", "Sintetico"], index=0)
    formato = st.selectbox("Formato risposta", ["Testo", "Elenco puntato", "Tabella", "Passi numerati"], index=0)
    tono = st.selectbox("Tono", ["Neutro", "Amichevole", "Professionale", "Ironico"], index=1)
    lunghezza = st.selectbox("Lunghezza", ["Breve", "Media", "Dettagliata"], index=1)

st.divider()

obiettivo = st.text_area(
    "🎯 Cosa vuoi ottenere dall'AI?",
    placeholder="Esempio: Voglio un piano marketing per un negozio di stampa 3D con budget ridotto..."
)

contesto = st.text_area(
    "🧩 Contesto utile (opzionale)",
    placeholder="Esempio: target Italia, budget 200€/mese, canali Instagram/TikTok, obiettivo lead..."
)

vincoli = st.text_area(
    "⛔ Vincoli / Requisiti (opzionale)",
    placeholder="Esempio: niente ads, solo organico; evita gergo troppo tecnico; includi esempi..."
)

input_dati = st.text_area(
    "📎 Dati / Materiali da usare (opzionale)",
    placeholder="Esempio: elenco prodotti, prezzi, USP, link, testo descrizione..."
)

st.divider()

def build_prompt():
    lang_map = {
        "Italiano": "Italiano",
        "English": "English"
    }

    prompt = []
    if lingua == "Italiano":
        prompt.append("Agisci come un assistente esperto di prompt engineering.")
        prompt.append(f"Stile: {stile}. Tono: {tono}. Lunghezza: {lunghezza}. Formato: {formato}.")
        prompt.append("")
        prompt.append("OBIETTIVO:")
        prompt.append(obiettivo.strip() if obiettivo.strip() else "-")
        prompt.append("")
        prompt.append("CONTESTO:")
        prompt.append(contesto.strip() if contesto.strip() else "-")
        prompt.append("")
        prompt.append("VINCOLI / REQUISITI:")
        prompt.append(vincoli.strip() if vincoli.strip() else "-")
        prompt.append("")
        prompt.append("DATI / MATERIALI DA USARE:")
        prompt.append(input_dati.strip() if input_dati.strip() else "-")
        prompt.append("")
        prompt.append("ISTRUZIONI FINALI:")
        prompt.append("1) Se mancano informazioni, fai prima 3-7 domande mirate.")
        prompt.append("2) Poi produci la risposta finale nel formato richiesto.")
    else:
        prompt.append("Act as an expert prompt-engineering assistant.")
        prompt.append(f"Style: {stile}. Tone: {tono}. Length: {lunghezza}. Format: {formato}.")
        prompt.append("")
        prompt.append("GOAL:")
        prompt.append(obiettivo.strip() if obiettivo.strip() else "-")
        prompt.append("")
        prompt.append("CONTEXT:")
        prompt.append(contesto.strip() if contesto.strip() else "-")
        prompt.append("")
        prompt.append("CONSTRAINTS / REQUIREMENTS:")
        prompt.append(vincoli.strip() if vincoli.strip() else "-")
        prompt.append("")
        prompt.append("DATA / MATERIALS TO USE:")
        prompt.append(input_dati.strip() if input_dati.strip() else "-")
        prompt.append("")
        prompt.append("FINAL INSTRUCTIONS:")
        prompt.append("1) If info is missing, ask 3-7 targeted questions first.")
        prompt.append("2) Then produce the final answer in the requested format.")

    return "\n".join(prompt)

col1, col2 = st.columns([1, 1])
with col1:
    genera = st.button("✨ Genera prompt", use_container_width=True)
with col2:
    pulisci = st.button("🧹 Pulisci", use_container_width=True)

if pulisci:
    st.rerun()

if genera:
    if not obiettivo.strip():
        st.warning("Scrivi almeno l’obiettivo: senza quello l’AI va in vacanza 😄")
    else:
        prompt_finale = build_prompt()
        st.subheader("📌 Prompt pronto da copiare")
        st.code(prompt_finale, language="markdown")
        st.download_button(
            "⬇️ Scarica prompt (.txt)",
            data=prompt_finale.encode("utf-8"),
            file_name="prompt_builder.txt",
            mime="text/plain",
            use_container_width=True
        )

st.caption("Tip: dopo aver cambiato icona su iPhone, elimina la vecchia icona dalla Home e aggiungi di nuovo.")

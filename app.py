import streamlit as st

# --- CONFIG BASE ---
st.set_page_config(
    page_title="🧠 Prompt Builder",
    page_icon="🧠",
    layout="centered"
)

# --- META TAG PER iOS (ADD TO HOME SCREEN) ---
st.markdown(
    """
    <head>
        <link rel="apple-touch-icon" sizes="180x180" href="assets/icon-180.png">
        <link rel="apple-touch-icon" sizes="192x192" href="assets/icon-192.png">
        <link rel="apple-touch-icon" sizes="512x512" href="assets/icon-512.png">

        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="Prompt Builder">
    </head>
    """,
    unsafe_allow_html=True
)

# --- UI ---
st.title("🧠 Prompt Builder")
st.subheader("Crea prompt efficaci per qualsiasi AI")

st.markdown("### 🎯 Seleziona il contesto")
contesto = st.selectbox(
    "Tipo di utilizzo",
    ["Scrittura", "Programmazione", "Marketing", "Studio", "Altro"]
)

st.markdown("### 📝 Descrivi cosa vuoi ottenere")
obiettivo = st.text_area("Obiettivo", placeholder="Es: scrivere un post LinkedIn virale...")

st.markdown("### ⚙️ Livello di dettaglio")
dettaglio = st.slider("Quanto deve essere dettagliato?", 1, 5, 3)

if st.button("🚀 Genera Prompt"):
    prompt = f"""
Agisci come un esperto di {contesto}.
Obiettivo: {obiettivo}

Livello di dettaglio richiesto: {dettaglio}/5.
Rispondi in modo chiaro, strutturato e pratico.
"""
    st.markdown("### ✅ Prompt generato")
    st.code(prompt)

import streamlit as st
st.set_page_config(
    page_title="🧠 Prompt Builder",
    page_icon="assets/icon-192.png",
    layout="centered"
)
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Universal Prompt Builder v2", page_icon="🚀", layout="wide")

# --- INIZIALIZZAZIONE CRONOLOGIA ---
if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

st.title("🚀 Universal Prompt Builder + History")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configurazione")
    mode = st.selectbox(
        "Modalità Prompt",
        ["📝 Testo/Generico", "📸 Foto (Image Gen)", "🎬 Video", "💻 Codice/Dev"]
    )
    
    st.divider()
    if st.button("🗑️ Cancella Cronologia"):
        st.session_state.prompt_history = []
        st.rerun()

# --- LAYOUT INPUT (Semplificato per brevità, usa la logica precedente) ---
col1, col2 = st.columns(2)
with col1:
    main_input = st.text_area("🎯 Obiettivo principale / Soggetto", placeholder="Cosa vuoi ottenere?")
    role_or_style = st.text_input("🎭 Ruolo / Stile artistico", placeholder="Es: Senior Dev o Fotorealismo")
with col2:
    context_or_tech = st.text_area("🧩 Dettagli tecnici / Contesto", placeholder="Vincoli, lenti, librerie...")
    format_or_ratio = st.text_input("📦 Formato / Aspect Ratio", placeholder="Es: Tabella, 16:9, JSON")

# --- GENERAZIONE ---
if st.button("✨ Genera e Salva in Cronologia", use_container_width=True):
    # Logica di costruzione semplificata per l'esempio
    timestamp = datetime.now().strftime("%H:%M:%S")
    final_prompt = f"MODO: {mode}\nRUOLO/STILE: {role_or_style}\nOBIETTIVO: {main_input}\nDETTAGLI: {context_or_tech}\nFORMATO: {format_or_ratio}"
    
    # Salvataggio nello stato della sessione
    st.session_state.prompt_history.insert(0, {
        "Ora": timestamp,
        "Tipo": mode,
        "Prompt": final_prompt
    })

# --- VISUALIZZAZIONE RISULTATO CORRENTE ---
if st.session_state.prompt_history:
    st.divider()
    st.subheader("📌 Ultimo Prompt Generato")
    latest_prompt = st.session_state.prompt_history[0]["Prompt"]
    st.code(latest_prompt, language="markdown")
    
    # Pulsante per simulare invio API
    if st.button("🔌 Invia a OpenAI/Claude (Mock)"):
        st.info("Connessione API in fase di configurazione. Inserisci la tua API Key nei segreti.")

# --- SEZIONE CRONOLOGIA ---
st.divider()
st.subheader("📜 Cronologia Sessione")
if st.session_state.prompt_history:
    df_history = pd.DataFrame(st.session_state.prompt_history)
    st.table(df_history)
else:
    st.write("Nessun prompt generato finora.")

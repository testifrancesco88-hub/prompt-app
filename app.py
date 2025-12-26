import streamlit as st
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Prompt Builder",
    page_icon="🧠",
    layout="centered",
)

# --- INIEZIONE META TAG PER IOS (PWA) ---
# Sostituisci questo URL con quello reale della tua icona se il percorso è diverso
ICON_URL = "https://raw.githubusercontent.com/testifrancesco88-hub/prompt-app/main/assets/icon-180.png"

def inject_pwa_meta():
    pwa_html = f"""
    <link rel="apple-touch-icon" sizes="180x180" href="{ICON_URL}">
    <link rel="icon" type="image/png" sizes="192x192" href="{ICON_URL}">
    
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="PromptBuilder">
    
    <style>
        /* Nasconde elementi superflui per un look più pulito */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .stDeployButton {{display:none;}}
    </style>
    """
    st.markdown(pwa_html, unsafe_allow_html=True)

inject_pwa_meta()

# --- LOGICA DEL PROMPT ---
def generate_prompt(role, goal, context, constraints):
    return f"RUOLO: {role}\n\nOBIETTIVO: {goal}\n\nCONTESTO: {context}\n\nVINCOLI: {constraints}"

# --- INTERFACCIA ---
st.title("🧠 Prompt Builder")
st.write("Genera prompt professionali e installa l'app sul tuo iPhone.")

with st.container():
    role = st.text_input("🎭 Ruolo dell'AI", "Esperto Senior")
    goal = st.text_area("🎯 Obiettivo", placeholder="Cosa deve fare l'AI?")
    context = st.text_area("🧩 Contesto", placeholder="Dati o background utili...")
    constraints = st.text_area("⛓️ Vincoli", placeholder="Es: max 200 parole, tono amichevole...")

if st.button("✨ Genera", use_container_width=True):
    if goal:
        final_prompt = generate_prompt(role, goal, context, constraints)
        st.subheader("📌 Prompt Generato:")
        st.code(final_prompt, language="markdown")
        
        st.download_button(
            label="⬇️ Scarica (.txt)",
            data=final_prompt,
            file_name=f"prompt_{datetime.now().strftime('%H%M')}.txt",
            use_container_width=True
        )
    else:
        st.warning("Inserisci almeno l'obiettivo!")

st.divider()
st.info("📲 **Istruzioni per iPhone:**\n1. Apri questa pagina in Safari\n2. Clicca l'icona 'Condividi' (quadrato con freccia)\n3. Seleziona **'Aggiungi alla schermata Home'**")

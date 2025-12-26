import base64
import json
from pathlib import Path

import streamlit as st


# -----------------------------
# PWA / iOS ICON INJECTION
# -----------------------------
def _b64_of_file(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode("utf-8")


def inject_ios_icons_and_meta(
    app_name: str = "Prompt Builder",
    theme_color: str = "#E11D48",  # rosso carino
):
    """
    iOS (Add to Home) usa apple-touch-icon nell'HEAD, non il manifest.
    Streamlit non permette di modificare l'HEAD "ufficialmente", ma st.markdown
    con unsafe_allow_html=True funziona per aggiungere i tag necessari.
    """

    assets = Path(__file__).parent / "assets"

    # Usa principalmente 180 per iOS. Mettiamo anche favicon 192/512 per altri.
    icon_180 = assets / "icon-180.png"
    icon_192 = assets / "icon-192.png"
    icon_512 = assets / "icon-512.png"

    missing = [p.name for p in [icon_180, icon_192, icon_512] if not p.exists()]
    if missing:
        st.warning(
            "Mancano alcune icone in assets/: " + ", ".join(missing) +
            " — le icone iOS potrebbero non aggiornarsi."
        )
        return

    b64_180 = _b64_of_file(icon_180)
    b64_192 = _b64_of_file(icon_192)
    b64_512 = _b64_of_file(icon_512)

    # Manifest (utile soprattutto Android/Chrome). iOS lo ignora quasi sempre,
    # ma lo includiamo uguale.
    manifest = {
        "name": app_name,
        "short_name": app_name,
        "start_url": ".",
        "display": "standalone",
        "background_color": theme_color,
        "theme_color": theme_color,
        "icons": [
            {"src": "data:image/png;base64," + b64_192, "sizes": "192x192", "type": "image/png"},
            {"src": "data:image/png;base64," + b64_512, "sizes": "512x512", "type": "image/png"},
        ],
    }
    manifest_b64 = base64.b64encode(json.dumps(manifest).encode("utf-8")).decode("utf-8")

    head_html = f"""
    <meta name="application-name" content="{app_name}">
    <meta name="apple-mobile-web-app-title" content="{app_name}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="{theme_color}">

    <!-- iOS Home Screen Icon (QUESTO è quello che conta davvero) -->
    <link rel="apple-touch-icon" sizes="180x180" href="data:image/png;base64,{b64_180}">

    <!-- Favicons (tab/browser) -->
    <link rel="icon" type="image/png" sizes="192x192" href="data:image/png;base64,{b64_192}">
    <link rel="icon" type="image/png" sizes="512x512" href="data:image/png;base64,{b64_512}">

    <!-- Web Manifest -->
    <link rel="manifest" href="data:application/manifest+json;base64,{manifest_b64}">
    """

    st.markdown(head_html, unsafe_allow_html=True)


# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(
    page_title="🧠 Prompt Builder",
    page_icon="🧠",      # favicon/tab (non basta per iOS Home)
    layout="centered"
)

inject_ios_icons_and_meta(app_name="Prompt Builder", theme_color="#E11D48")


# -----------------------------
# PROMPT BUILDER UI
# -----------------------------
st.title("🧠 Prompt Builder")
st.caption("Costruisci prompt efficaci e riutilizzabili. Zero magia, solo struttura. 😉")

with st.sidebar:
    st.subheader("Impostazioni")
    model_type = st.selectbox("Tipo di AI", ["Chat / LLM", "Immagini", "Codice", "Analisi dati"])
    tone = st.selectbox("Tono", ["Neutro", "Professionale", "Amichevole", "Creativo", "Sintetico"])
    language = st.selectbox("Lingua output", ["Italiano", "English", "Español"])
    length = st.select_slider("Lunghezza risposta", options=["Breve", "Media", "Dettagliata"], value="Media")
    add_examples = st.toggle("Aggiungi esempi", value=True)

st.markdown("### 1) Descrivi cosa vuoi ottenere")
goal = st.text_area(
    "Obiettivo",
    placeholder="Es: Voglio un piano di allenamento di 4 settimane per principianti, 3 giorni a settimana…",
    height=110
)

st.markdown("### 2) Dai contesto (opzionale ma potentissimo)")
context = st.text_area(
    "Contesto",
    placeholder="Es: Ho 30 anni, poco tempo, attrezzatura minima, obiettivo dimagrimento…",
    height=110
)

st.markdown("### 3) Vincoli e preferenze")
constraints = st.text_area(
    "Vincoli",
    placeholder="Es: max 500 parole, elenco puntato, includi tabelle, evita gergo, cita fonti…",
    height=110
)

st.markdown("### 4) Input / dati che l’AI deve usare (opzionale)")
inputs = st.text_area(
    "Dati / Input",
    placeholder="Es: qui incollo un testo, una tabella, un elenco di prodotti, ecc.",
    height=110
)

def build_prompt():
    lang_map = {"Italiano": "italiano", "English": "english", "Español": "español"}
    ln = lang_map.get(language, "italiano")

    sections = []

    # Ruolo/sistema leggero (senza spaventare l’AI 😄)
    if model_type == "Immagini":
        sections.append("Sei un assistente specializzato nel creare descrizioni (prompt) per modelli di generazione immagini.")
    elif model_type == "Codice":
        sections.append("Sei un assistente esperto di programmazione. Produci soluzioni corrette, sicure e spiegate con chiarezza.")
    elif model_type == "Analisi dati":
        sections.append("Sei un assistente esperto di analisi dati. Ragioni in modo strutturato e verifichi assunzioni e calcoli.")
    else:
        sections.append("Sei un assistente utile e preciso. Fai domande solo se indispensabile; altrimenti fai ipotesi ragionevoli e dichiarale.")

    sections.append(f"Scrivi la risposta in {ln}. Tono: {tone}. Lunghezza: {length}.")

    if goal.strip():
        sections.append(f"OBIETTIVO:\n{goal.strip()}")
    if context.strip():
        sections.append(f"CONTESTO:\n{context.strip()}")
    if inputs.strip():
        sections.append(f"DATI / INPUT DA USARE:\n{inputs.strip()}")
    if constraints.strip():
        sections.append(f"VINCOLI:\n{constraints.strip()}")

    if add_examples:
        sections.append(
            "FORMATO RISPOSTA:\n"
            "- Usa titoli e punti elenco quando utile.\n"
            "- Se fai assunzioni, scrivile esplicitamente.\n"
            "- Se mancano dati cruciali, elenca massimo 3 domande mirate alla fine."
        )

    return "\n\n---\n\n".join(sections)


col1, col2 = st.columns([1, 1])
with col1:
    generate = st.button("✨ Genera prompt", use_container_width=True)
with col2:
    clear = st.button("🧹 Pulisci campi", use_container_width=True)

if clear:
    st.session_state.clear()
    st.rerun()

if generate:
    prompt = build_prompt()
    st.markdown("## Prompt pronto da copiare")
    st.code(prompt, language="markdown")

    st.download_button(
        "⬇️ Scarica prompt (.txt)",
        data=prompt.encode("utf-8"),
        file_name="prompt_builder.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown("---")
st.caption("Tip: se l’icona su iPhone non cambia, elimina l’app dalla Home e aggiungila di nuovo (iOS cachea forte).")

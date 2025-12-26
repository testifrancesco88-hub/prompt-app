import base64
import json
import time
from pathlib import Path

import streamlit as st

APP_NAME = "🧠 Prompt Builder"
APP_SHORT = "Prompt Builder"

# Cambia questa stringa ogni volta che vuoi forzare l'aggiornamento icone su iPhone
# (es: "v3", "2025-12-26-2", ecc.)
ASSET_VERSION = "v3"

ASSETS_DIR = Path(__file__).parent / "assets"
ICON_180 = ASSETS_DIR / "icon-180.png"   # iOS home screen
ICON_192 = ASSETS_DIR / "icon-192.png"   # android/manifest
ICON_512 = ASSETS_DIR / "icon-512.png"   # android/manifest
ICON_1024 = ASSETS_DIR / "icon-1024.png" # fallback high-res

st.set_page_config(
    page_title=APP_SHORT,
    page_icon="🧠",
    layout="wide",
)

def _b64_data_uri(p: Path) -> str:
    if not p.exists():
        return ""
    b = p.read_bytes()
    b64 = base64.b64encode(b).decode("utf-8")
    return f"data:image/png;base64,{b64}"

def inject_pwa_head():
    """
    Inietta:
    - apple-touch-icon (quella che iPhone usa per 'Aggiungi a Home')
    - favicon
    - manifest
    - meta PWA base
    - (opzionale) service worker registration (solo se in futuro metti un sw.js servibile)
    """
    icon180_uri = _b64_data_uri(ICON_180) or _b64_data_uri(ICON_1024)
    icon192_uri = _b64_data_uri(ICON_192) or icon180_uri
    icon512_uri = _b64_data_uri(ICON_512) or icon180_uri

    # Manifest in data URI (molti browser lo accettano; iOS comunque si affida soprattutto ad apple-touch-icon)
    manifest = {
        "name": APP_NAME,
        "short_name": APP_SHORT,
        "start_url": ".",
        "scope": ".",
        "display": "standalone",
        "background_color": "#0b0f17",
        "theme_color": "#0b0f17",
        "icons": [
            {"src": icon192_uri, "sizes": "192x192", "type": "image/png"},
            {"src": icon512_uri, "sizes": "512x512", "type": "image/png"},
        ],
    }
    manifest_b64 = base64.b64encode(json.dumps(manifest).encode("utf-8")).decode("utf-8")
    manifest_uri = f"data:application/manifest+json;base64,{manifest_b64}"

    # Cache busting: metto ?v=... anche se sono data-uri (inutile tecnicamente),
    # ma su alcuni dispositivi aiuta a “sporcare” l’URL e ridurre caching weird.
    cb = ASSET_VERSION

    head_html = f"""
    <meta name="application-name" content="{APP_NAME}"/>
    <meta name="apple-mobile-web-app-title" content="{APP_SHORT}"/>
    <meta name="apple-mobile-web-app-capable" content="yes"/>
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>
    <meta name="theme-color" content="#0b0f17"/>

    <link rel="manifest" href="{manifest_uri}?v={cb}">

    <!-- iPhone Home Screen icon (la più importante) -->
    <link rel="apple-touch-icon" sizes="180x180" href="{icon180_uri}?v={cb}">
    <!-- Fallback extra -->
    <link rel="apple-touch-icon" sizes="1024x1024" href="{_b64_data_uri(ICON_1024)}?v={cb}">

    <!-- Favicon -->
    <link rel="icon" type="image/png" sizes="192x192" href="{icon192_uri}?v={cb}">
    <link rel="icon" type="image/png" sizes="512x512" href="{icon512_uri}?v={cb}">

    <style>
      /* Piccolo polish */
      .pb-card {{
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 16px;
        background: rgba(255,255,255,0.02);
      }}
      .muted {{
        opacity: 0.75;
      }}
    </style>

    <script>
      // Niente promesse: questo è solo un helper per debug.
      // iOS spesso cache-a l'icona della Home screen per conto suo.
      console.log("PWA head injected: {cb}");
    </script>
    """
    st.markdown(head_html, unsafe_allow_html=True)

def build_prompt(goal, audience, tone, output_format, constraints, context, examples, language):
    parts = []

    # Ruolo + obiettivo
    parts.append(f"Sei un assistente esperto. Il tuo compito: {goal.strip()}")

    # Pubblico
    if audience.strip():
        parts.append(f"Pubblico/utente finale: {audience.strip()}")

    # Contesto
    if context.strip():
        parts.append("Contesto/Informazioni disponibili:")
        parts.append(context.strip())

    # Tono
    if tone.strip():
        parts.append(f"Tono: {tone.strip()}")

    # Lingua
    if language.strip():
        parts.append(f"Rispondi in: {language.strip()}")

    # Vincoli
    if constraints.strip():
        parts.append("Vincoli e requisiti:")
        parts.append(constraints.strip())

    # Formato output
    if output_format.strip():
        parts.append("Formato di output richiesto:")
        parts.append(output_format.strip())

    # Esempi
    if examples.strip():
        parts.append("Esempi (se utili, imita struttura e livello di dettaglio):")
        parts.append(examples.strip())

    # Chiusura “operativa”
    parts.append("Prima di rispondere, se manca un’informazione critica fai al massimo 3 domande mirate. Altrimenti procedi.")

    return "\n\n".join(parts).strip()

def main():
    inject_pwa_head()

    st.title("🧠 Prompt Builder")
    st.caption("Costruisci prompt chiari, completi e riutilizzabili. (E sì: iPhone deve smettere di mettere l’icona di Streamlit 😄)")

    with st.sidebar:
        st.subheader("Template rapidi")
        template = st.selectbox(
            "Scegli un template",
            ["Custom", "Coding Assistant", "Marketing Copy", "Analisi Dati", "Tutor/Spiegazione", "Prompt per Immagini"],
        )
        st.markdown("---")
        st.write("**Cache-busting icone:**")
        st.code(f"ASSET_VERSION = {ASSET_VERSION}", language="text")
        st.caption("Se l’icona non cambia, incrementa ASSET_VERSION e ridistribuisci.")

    # Default per template
    defaults = {
        "Custom": dict(
            goal="",
            audience="",
            tone="",
            output_format="",
            constraints="",
            context="",
            examples="",
            language="Italiano",
        ),
        "Coding Assistant": dict(
            goal="Scrivi/correggi codice e spiega le scelte in modo pratico",
            audience="Sviluppatore",
            tone="Diretto, tecnico, senza fronzoli",
            output_format="1) Soluzione 2) Spiegazione breve 3) Edge cases",
            constraints="- Non inventare API\n- Se mancano dettagli, chiedi info essenziali\n- Fornisci codice completo eseguibile",
            context="Stack/linguaggio:\nObiettivo:\nVincoli di runtime:\n",
            examples="Input esempio:\n...\nOutput esempio:\n...",
            language="Italiano",
        ),
        "Marketing Copy": dict(
            goal="Scrivi testi marketing ad alta conversione",
            audience="Clienti finali non tecnici",
            tone="Persuasivo, chiaro, non aggressivo",
            output_format="Headline (5 varianti)\nSottotitolo\nBody (2 versioni)\nCTA (5 varianti)",
            constraints="- Evita promesse non verificabili\n- Mantieni frasi brevi\n- Niente superlativi inutili",
            context="Prodotto:\nTarget:\nBenefici:\nObiezioni:\n",
            examples="",
            language="Italiano",
        ),
        "Analisi Dati": dict(
            goal="Analizza dati e proponi insight azionabili",
            audience="Business / manager",
            tone="Chiaro, orientato alle decisioni",
            output_format="Sintesi (bullet)\nCosa significa\nCosa fare dopo\nRischi/limiti",
            constraints="- Se mancano dati, esplicita assunzioni\n- Indica confidenza (bassa/media/alta)",
            context="Dati (tabella o descrizione):\n",
            examples="",
            language="Italiano",
        ),
        "Tutor/Spiegazione": dict(
            goal="Spiega un argomento in modo comprensibile e progressivo",
            audience="Principiante",
            tone="Calmo, incoraggiante",
            output_format="Spiegazione breve\nEsempio\nMini quiz (3 domande)\nSoluzioni",
            constraints="- Evita gergo non spiegato\n- Passi piccoli e verificabili",
            context="Argomento:\nCosa so già:\nObiettivo:\n",
            examples="",
            language="Italiano",
        ),
        "Prompt per Immagini": dict(
            goal="Crea un prompt dettagliato per generare un’immagine coerente",
            audience="Generatore di immagini",
            tone="Descrittivo, preciso",
            output_format="Prompt unico + Negative prompt + 3 varianti",
            constraints="- Specifica soggetto, stile, luci, lente, composizione\n- Evita marchi registrati",
            context="Soggetto:\nStile (es. flat, 3D, foto, anime):\nMood:\nColori:\n",
            examples="",
            language="Italiano",
        ),
    }

    d = defaults.get(template, defaults["Custom"])

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        st.markdown('<div class="pb-card">', unsafe_allow_html=True)
        goal = st.text_area("Obiettivo (cosa vuoi ottenere)", value=d["goal"], height=90, placeholder="Es: Scrivi una landing page per...")
        audience = st.text_input("Audience", value=d["audience"], placeholder="Es: Principianti, CTO, clienti B2C…")
        tone = st.text_input("Tono", value=d["tone"], placeholder="Es: sintetico, amichevole, tecnico…")
        language = st.text_input("Lingua risposta", value=d["language"], placeholder="Es: Italiano")
        context = st.text_area("Contesto / dati di input", value=d["context"], height=140, placeholder="Incolla info, vincoli, dati…")
        constraints = st.text_area("Vincoli / requisiti", value=d["constraints"], height=120, placeholder="- max 200 parole\n- evita gergo\n- cita fonti…")
        output_format = st.text_area("Formato output", value=d["output_format"], height=110, placeholder="Es: tabella + bullet + conclusione…")
        examples = st.text_area("Esempi (opzionale)", value=d["examples"], height=120, placeholder="Esempio input/output…")
        st.markdown("</div>", unsafe_allow_html=True)

        generate = st.button("Genera prompt", type="primary", use_container_width=True)

    with col2:
        st.markdown('<div class="pb-card">', unsafe_allow_html=True)
        st.subheader("Prompt finale")
        st.caption("Copia e incolla nel tuo AI preferito.")
        if generate:
            final_prompt = build_prompt(goal, audience, tone, output_format, constraints, context, examples, language)
            st.session_state["final_prompt"] = final_prompt

        final_prompt = st.session_state.get("final_prompt", "")
        if final_prompt:
            st.code(final_prompt, language="text")
            st.download_button(
                "Scarica .txt",
                data=final_prompt.encode("utf-8"),
                file_name="prompt_builder.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.write("Compila i campi e premi **Genera prompt**.")
            st.caption("Tip: più contesto = meno magia nera, più risultati.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        """
        **Nota icona iPhone (importantissima):** iOS può “incollarsi” all’icona vecchia anche se hai aggiornato tutto.
        Se dopo il deploy vedi ancora Streamlit, fai i passaggi qui sotto.
        """
    )

    with st.expander("Fix icona iPhone: cosa fare se resta Streamlit"):
        st.write("1) **Elimina** l’icona salvata sulla Home (tieni premuto → Rimuovi app).")
        st.write("2) Safari → **Impostazioni iPhone** → Safari → **Cancella dati siti web e cronologia**.")
        st.write("3) Riapri l’URL della tua app, aspetta 2–3 secondi, poi **Condividi → Aggiungi a Home**.")
        st.write("Se ancora niente: incrementa `ASSET_VERSION` (es. v4), fai push su GitHub e ridistribuisci su Render.")

if __name__ == "__main__":
    main()

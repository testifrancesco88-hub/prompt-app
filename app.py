import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


ASSETS_DIR = Path(__file__).parent / "assets"

ICON_180 = ASSETS_DIR / "icon-180.png"
ICON_192 = ASSETS_DIR / "icon-192.png"
ICON_512 = ASSETS_DIR / "icon-512.png"
ICON_1024 = ASSETS_DIR / "icon-1024.png"


def _b64_png(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode("utf-8")


def inject_pwa_head(
    app_name: str = "Prompt Builder",
    theme_color: str = "#111827",
    background_color: str = "#111827",
):
    """
    Inject PWA + iOS icons into <head>.

    IMPORTANT: iOS Home Screen uses apple-touch-icon (180x180) primarily.
    We embed icons as base64 data URIs to avoid static hosting complications.
    """

    missing = [p for p in [ICON_180, ICON_192, ICON_512, ICON_1024] if not p.exists()]
    if missing:
        st.warning(
            "Mancano queste icone nella cartella assets:\n- "
            + "\n- ".join(str(m.name) for m in missing)
        )
        return

    b64_180 = _b64_png(ICON_180)
    b64_192 = _b64_png(ICON_192)
    b64_512 = _b64_png(ICON_512)
    b64_1024 = _b64_png(ICON_1024)

    manifest = {
        "name": app_name,
        "short_name": "Prompt Builder",
        "start_url": "./",
        "display": "standalone",
        "background_color": background_color,
        "theme_color": theme_color,
        "icons": [
            {"src": f"data:image/png;base64,{b64_192}", "sizes": "192x192", "type": "image/png"},
            {"src": f"data:image/png;base64,{b64_512}", "sizes": "512x512", "type": "image/png"},
            {"src": f"data:image/png;base64,{b64_1024}", "sizes": "1024x1024", "type": "image/png"},
        ],
    }

    manifest_json = json.dumps(manifest, ensure_ascii=False)
    manifest_b64 = base64.b64encode(manifest_json.encode("utf-8")).decode("utf-8")
    manifest_data_url = f"data:application/manifest+json;base64,{manifest_b64}"

    # Inject into HEAD
    head_html = f"""
    <script>
      // Avoid duplicate injections on reruns
      (function() {{
        const ID = "pwa-injected-head";
        if (document.getElementById(ID)) return;
        const el = document.createElement("div");
        el.id = ID;
        document.head.appendChild(el);
      }})();
    </script>

    <link rel="manifest" href="{manifest_data_url}">

    <!-- iOS / Safari -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="{app_name}">

    <!-- The one iPhone cares about most for "Add to Home Screen" -->
    <link rel="apple-touch-icon" sizes="180x180" href="data:image/png;base64,{b64_180}">

    <!-- Favicons -->
    <link rel="icon" type="image/png" sizes="192x192" href="data:image/png;base64,{b64_192}">
    <link rel="icon" type="image/png" sizes="512x512" href="data:image/png;base64,{b64_512}">

    <!-- Nice-to-have -->
    <meta name="theme-color" content="{theme_color}">
    """

    components.html(head_html, height=0, width=0)


def copy_button(text: str, label: str = "Copia negli appunti"):
    safe = text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    html = f"""
    <button id="copybtn"
      style="
        padding:10px 14px;
        border-radius:12px;
        border:1px solid rgba(255,255,255,.18);
        background: rgba(255,255,255,.08);
        color: white;
        cursor:pointer;
        font-weight:600;">
      {label}
    </button>
    <span id="copystatus" style="margin-left:10px; opacity:.8; font-size:14px;"></span>

    <script>
      const btn = document.getElementById("copybtn");
      const status = document.getElementById("copystatus");
      const txt = `{safe}`;
      btn.onclick = async () => {{
        try {{
          await navigator.clipboard.writeText(txt);
          status.textContent = "Copiato ✅";
          setTimeout(()=>status.textContent="", 1200);
        }} catch(e) {{
          status.textContent = "Non posso copiare qui 😅";
        }}
      }};
    </script>
    """
    components.html(html, height=60)


# ------------------- APP -------------------

st.set_page_config(
    page_title="🧠 Prompt Builder",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Inject PWA + iOS icons
inject_pwa_head(app_name="Prompt Builder", theme_color="#0b1220", background_color="#0b1220")


st.title("🧠 Prompt Builder")
st.caption("Costruisci prompt chiari, completi e riutilizzabili — senza impazzire.")


with st.form("builder", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Ruolo dell'AI", value="Sei un assistente esperto.")
        tone = st.selectbox("Tono", ["Neutro", "Professionale", "Amichevole", "Ironico", "Molto tecnico"], index=0)
    with col2:
        language = st.selectbox("Lingua output", ["Italiano", "English"], index=0)
        length = st.selectbox("Lunghezza risposta", ["Breve", "Media", "Dettagliata"], index=1)

    goal = st.text_area("Obiettivo (cosa vuoi ottenere)", placeholder="Es: Crea un piano marketing per un'app...", height=90)
    context = st.text_area("Contesto (info utili)", placeholder="Es: target, mercato, vincoli, dati...", height=90)
    constraints = st.text_area("Vincoli / regole (opzionale)", placeholder="Es: massimo 5 punti, evita gergo, cita fonti...", height=90)

    output_format = st.text_input("Formato output (opzionale)", value="Elenco puntato + checklist finale")
    examples = st.text_area("Esempi / Input (opzionale)", placeholder="Incolla esempi, dati, testo da trasformare...", height=90)

    submitted = st.form_submit_button("Genera prompt")


def build_prompt():
    if not goal.strip():
        return ""

    tone_map = {
        "Neutro": "Usa un tono neutro e chiaro.",
        "Professionale": "Usa un tono professionale e preciso.",
        "Amichevole": "Usa un tono amichevole e diretto.",
        "Ironico": "Usa un tono leggermente ironico ma utile.",
        "Molto tecnico": "Usa un tono molto tecnico con terminologia corretta.",
    }

    length_map = {
        "Breve": "Rispondi in modo sintetico (massimo 8-12 righe).",
        "Media": "Rispondi con una lunghezza media e ben strutturata.",
        "Dettagliata": "Rispondi in modo dettagliato, con passaggi e motivazioni.",
    }

    lang_line = "Scrivi in Italiano." if language == "Italiano" else "Write in English."

    parts = []
    parts.append(f"{role.strip()}")
    parts.append(lang_line)
    parts.append(tone_map.get(tone, "Usa un tono chiaro."))
    parts.append(length_map.get(length, "Rispondi in modo ben strutturato."))

    parts.append("\n## Obiettivo")
    parts.append(goal.strip())

    if context.strip():
        parts.append("\n## Contesto")
        parts.append(context.strip())

    if constraints.strip():
        parts.append("\n## Vincoli")
        parts.append(constraints.strip())

    if output_format.strip():
        parts.append("\n## Formato richiesto")
        parts.append(output_format.strip())

    if examples.strip():
        parts.append("\n## Dati / Esempi")
        parts.append(examples.strip())

    parts.append("\n## Checklist qualità (obbligatoria)")
    parts.append("- Se mancano informazioni critiche, fai domande mirate prima di rispondere.")
    parts.append("- Evita assunzioni non dichiarate: se assumi qualcosa, dichiaralo.")
    parts.append("- Struttura la risposta con titoli e punti chiari.")

    return "\n".join(parts).strip()


if submitted:
    final_prompt = build_prompt()
    if not final_prompt:
        st.error("Inserisci almeno l'obiettivo 🙂")
    else:
        st.subheader("Prompt generato")
        st.code(final_prompt, language="markdown")
        copy_button(final_prompt, "Copia prompt")
        st.info("Se su iPhone non cambia icona, guarda le istruzioni sotto 👇")

st.divider()
st.markdown("### Nota iPhone (icona Home)")
st.markdown(
    "- **Elimina** il collegamento già aggiunto alla Home.\n"
    "- Vai in **Impostazioni → Safari → Cancella dati siti web e cronologia**.\n"
    "- Apri di nuovo l’app in Safari, ricarica la pagina (anche due volte), poi **Condividi → Aggiungi a Home**.\n"
    "- Se ancora non cambia: prova in **Safari privato** e rifai “Aggiungi a Home”."
)

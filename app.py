import streamlit as st

# ---------- HEAD INJECTION (iPhone A2HS icon + manifest) ----------
def inject_pwa_icons(
    app_name: str = "Prompt Builder",
    theme_color: str = "#0B1220",
):
    """
    Injects <link> and <meta> tags into document.head via JS.
    This is the most reliable way in Streamlit to affect iOS "Add to Home Screen" icon.
    Files must exist under /static/...
    """
    js = f"""
    <script>
      (function() {{
        const head = document.head;

        function upsertLink(rel, href, sizes) {{
          let selector = `link[rel="${{rel}}"]` + (sizes ? `[sizes="${{sizes}}"]` : "");
          let el = head.querySelector(selector);
          if (!el) {{
            el = document.createElement("link");
            el.rel = rel;
            if (sizes) el.sizes = sizes;
            head.appendChild(el);
          }}
          el.href = href;
        }}

        function upsertMeta(name, content, isProperty=false) {{
          let selector = isProperty ? `meta[property="${{name}}"]` : `meta[name="${{name}}"]`;
          let el = head.querySelector(selector);
          if (!el) {{
            el = document.createElement("meta");
            if (isProperty) el.setAttribute("property", name);
            else el.setAttribute("name", name);
            head.appendChild(el);
          }}
          el.setAttribute("content", content);
        }}

        // Manifest
        upsertLink("manifest", "/static/manifest.json");

        // Favicons (browser tab)
        upsertLink("icon", "/static/icons/icon-192.png");
        upsertLink("apple-touch-icon", "/static/icons/icon-180.png");

        // iOS standalone look
        upsertMeta("apple-mobile-web-app-capable", "yes");
        upsertMeta("apple-mobile-web-app-status-bar-style", "black-translucent");
        upsertMeta("apple-mobile-web-app-title", "{app_name}");

        // Theme color
        upsertMeta("theme-color", "{theme_color}");

        // Optional social preview (doesn't hurt)
        upsertMeta("og:title", "{app_name}", true);
      }})();
    </script>
    """
    st.components.v1.html(js, height=0)

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Prompt Builder",
    page_icon="🧠",  # questo è per browser/Streamlit UI, NON basta per A2HS iPhone
    layout="wide"
)

inject_pwa_icons(app_name="Prompt Builder", theme_color="#0B1220")

# ---------- UI ----------
st.title("🧠 Prompt Builder")
st.caption("Costruisci prompt chiari, completi e riutilizzabili. (E sì: senza magie nere.)")

with st.sidebar:
    st.header("Impostazioni")
    tone = st.selectbox("Tono", ["Neutro", "Professionale", "Amichevole", "Creativo", "Ironico"])
    length = st.selectbox("Lunghezza output", ["Breve", "Media", "Lunga"])
    format_out = st.selectbox("Formato", ["Testo", "Lista puntata", "Tabella", "JSON"])
    include_examples = st.toggle("Includi esempi", value=True)

st.subheader("1) Contesto")
role = st.text_input("Ruolo dell'AI (es. 'copywriter', 'analista dati', 'coach fitness')", value="Esperto di prompt engineering")
goal = st.text_area("Obiettivo", placeholder="Cosa vuoi ottenere dall'AI?")
audience = st.text_input("Pubblico/utente finale (opzionale)", placeholder="Per chi è pensato l'output?")

st.subheader("2) Input e vincoli")
inputs = st.text_area("Dati / input disponibili", placeholder="Testo, punti chiave, link (se li userai), esempi, ecc.")
constraints = st.text_area("Vincoli", placeholder="Cosa evitare, limiti, stile, regole, privacy, ecc.")

st.subheader("3) Struttura output")
details = st.text_area("Dettagli desiderati", placeholder="Sezioni, criteri, checklist, passaggi, ecc.")

# ---------- PROMPT BUILDER ----------
def build_prompt():
    parts = []
    parts.append(f"Sei {role.strip() or 'un assistente esperto'}.")

    if goal.strip():
        parts.append(f"Obiettivo: {goal.strip()}")

    if audience.strip():
        parts.append(f"Pubblico: {audience.strip()}")

    parts.append(f"Tono: {tone}. Lunghezza: {length}. Formato: {format_out}.")

    if inputs.strip():
        parts.append("Input disponibili:")
        parts.append(inputs.strip())

    if constraints.strip():
        parts.append("Vincoli / regole:")
        parts.append(constraints.strip())

    if details.strip():
        parts.append("Requisiti di struttura / dettagli:")
        parts.append(details.strip())

    if include_examples:
        parts.append("Se utile, includi 1-2 esempi concreti (senza inventare dati non forniti).")

    parts.append("Fai domande solo se mancano informazioni indispensabili; altrimenti procedi con assunzioni esplicite e ragionevoli.")
    return "\n\n".join(parts)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Genera prompt", type="primary"):
        st.session_state["prompt"] = build_prompt()

with col2:
    if st.button("Pulisci"):
        st.session_state["prompt"] = ""

st.divider()

prompt = st.session_state.get("prompt", "")
st.subheader("Prompt finale")
st.text_area("Copia e incolla questo prompt nella tua AI", value=prompt, height=280)

if prompt:
    st.download_button(
        "Scarica .txt",
        data=prompt.encode("utf-8"),
        file_name="prompt_builder.txt",
        mime="text/plain"
    )

import streamlit as st
import streamlit.components.v1 as components

# -----------------------------
# Page config (favicon + title)
# -----------------------------
st.set_page_config(
    page_title="Prompt Builder",
    page_icon="🧠",
    layout="centered",
)

# -----------------------------
# Inject PWA / iOS icons + manifest
# Streamlit serves ./static/* at /app/static/*
# -----------------------------
def inject_pwa_head():
    icon180 = "/app/static/icon-180.png"
    icon192 = "/app/static/icon-192.png"
    icon512 = "/app/static/icon-512.png"
    icon1024 = "/app/static/icon-1024.png"
    manifest = "/app/static/manifest.json"

    js = f"""
    <script>
      (function() {{
        // Prevent duplicates
        function upsertLink(rel, href, sizes) {{
          let sel = 'link[rel="' + rel + '"]' + (sizes ? '[sizes="' + sizes + '"]' : '');
          let el = document.head.querySelector(sel);
          if (!el) {{
            el = document.createElement('link');
            el.setAttribute('rel', rel);
            if (sizes) el.setAttribute('sizes', sizes);
            document.head.appendChild(el);
          }}
          el.setAttribute('href', href);
        }}

        function upsertMeta(name, content) {{
          let el = document.head.querySelector('meta[name="' + name + '"]');
          if (!el) {{
            el = document.createElement('meta');
            el.setAttribute('name', name);
            document.head.appendChild(el);
          }}
          el.setAttribute('content', content);
        }}

        // iOS / PWA-ish metas
        upsertMeta('apple-mobile-web-app-capable', 'yes');
        upsertMeta('apple-mobile-web-app-status-bar-style', 'default');
        upsertMeta('apple-mobile-web-app-title', 'Prompt Builder');

        // Icons
        upsertLink('apple-touch-icon', '{icon180}', '180x180');

        // Optional: favicons (some browsers)
        upsertLink('icon', '{icon192}', '192x192');
        upsertLink('icon', '{icon512}', '512x512');

        // Manifest
        upsertLink('manifest', '{manifest}', null);

      }})();
    </script>
    """

    # Height=0 so it doesn't "take space"
    components.html(js, height=0)

inject_pwa_head()

# -----------------------------
# App UI (example)
# -----------------------------
st.title("🧠 Prompt Builder")
st.caption("Genera prompt efficaci in pochi secondi.")

with st.form("builder"):
    goal = st.text_input("Obiettivo", placeholder="Es: creare un post Instagram che vende un corso")
    audience = st.text_input("Pubblico", placeholder="Es: principianti, 25-35, interessati a…")
    tone = st.selectbox("Tono", ["Professionale", "Amichevole", "Ironico", "Tecnico", "Persuasivo"])
    context = st.text_area("Contesto / Vincoli", placeholder="Es: max 120 parole, includi CTA, no emoji…")
    output = st.selectbox("Formato output", ["Testo", "Lista", "Tabella", "Script video", "Email"])
    submit = st.form_submit_button("Crea prompt")

if submit:
    prompt = f"""Agisci come un esperto di prompt engineering.

OBIETTIVO:
{goal}

PUBBLICO:
{audience}

TONO:
{tone}

CONTESTO E VINCOLI:
{context}

FORMATO OUTPUT:
{output}

ISTRUZIONI:
- Fai domande solo se servono davvero; altrimenti procedi.
- Produci un risultato pronto all'uso.
- Se opportuno, proponi 2 varianti (breve e dettagliata).
"""
    st.subheader("✅ Prompt pronto da copiare")
    st.code(prompt, language="text")
    st.success("Fatto. Ora incollalo nella tua AI preferita e fai magia.")

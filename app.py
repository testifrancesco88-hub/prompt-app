import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime


# ----------------------------
# PWA / iPhone icon injection
# ----------------------------
def inject_icons_and_manifest():
    """
    Injects <link rel="icon"> and <link rel="apple-touch-icon"> into <head>.
    This makes the iPhone "Add to Home Screen" icon show your custom logo.
    """
    components.html(
        """
        <script>
        (function() {
          const links = [
            { rel: "apple-touch-icon", sizes: "180x180", href: "assets/icon-180.png" },
            { rel: "icon", type: "image/png", sizes: "192x192", href: "assets/icon-192.png" },
            { rel: "icon", type: "image/png", sizes: "512x512", href: "assets/icon-512.png" },
            // Optional: if you add manifest.json later, this will enable a more "app-like" install
            // { rel: "manifest", href: "assets/manifest.json" },
          ];

          function upsertLink(attrs) {
            // Try to find an existing matching link
            let selector = 'link[rel="' + attrs.rel + '"]';
            if (attrs.sizes) selector += '[sizes="' + attrs.sizes + '"]';
            let el = document.head.querySelector(selector);

            if (!el) {
              el = document.createElement("link");
              document.head.appendChild(el);
            }

            Object.keys(attrs).forEach(k => el.setAttribute(k, attrs[k]));
          }

          links.forEach(upsertLink);
        })();
        </script>
        """,
        height=0,
    )


# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="🧠 Prompt Builder",
    page_icon="🧠",  # questo è l'icona tab “base”; le icone reali le iniettiamo sopra
    layout="wide",
)

inject_icons_and_manifest()


# ----------------------------
# UI helpers
# ----------------------------
def pill(label: str, value: str):
    st.markdown(
        f"""
        <div style="
            display:inline-block;
            padding:6px 10px;
            border-radius:999px;
            border:1px solid rgba(255,255,255,0.15);
            background:rgba(255,255,255,0.04);
            margin-right:8px;
            margin-bottom:8px;
            font-size:13px;">
          <b>{label}</b> {value}
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_prompt(goal, audience, context, input_data, constraints, tone, format_out, examples, model_hint):
    sections = []

    sections.append(f"## Obiettivo\n{goal.strip() or '-'}")
    sections.append(f"## Pubblico / Utente target\n{audience.strip() or '-'}")
    sections.append(f"## Contesto\n{context.strip() or '-'}")

    if input_data.strip():
        sections.append(f"## Dati di input\n{input_data.strip()}")

    if constraints.strip():
        sections.append(f"## Vincoli\n{constraints.strip()}")

    sections.append(f"## Stile / Tono\n{tone.strip() or '-'}")
    sections.append(f"## Formato output richiesto\n{format_out.strip() or '-'}")

    if examples.strip():
        sections.append(f"## Esempi / Riferimenti\n{examples.strip()}")

    if model_hint.strip():
        sections.append(f"## Note per il modello\n{model_hint.strip()}")

    sections.append(
        "## Istruzioni finali\n"
        "- Se qualcosa è ambiguo, fai domande mirate prima di rispondere.\n"
        "- Ragiona passo-passo internamente, ma mostra all’utente solo il risultato finale in modo chiaro.\n"
        "- Se proponi opzioni, presentale in elenco e poi consigliami la migliore."
    )

    return "\n\n".join(sections)


# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.image("assets/icon-512.png", width=84)
    st.markdown("### 🧠 Prompt Builder")
    st.caption("Costruisci prompt più chiari, completi e “a prova di fraintendimenti”.")

    template = st.selectbox(
        "Template",
        [
            "Generico (consigliato)",
            "Copywriting / Ads",
            "Analisi dati / Tabelle",
            "Coding / Debug",
            "Strategia / Business",
        ],
        index=0,
    )

    st.markdown("---")
    st.markdown("**Suggerimento veloce**")
    st.write("Un prompt forte = obiettivo + contesto + vincoli + formato output.")


# ----------------------------
# Main layout
# ----------------------------
st.title("🧠 Prompt Builder")
st.caption("Costruisci un prompt “serio” senza perdere tempo. Poi copia/incolla dove vuoi (ChatGPT, Claude, Gemini, ecc.).")

c1, c2, c3, c4 = st.columns(4)
with c1:
    pill("Template:", template)
with c2:
    pill("Aggiornato:", datetime.now().strftime("%d/%m/%Y"))
with c3:
    pill("Icone:", "iPhone + Browser ✅")
with c4:
    pill("Export:", "Copia / TXT ✅")

st.markdown("---")

left, right = st.columns([1, 1])

with left:
    st.subheader("1) Inserisci i dettagli")

    goal = st.text_area("Obiettivo (cosa vuoi ottenere?)", height=90, placeholder="Esempio: Crea una landing page che converta per un'app di prompt...")

    if template == "Copywriting / Ads":
        audience_ph = "Esempio: utenti iPhone 18–35, interessati a produttività e AI"
        format_default = "Headline + sottotitolo + 3 benefit + CTA + 2 varianti A/B"
    elif template == "Analisi dati / Tabelle":
        audience_ph = "Esempio: un manager non tecnico che deve decidere velocemente"
        format_default = "Tabella + bullet di insight + raccomandazione finale"
    elif template == "Coding / Debug":
        audience_ph = "Esempio: sviluppatore Python junior"
        format_default = "Spiegazione breve + patch del codice + test suggeriti"
    elif template == "Strategia / Business":
        audience_ph = "Esempio: founder che deve validare un'idea"
        format_default = "Analisi + opzioni + pro/contro + roadmap 30 giorni"
    else:
        audience_ph = "Esempio: principianti, esperti, clienti finali, ecc."
        format_default = "Risposta strutturata con punti elenco e sezione finale con sintesi"

    audience = st.text_input("Pubblico / Utente target", placeholder=audience_ph)

    context = st.text_area("Contesto (cosa deve sapere l’AI?)", height=90, placeholder="Vincoli, scenario, cosa hai già provato, cosa NON vuoi…")

    input_data = st.text_area("Dati di input (opzionale)", height=90, placeholder="Incolla testo, dati, link descrittivi, requisiti, ecc.")

    constraints = st.text_area("Vincoli (opzionale)", height=80, placeholder="Esempio: max 120 parole, niente gergo, tono amichevole, ecc.")

    tone = st.text_input("Stile / Tono", value="Chiaro, pratico, diretto")
    format_out = st.text_input("Formato output richiesto", value=format_default)

    examples = st.text_area("Esempi / Riferimenti (opzionale)", height=80, placeholder="Esempio: 'simile allo stile di X', oppure incolla un esempio di output ideale.")
    model_hint = st.text_input("Note per il modello (opzionale)", placeholder="Esempio: 'se mancano info, fai 3 domande prima di rispondere'")

    st.markdown("### 2) Genera")
    generate = st.button("✨ Crea prompt", use_container_width=True)

with right:
    st.subheader("Prompt finale")

    if "final_prompt" not in st.session_state:
        st.session_state.final_prompt = ""

    if generate:
        st.session_state.final_prompt = build_prompt(
            goal=goal,
            audience=audience,
            context=context,
            input_data=input_data,
            constraints=constraints,
            tone=tone,
            format_out=format_out,
            examples=examples,
            model_hint=model_hint,
        )

    st.text_area(
        "Copia/incolla questo prompt nella tua AI:",
        value=st.session_state.final_prompt,
        height=420,
    )

    colA, colB = st.columns(2)
    with colA:
        if st.session_state.final_prompt.strip():
            st.download_button(
                "⬇️ Scarica .txt",
                data=st.session_state.final_prompt,
                file_name="prompt_builder.txt",
                mime="text/plain",
                use_container_width=True,
            )
    with colB:
        st.caption("Tip: su iPhone, usa “Condividi → Aggiungi a Home” per averla come app.")

st.markdown("---")
st.caption("Se vuoi, dopo ti preparo anche il `manifest.json` (PWA) così su iPhone sembra ancora più un’app vera, con splash e nome corretto.")

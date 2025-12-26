import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Prompt Builder", page_icon="🧠", layout="centered")

st.title("🧠 Prompt Builder")
st.caption("Crea prompt efficaci e riutilizzabili per qualsiasi AI (ChatGPT, Claude, Gemini, ecc.).")

with st.sidebar:
    st.header("⚙️ Impostazioni")
    model_family = st.selectbox(
        "Target (opzionale)",
        ["Generico", "ChatGPT", "Claude", "Gemini", "Midjourney/Immagini", "Copilot/Dev"],
        index=0,
    )
    prompt_style = st.selectbox(
        "Stile del prompt",
        ["Strutturato (consigliato)", "Compatto", "Checklist + Prompt"],
        index=0,
    )
    include_guardrails = st.checkbox("Aggiungi guardrails (evita allucinazioni)", value=True)
    include_clarifying = st.checkbox("Chiedi domande se mancano info", value=True)
    include_rubric = st.checkbox("Aggiungi rubric di qualità (autovalutazione)", value=False)

st.divider()

col1, col2 = st.columns(2)
with col1:
    goal = st.text_area("🎯 Obiettivo", placeholder="Es: Scrivere una landing page per un corso di Fusion 360", height=100)
    audience = st.text_input("👥 Pubblico", placeholder="Es: principianti, developer, clienti B2B…")
    tone = st.selectbox("🗣️ Tono", ["Neutro", "Professionale", "Amichevole", "Diretto", "Creativo", "Tecnico"], index=1)
with col2:
    context = st.text_area("🧩 Contesto / background", placeholder="Info utili, dati, link, vincoli di scenario…", height=100)
    constraints = st.text_area("⛓️ Vincoli", placeholder="Es: max 200 parole, evita gergo, lingua IT, compliance…", height=80)
    output_format = st.text_input("📦 Formato output", placeholder="Es: elenco puntato + tabella + CTA finale")

examples = st.text_area("🧪 Esempi (opzionale)", placeholder="Esempio di input/output o stile da imitare (anche grezzo).", height=120)

st.divider()

advanced = st.expander("🔬 Avanzato (opzionale)")
with advanced:
    role = st.text_input("🎭 Ruolo dell'AI", placeholder="Es: Sei un copywriter senior specializzato in SaaS…")
    do_list = st.text_area("✅ Da fare", placeholder="Es: includi un piano in 5 step; chiedi 3 domande; proponi 2 varianti…", height=80)
    dont_list = st.text_area("⛔ Da NON fare", placeholder="Es: non inventare statistiche; non citare fonti non verificate…", height=80)

def build_prompt():
    parts = []

    # Header / role
    if role.strip():
        parts.append(f"RUOLO:\n{role.strip()}\n")

    # Target
    if model_family != "Generico":
        parts.append(f"TARGET:\nOttimizza la risposta per {model_family}.\n")

    # Goal
    if goal.strip():
        parts.append(f"OBIETTIVO:\n{goal.strip()}\n")
    else:
        parts.append("OBIETTIVO:\n[Inserisci un obiettivo chiaro qui]\n")

    # Context
    if context.strip():
        parts.append(f"CONTESTO:\n{context.strip()}\n")

    # Audience + tone
    meta = []
    if audience.strip():
        meta.append(f"Pubblico: {audience.strip()}")
    if tone:
        meta.append(f"Tono: {tone}")
    if meta:
        parts.append("STILE:\n" + " | ".join(meta) + "\n")

    # Constraints
    if constraints.strip():
        parts.append(f"VINCOLI:\n{constraints.strip()}\n")

    # Output format
    if output_format.strip():
        parts.append(f"FORMATO OUTPUT:\n{output_format.strip()}\n")

    # Do / Don't
    if do_list.strip():
        parts.append(f"DA FARE:\n{do_list.strip()}\n")
    if dont_list.strip():
        parts.append(f"DA NON FARE:\n{dont_list.strip()}\n")

    # Examples
    if examples.strip():
        parts.append(f"ESEMPI:\n{examples.strip()}\n")

    # Guardrails
    if include_guardrails:
        parts.append(
            "GUARDRAILS:\n"
            "- Se non sei sicuro di un dato, dichiaralo e proponi come verificarlo.\n"
            "- Non inventare numeri, nomi propri o citazioni.\n"
        )

    # Clarifying questions
    if include_clarifying:
        parts.append(
            "DOMANDE:\n"
            "- Se mancano informazioni essenziali, fai fino a 3 domande mirate prima di rispondere.\n"
        )

    # Rubric
    if include_rubric:
        parts.append(
            "RUBRIC DI QUALITÀ (autovaluta prima di finalizzare):\n"
            "- Chiarezza (0-10)\n- Completezza (0-10)\n- Aderenza ai vincoli (0-10)\n"
        )

    return "\n".join(parts).strip()

def build_compact():
    base = build_prompt()
    # versione più corta: elimina intestazioni “lunghe”
    lines = [ln for ln in base.splitlines() if ln.strip() != ""]
    return "\n".join(lines)

def build_checklist_prompt():
    prompt = build_prompt()
    checklist = [
        "✅ Obiettivo chiaro e misurabile",
        "✅ Contesto sufficiente (dati, scenario, definizioni)",
        "✅ Vincoli espliciti (lunghezza, lingua, stile, compliance)",
        "✅ Output richiesto in formato preciso",
        "✅ Esempi (se serve) per guidare lo stile",
        "✅ Guardrails per evitare invenzioni",
    ]
    return "CHECKLIST:\n- " + "\n- ".join(checklist) + "\n\nPROMPT:\n" + prompt

generate = st.button("✨ Genera prompt")

if generate:
    if prompt_style == "Strutturato (consigliato)":
        final_prompt = build_prompt()
    elif prompt_style == "Compatto":
        final_prompt = build_compact()
    else:
        final_prompt = build_checklist_prompt()

    st.subheader("📌 Il tuo prompt")
    st.code(final_prompt, language="markdown")

    st.download_button(
        "⬇️ Scarica come .txt",
        data=final_prompt.encode("utf-8"),
        file_name=f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
    )

st.info("Tip: più sei specifico su **obiettivo + vincoli + formato output**, meno l’AI “improvvisa”.")

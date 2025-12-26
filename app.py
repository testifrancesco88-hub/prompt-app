import json
from datetime import datetime
from pathlib import Path

import streamlit as st


# -----------------------------
# Helpers
# -----------------------------
ASSETS_DIR = Path(__file__).parent / "assets"

ICON_180 = ASSETS_DIR / "icon-180.png"
ICON_192 = ASSETS_DIR / "icon-192.png"
ICON_512 = ASSETS_DIR / "icon-512.png"
ICON_1024 = ASSETS_DIR / "icon-1024.png"

def safe_icon_path(p: Path):
    return str(p) if p.exists() else None

def build_prompt(data: dict) -> str:
    role = data.get("role", "").strip()
    goal = data.get("goal", "").strip()
    context = data.get("context", "").strip()
    audience = data.get("audience", "").strip()
    tone = data.get("tone", "").strip()
    language = data.get("language", "").strip()
    constraints = [c.strip() for c in data.get("constraints", []) if c.strip()]
    must_include = [m.strip() for m in data.get("must_include", []) if m.strip()]
    must_avoid = [m.strip() for m in data.get("must_avoid", []) if m.strip()]
    output_format = data.get("output_format", "").strip()
    length = data.get("length", "").strip()
    examples = data.get("examples", "").strip()
    evaluation = data.get("evaluation", "").strip()

    lines = []

    # Identity / role
    if role:
        lines.append(f"Agisci come: {role}")

    # Language
    if language:
        lines.append(f"Rispondi in: {language}")

    # Tone
    if tone:
        lines.append(f"Tono/Stile: {tone}")

    # Audience
    if audience:
        lines.append(f"Pubblico target: {audience}")

    lines.append("")  # spacer

    # Goal
    if goal:
        lines.append("OBIETTIVO")
        lines.append(goal)
        lines.append("")

    # Context
    if context:
        lines.append("CONTESTO")
        lines.append(context)
        lines.append("")

    # Constraints
    if constraints:
        lines.append("VINCOLI")
        for c in constraints:
            lines.append(f"- {c}")
        lines.append("")

    # Must include / avoid
    if must_include:
        lines.append("INCLUDI OBBLIGATORIAMENTE")
        for m in must_include:
            lines.append(f"- {m}")
        lines.append("")

    if must_avoid:
        lines.append("EVITA")
        for m in must_avoid:
            lines.append(f"- {m}")
        lines.append("")

    # Output format
    if output_format or length:
        lines.append("OUTPUT RICHIESTO")
        if output_format:
            lines.append(f"- Formato: {output_format}")
        if length:
            lines.append(f"- Lunghezza: {length}")
        lines.append("")

    # Examples
    if examples:
        lines.append("ESEMPI (se utili)")
        lines.append(examples)
        lines.append("")

    # Evaluation / checklist
    if evaluation:
        lines.append("CONTROLLO QUALITÀ")
        lines.append(evaluation)
        lines.append("")

    # Final instruction
    lines.append("Se ti mancano informazioni importanti, fai prima le domande minime necessarie (max 5) e poi produci l’output.")

    # Clean trailing spaces
    prompt = "\n".join(lines).strip()
    return prompt


# -----------------------------
# Page config (favicon/tab icon)
# -----------------------------
st.set_page_config(
    page_title="🧠 Prompt Builder",
    page_icon=safe_icon_path(ICON_192) or "🧠",
    layout="wide",
)


# -----------------------------
# Header
# -----------------------------
colA, colB = st.columns([1, 3], vertical_alignment="center")
with colA:
    if ICON_512.exists():
        st.image(str(ICON_512), width=140)
    else:
        st.markdown("## 🧠")

with colB:
    st.title("🧠 Prompt Builder")
    st.caption("Crea prompt chiari, completi e riutilizzabili per qualsiasi AI (ChatGPT, Claude, Gemini, ecc.).")


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.subheader("Impostazioni")
    st.write("Le icone vengono lette da `assets/` (icon-192 usata come favicon).")

    st.markdown("---")
    preset = st.selectbox(
        "Preset rapido",
        [
            "Generico",
            "Copywriting (ads/landing)",
            "Coding (debug/feature)",
            "Analisi dati",
            "Social (post/idee)",
            "Prompt per immagini (stile/brief)",
        ],
        index=0
    )

    st.markdown("---")
    st.caption("Suggerimento: un buon prompt è come una richiesta al barista: se dici solo “caffè”, ti arriva quello che capita ☕")


# -----------------------------
# Defaults per preset
# -----------------------------
def preset_defaults(p: str) -> dict:
    if p == "Copywriting (ads/landing)":
        return dict(
            role="Copywriter senior orientato alle conversioni",
            tone="Chiaro, persuasivo, concreto, senza superlativi vuoti",
            output_format="Titolo + sottotitolo + 3 bullet benefit + CTA + varianti",
            evaluation="Controlla: chiarezza, specificità, coerenza col target, nessuna promessa non verificabile."
        )
    if p == "Coding (debug/feature)":
        return dict(
            role="Senior software engineer e code reviewer",
            tone="Diretto, pratico, con esempi",
            output_format="Spiegazione breve + patch/ codice + note su edge case",
            evaluation="Controlla: correttezza, complessità, compatibilità, sicurezza."
        )
    if p == "Analisi dati":
        return dict(
            role="Data analyst",
            tone="Preciso, strutturato",
            output_format="Passi + formule/SQL/Python se serve + conclusioni",
            evaluation="Controlla: assunzioni esplicite, limiti, interpretazione corretta."
        )
    if p == "Social (post/idee)":
        return dict(
            role="Content creator",
            tone="Energico ma non cringe 😄",
            output_format="10 idee + 3 hook + 1 calendario settimanale",
            evaluation="Controlla: originalità, call-to-action, chiarezza."
        )
    if p == "Prompt per immagini (stile/brief)":
        return dict(
            role="Art director",
            tone="Tecnico e descrittivo",
            output_format="Prompt principale + negative prompt + varianti",
            evaluation="Controlla: soggetto, stile, luce, composizione, dettagli coerenti."
        )
    return dict(
        role="Assistente esperto",
        tone="Chiaro e utile",
        output_format="Strutturato in punti con esempi se utile",
        evaluation="Controlla: rispetta i vincoli, niente invenzioni, chiedi chiarimenti se manca contesto."
    )


defaults = preset_defaults(preset)

# -----------------------------
# Main builder UI
# -----------------------------
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.subheader("1) Costruisci il prompt")

    role = st.text_input("Ruolo dell’AI", value=defaults["role"], placeholder="Es: Product manager, Avvocato, Tutor di matematica...")
    goal = st.text_area("Obiettivo", height=110, placeholder="Cosa vuoi ottenere, in modo misurabile?")
    context = st.text_area("Contesto", height=140, placeholder="Dettagli, background, dati, link (se rilevanti)...")
    audience = st.text_input("Pubblico target (opzionale)", placeholder="Es: principianti, clienti B2B, studenti...")

    c1, c2 = st.columns(2)
    with c1:
        tone = st.text_input("Tono / stile", value=defaults["tone"])
    with c2:
        language = st.selectbox("Lingua output", ["Italiano", "English", "Español", "Français", "Deutsch"], index=0)

    st.markdown("#### Vincoli / Regole")
    constraints_raw = st.text_area(
        "Un vincolo per riga (opzionale)",
        height=100,
        placeholder="Es:\n- Non usare gergo tecnico\n- Includi pro/contro\n- Massimo 200 parole",
    )
    constraints = [x.lstrip("-• ").strip() for x in constraints_raw.splitlines() if x.strip()]

    st.markdown("#### Include / Evita")
    ci1, ci2 = st.columns(2)
    with ci1:
        must_include_raw = st.text_area(
            "Includi (uno per riga)",
            height=90,
            placeholder="Es:\n- Tabella comparativa\n- Esempi pratici",
        )
        must_include = [x.lstrip("-• ").strip() for x in must_include_raw.splitlines() if x.strip()]
    with ci2:
        must_avoid_raw = st.text_area(
            "Evita (uno per riga)",
            height=90,
            placeholder="Es:\n- Nomi inventati\n- Dati non verificati",
        )
        must_avoid = [x.lstrip("-• ").strip() for x in must_avoid_raw.splitlines() if x.strip()]

    st.markdown("#### Output")
    o1, o2 = st.columns(2)
    with o1:
        output_format = st.text_input("Formato output", value=defaults["output_format"], placeholder="Es: lista puntata, tabella, JSON...")
    with o2:
        length = st.selectbox("Lunghezza", ["Breve", "Media", "Lunga", "Molto lunga"], index=1)

    examples = st.text_area("Esempi (opzionale)", height=110, placeholder="Incolla esempi di stile o input/output desiderati...")
    evaluation = st.text_area("Checklist qualità (opzionale)", value=defaults["evaluation"], height=100)

    data = {
        "role": role,
        "goal": goal,
        "context": context,
        "audience": audience,
        "tone": tone,
        "language": language,
        "constraints": constraints,
        "must_include": must_include,
        "must_avoid": must_avoid,
        "output_format": output_format,
        "length": length,
        "examples": examples,
        "evaluation": evaluation,
    }

    generate = st.button("✨ Genera prompt", use_container_width=True)


with right:
    st.subheader("2) Prompt finale")

    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    if generate:
        st.session_state.prompt = build_prompt(data)

    if st.session_state.prompt.strip():
        st.code(st.session_state.prompt, language="markdown")
        st.download_button(
            "⬇️ Scarica come TXT",
            data=st.session_state.prompt.encode("utf-8"),
            file_name=f"prompt_builder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.download_button(
            "⬇️ Scarica come JSON (dati builder)",
            data=json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name=f"prompt_builder_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )

        st.info("Tip: incolla il prompt nella tua AI e poi aggiungi il materiale (testo/dati) subito dopo.")
    else:
        st.caption("Compila a sinistra e premi **Genera prompt**.")


# -----------------------------
# Footer / assets check
# -----------------------------
with st.expander("🔧 Diagnostica assets (se qualcosa non si vede)"):
    st.write("Percorso assets:", str(ASSETS_DIR))
    st.write("icon-192 (favicon):", "OK ✅" if ICON_192.exists() else "MANCANTE ❌")
    st.write("icon-512 (header):", "OK ✅" if ICON_512.exists() else "MANCANTE ❌")
    st.write("icon-1024:", "OK ✅" if ICON_1024.exists() else "MANCANTE ❌")
    st.caption("Se non vede le icone dopo il deploy, prova hard refresh del browser o redeploy.")

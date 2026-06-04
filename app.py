import streamlit as st
import json
import random
import pandas as pd
import altair as alt

# --- Seitenkonfiguration ---
st.set_page_config(page_title="Szenentrainer", layout="centered", page_icon="🎭")

# --- Daten laden ---
@st.cache_data
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# --- Smart Randomizer (Shuffle Bag Algorithmus) ---
def get_next_item(category_key):
    pool_key = f"pool_{category_key}"
    if pool_key not in st.session_state or len(st.session_state[pool_key]) == 0:
        st.session_state[pool_key] = data[category_key].copy()
        random.shuffle(st.session_state[pool_key])
    return st.session_state[pool_key].pop()

# --- Callbacks für die Buttons ---
def draw_new_verb():
    st.session_state.verb = get_next_item('verben')

def draw_new_circumplex():
    st.session_state.circumplex = (random.randint(-100, 100), random.randint(-100, 100))

def draw_new_umstand():
    st.session_state.umstand = get_next_item('umstaende')
    
def draw_new_beziehung():
    st.session_state.beziehung = get_next_item('beziehungen')
    
def draw_new_trigger():
    st.session_state.trigger = get_next_item('trigger')
    
def draw_new_widerstand():
    st.session_state.widerstand = get_next_item('widerstand')

# --- Session State Initialisierung ---
if 'verb' not in st.session_state:
    st.session_state.verb = get_next_item('verben')
if 'circumplex' not in st.session_state:
    st.session_state.circumplex = (random.randint(-100, 100), random.randint(-100, 100))
    
if 'umstand' not in st.session_state:
    st.session_state.umstand = get_next_item('umstaende')
if 'beziehung' not in st.session_state:
    st.session_state.beziehung = get_next_item('beziehungen')
if 'trigger' not in st.session_state:
    st.session_state.trigger = get_next_item('trigger')
if 'widerstand' not in st.session_state:
    st.session_state.widerstand = get_next_item('widerstand')

# --- Responsive Styling & Mobile-Tooltip ---
st.markdown("""
    <style>
    .block-container {
        max-width: 1100px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    
    .big-verb {
        font-size: clamp(1.8rem, 6vw, 3.5rem) !important; 
        font-weight: 900;
        color: #ff4b4b;
        margin-bottom: 10px;
        line-height: 1.1;
        text-transform: uppercase;
        letter-spacing: 2px;
        display: flex;
        align-items: center;
        flex-wrap: wrap; 
        gap: 8px;
        word-break: break-word; 
    }
    
    /* --- CSS Tooltip Logik (Desktop Hover & Mobile Tap) --- */
    .tooltip-container {
        position: relative;
        display: inline-block;
        cursor: pointer;
        outline: none; /* Verhindert den blauen Rahmen beim Antippen */
        -webkit-tap-highlight-color: transparent;
    }
    
    .tooltip-icon {
        font-size: clamp(1.2rem, 3vw, 1.8rem);
        color: #888;
        opacity: 0.6;
        transition: all 0.2s;
        margin-left: 5px;
    }
    
    .tooltip-container:hover .tooltip-icon,
    .tooltip-container:focus .tooltip-icon {
        opacity: 1.0;
        transform: scale(1.1);
    }
    
    .tooltip-text {
        visibility: hidden;
        background-color: #262730;
        color: #ffffff;
        text-align: left;
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid #444;
        
        /* Text-Reset für saubere Duden-Lesbarkeit */
        font-size: 1rem;
        font-weight: 500;
        text-transform: none;
        letter-spacing: normal;
        line-height: 1.4;
        font-family: sans-serif;
        
        /* Positionierung */
        position: absolute;
        z-index: 9999;
        top: 140%;
        left: 50%;
        transform: translateX(-50%);
        width: max-content;
        max-width: 280px;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.4);
        
        opacity: 0;
        transition: opacity 0.2s;
    }
    
    /* Das kleine Dreieck (Pfeil) oben am Tooltip */
    .tooltip-text::after {
        content: "";
        position: absolute;
        bottom: 100%;
        left: 50%;
        margin-left: -8px;
        border-width: 8px;
        border-style: solid;
        border-color: transparent transparent #262730 transparent;
    }
    
    /* Mobile-Optimierung: Tooltip nach links verschieben, damit er nicht aus dem Display ragt */
    @media (max-width: 600px) {
        .tooltip-text {
            transform: translateX(-80%);
        }
        .tooltip-text::after {
            left: 80%;
        }
    }
    
    /* Tooltip anzeigen bei Hover (PC) oder Focus/Tap (Handy) */
    .tooltip-container:hover .tooltip-text,
    .tooltip-container:focus .tooltip-text,
    .tooltip-container:active .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    /* --------------------------------------------------- */
    
    .highlight-tactic {
        background-color: rgba(255, 75, 75, 0.1);
        padding: clamp(12px, 3vw, 20px);
        border-left: 6px solid #ff4b4b;
        border-radius: 8px;
        margin-top: 15px;
        font-size: clamp(1.1rem, 3vw, 1.4rem);
        font-weight: 600;
        line-height: 1.4;
    }
    
    .streamlit-expanderHeader {
        font-size: clamp(1rem, 2.5vw, 1.2rem) !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# KOPFZEILE
# ==========================================
st.title("🎭 Szenentrainer")
st.markdown("---")

# ==========================================
# HAUPTFOKUS: DAS AKTIONS-VERB
# ==========================================
st.caption("DEIN AKTIONS-VERB")

verb_base = st.session_state.verb['base']
verb_def = st.session_state.verb.get('definition', '')

# Hier sitzt jetzt die Mobile-taugliche Tooltip-Struktur (tabindex="0" macht es antippbar)
st.markdown(f"""
    <div class='big-verb'>
        {verb_base} 
        <div class='tooltip-container' tabindex='0'>
            <span class='tooltip-icon'>ℹ️</span>
            <div class='tooltip-text'>{verb_def}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.expander("🎨 Taktische Präzisierung (Optionale Färbung)"):
    st.markdown("Wähle **einen** konkreten Impuls, wie du diese Aktion ausführen willst:")
    
    radio_key = f"radio_{st.session_state.verb['base']}"
    selected_tactic = st.radio(
        "Impuls:", 
        st.session_state.verb['details'], 
        index=None,
        label_visibility="collapsed",
        key=radio_key
    )
    
    if selected_tactic:
        st.markdown(f"<div class='highlight-tactic'>... {selected_tactic}</div>", unsafe_allow_html=True)

st.write("")
st.button("🔄 Neues Verb ziehen", on_click=draw_new_verb, use_container_width=True)

st.write("")
st.write("")

# ==========================================
# DAS CIRCUMPLEX-MODELL (ENERGETISCHE LADUNG)
# ==========================================
circumplex_aktiv = st.checkbox("⚡ Circumplex-Modus aktivieren (Energetischer Zustand)", key="show_circumplex")

if circumplex_aktiv:
    st.markdown("#### Deine energetische Ladung")
    st.caption("Finde diesen Zustand organisch im Körper, bevor du mit dem Text beginnst. Wie fühlst du dich (Valenz) und wie hoch ist dein Puls (Arousal)?")
    
    val, arou = st.session_state.circumplex
    
    df = pd.DataFrame({"Valenz": [val], "Arousal": [arou]})
    
    xrule = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='gray', strokeDash=[4,4]).encode(y='y')
    yrule = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='gray', strokeDash=[4,4]).encode(x='x')
    
    point = alt.Chart(df).mark_circle(size=400, color='#ff4b4b', opacity=0.9).encode(
        x=alt.X('Valenz', scale=alt.Scale(domain=[-100, 100]), title='Valenz (Tiefe Bedrohung ◀  ▶ Absolute Sicherheit)'),
        y=alt.Y('Arousal', scale=alt.Scale(domain=[-100, 100]), title='Arousal (Erschlafft ◀  ▶ Alarmiert/Puls)'),
        tooltip=['Valenz', 'Arousal']
    )
    
    chart = (xrule + yrule + point).properties(height=350)
    st.altair_chart(chart, use_container_width=True)
    
    st.button("🎲 Zustand neu auswürfeln", on_click=draw_new_circumplex)

st.write("")
st.write("")

# ==========================================
# DIE GEWÜRZ-SCHUBLADE (OPTIONALE EBENEN)
# ==========================================
with st.expander("🛠️ Zusätzliche Ebenen (Die Gewürz-Schublade)"):
    st.markdown("Nutze diese Hindernisse nur, wenn das reine Verb etabliert ist und du eine zusätzliche handwerkliche Hürde brauchst.")
    
    # Umstand
    st.markdown("#### 🏔️ Umstand / Physisches Hindernis")
    st.info(st.session_state.umstand['base'])
    st.button("Neu: Umstand", on_click=draw_new_umstand)
        
    st.markdown("---")
    
    # Beziehung
    st.markdown("#### 👥 Beziehung")
    st.info(st.session_state.beziehung['base'])
    st.button("Neu: Beziehung", on_click=draw_new_beziehung)

    st.markdown("---")
    
    # Trigger
    st.markdown("#### ⚡ Unmittelbarer Trigger (Sekunde vor Textbeginn)")
    st.info(st.session_state.trigger)
    st.button("Neu: Trigger", on_click=draw_new_trigger)

    st.markdown("---")

    # Widerstand
    st.markdown("#### 🛡️ Widerstand des Partners (Meisner)")
    st.info(st.session_state.widerstand)
    st.button("Neu: Widerstand", on_click=draw_new_widerstand)

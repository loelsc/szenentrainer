import streamlit as st
import json
import random

# Lade die JSON-Daten
@st.cache_data
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

# Helper für Historie und zufälliges Ziehen
def get_random_with_history(options_list, history_list, max_history=5, is_dict=True):
    if is_dict:
        valid_options = [opt for opt in options_list if opt['base'] not in history_list]
    else:
        valid_options = [opt for opt in options_list if opt not in history_list]
        
    if not valid_options:
        valid_options = options_list
        
    chosen = random.choice(valid_options)
    
    track_val = chosen['base'] if is_dict else chosen
    history_list.append(track_val)
    if len(history_list) > max_history:
        history_list.pop(0)
        
    return chosen

# Initialisiere / Resette das Board
def reset_board():
    for key in ['verb_base', 'verb_details', 'verb_current_detail',
                'umstand_base', 'umstand_details', 'umstand_current_detail',
                'beziehung_base', 'beziehung_details', 'beziehung_current_detail',
                'text_topic_content', 'trigger_content', 'widerstand_content']:
        st.session_state[key] = None

if 'initialized' not in st.session_state:
    reset_board()
    for key in ['hist_verben', 'hist_umstaende', 'hist_beziehungen', 'hist_vehikel', 'hist_trigger', 'hist_widerstand']:
        st.session_state[key] = []
    st.session_state.initialized = True

# --- UI Aufbau ---
st.set_page_config(layout="wide", page_title="Szenentrainer")
st.title("🎭 Szenentrainer")

if st.button("🧹 Alles zurücksetzen", type="primary"):
    reset_board()
    st.rerun()

st.divider()

# Layout Kern-Elemente
col1, col2, col3 = st.columns(3)

def render_column(title, category_key, state_prefix):
    st.subheader(title)
    if st.session_state[f"{state_prefix}_base"] is None:
        if st.button(f"🎲 Auswürfeln", key=f"btn_draw_{state_prefix}"):
            item = get_random_with_history(data[category_key], st.session_state[f"hist_{category_key}"])
            st.session_state[f"{state_prefix}_base"] = item['base']
            st.session_state[f"{state_prefix}_details"] = item['details']
            st.session_state[f"{state_prefix}_current_detail"] = None
            st.rerun()
    else:
        c_text, c_btn = st.columns([8, 2])
        with c_text:
            st.info(st.session_state[f"{state_prefix}_base"])
        with c_btn:
            if st.button("🔄", key=f"btn_re_base_{state_prefix}", help=f"{title} neu auswürfeln"):
                item = get_random_with_history(data[category_key], st.session_state[f"hist_{category_key}"])
                st.session_state[f"{state_prefix}_base"] = item['base']
                st.session_state[f"{state_prefix}_details"] = item['details']
                st.session_state[f"{state_prefix}_current_detail"] = None
                st.rerun()
                
        if st.session_state[f"{state_prefix}_current_detail"] is None:
            if st.button("🎯 Präzisieren", key=f"btn_prez_{state_prefix}"):
                st.session_state[f"{state_prefix}_current_detail"] = random.choice(st.session_state[f"{state_prefix}_details"])
                st.rerun()
        else:
            c_det, c_btn_det = st.columns([8, 2])
            with c_det:
                st.success(st.session_state[f"{state_prefix}_current_detail"])
            with c_btn_det:
                if st.button("🔄", key=f"btn_re_det_{state_prefix}", help="Präzisierung neu auswürfeln"):
                    current = st.session_state[f"{state_prefix}_current_detail"]
                    options = [d for d in st.session_state[f"{state_prefix}_details"] if d != current]
                    st.session_state[f"{state_prefix}_current_detail"] = random.choice(options) if options else current
                    st.rerun()

with col1:
    render_column("Aktions-Verb", "verben", "verb")
with col2:
    render_column("Hindernis / Umstand", "umstaende", "umstand")
with col3:
    render_column("Beziehung", "beziehungen", "beziehung")

st.divider()

# Text oder Thema
st.subheader("📄 Text oder Themengebiet")
choice = st.radio("Was möchtest du als Grundlage nutzen?", ["Neutraler Text", "Themengebiet"], horizontal=True, label_visibility="collapsed")

if st.session_state.text_topic_content is None:
    if st.button("🎲 Vehikel auswählen", key="btn_text_topic"):
        cat_key = 'texte' if choice == "Neutraler Text" else 'themen'
        prefix = "**Dein Text:**\n\n" if choice == "Neutraler Text" else "**Dein Impro-Thema:**\n\n"
        chosen_text = get_random_with_history(data[cat_key], st.session_state['hist_vehikel'], is_dict=False)
        st.session_state.text_topic_content = f"{prefix}{chosen_text}"
        st.rerun()
else:
    c_text, c_btn = st.columns([10, 1])
    with c_text:
         st.markdown(f"> {st.session_state.text_topic_content}")
    with c_btn:
         if st.button("🔄", key="btn_re_vehikel", help="Neu auswürfeln"):
             cat_key = 'texte' if choice == "Neutraler Text" else 'themen'
             prefix = "**Dein Text:**\n\n" if choice == "Neutraler Text" else "**Dein Impro-Thema:**\n\n"
             chosen_text = get_random_with_history(data[cat_key], st.session_state['hist_vehikel'], is_dict=False)
             st.session_state.text_topic_content = f"{prefix}{chosen_text}"
             st.rerun()

st.divider()

# --- Solo-Training Modul (Meisner & Mitchell Fokus) ---
st.subheader("👤 Modus für Solo-Training")
st.write("Verhindert Spielen im luftleeren Raum durch klare Vorgaben zum 'Immediate Event' und zum Verhalten des imaginären Partners.")

c_trig, c_wid = st.columns(2)

# Trigger
with c_trig:
    st.markdown("**1. Der Trigger (Unmittelbarer Vorfall)**")
    st.caption("Was passierte exakt eine Sekunde vor dem ersten Wort?")
    
    if st.session_state.trigger_content is None:
        if st.button("⚡ Trigger auswürfeln", key="btn_trigger"):
            st.session_state.trigger_content = get_random_with_history(data['trigger'], st.session_state['hist_trigger'], is_dict=False)
            st.rerun()
    else:
        ct_t, ct_b = st.columns([8, 2])
        with ct_t:
            st.warning(st.session_state.trigger_content)
        with ct_b:
            if st.button("🔄", key="btn_re_trigger", help="Trigger neu auswürfeln"):
                st.session_state.trigger_content = get_random_with_history(data['trigger'], st.session_state['hist_trigger'], is_dict=False)
                st.rerun()

# Widerstand
with c_wid:
    st.markdown("**2. Der Widerstand (Meisner-Komponente)**")
    st.caption("Wie reagiert der imaginäre Partner während der Szene auf dich?")
    
    if st.session_state.widerstand_content is None:
        if st.button("🛡️ Widerstand auswürfeln", key="btn_widerstand"):
            st.session_state.widerstand_content = get_random_with_history(data['widerstand'], st.session_state['hist_widerstand'], is_dict=False)
            st.rerun()
    else:
        cw_t, cw_b = st.columns([8, 2])
        with cw_t:
            st.error(st.session_state.widerstand_content)
        with cw_b:
            if st.button("🔄", key="btn_re_widerstand", help="Widerstand neu auswürfeln"):
                st.session_state.widerstand_content = get_random_with_history(data['widerstand'], st.session_state['hist_widerstand'], is_dict=False)
                st.rerun()

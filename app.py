import streamlit as st
from supabase import create_client


# ============================================================
# CONFIGURAZIONE
# ============================================================

st.set_page_config(
    page_title="Delphi Study | Ponderazione KPI",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="collapsed",
)


@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["key"],
    )


supabase = get_supabase()


# ============================================================
# KPI
# ============================================================

KPIS = {
    "E1": {
        "area": "ENVIRONMENTAL",
        "nome": "Tasso di efficacia carbonica — Scope 1+2",
        "short": "Efficacia carbonica",
        "descrizione": (
            "Misura la variazione delle emissioni di gas serra Scope 1 e Scope 2 "
            "rispetto all'anno precedente. Permette di valutare se la performance "
            "emissiva dell'impresa è migliorata o peggiorata nel tempo."
        ),
    },
    "E2": {
        "area": "ENVIRONMENTAL",
        "nome": "Tasso di efficacia idrica",
        "short": "Efficacia idrica",
        "descrizione": (
            "Misura la variazione del consumo complessivo di acqua rispetto "
            "all'anno precedente. Permette di valutare il miglioramento o il "
            "peggioramento dell'impresa nella gestione della risorsa idrica."
        ),
    },
    "E3": {
        "area": "ENVIRONMENTAL",
        "nome": "Quota di energia rinnovabile",
        "short": "Energia rinnovabile",
        "descrizione": (
            "Misura la percentuale del consumo energetico complessivo "
            "dell'impresa coperta da energia proveniente da fonti rinnovabili."
        ),
    },
    "E4": {
        "area": "ENVIRONMENTAL",
        "nome": "Tasso di circolarità dei rifiuti",
        "short": "Circolarità dei rifiuti",
        "descrizione": (
            "Misura la percentuale dei rifiuti prodotti dall'impresa destinata "
            "a riciclo, riutilizzo o altre forme di recupero, anziché allo "
            "smaltimento."
        ),
    },
    "E5": {
        "area": "SUPPLY CHAIN ESG",
        "nome": "Copertura della valutazione di sostenibilità/ESG dei fornitori",
        "short": "Valutazione ESG dei fornitori",
        "descrizione": (
            "Misura la quota di fornitori sottoposta a processi di valutazione "
            "della sostenibilità, come screening ESG, questionari, assessment, "
            "audit o due diligence. Indica quanto estesamente l'impresa monitora "
            "i rischi e le performance di sostenibilità della propria catena "
            "di fornitura."
        ),
    },
    "S1": {
        "area": "SOCIAL",
        "nome": "Ore medie di formazione per dipendente",
        "short": "Formazione dei dipendenti",
        "descrizione": (
            "Misura il numero medio di ore di formazione erogate annualmente "
            "per dipendente e rappresenta l'impegno dell'impresa nello sviluppo "
            "e nell'aggiornamento delle competenze del personale."
        ),
    },
    "GS2": {
        "area": "SOCIAL",
        "nome": "Rappresentanza femminile nella workforce",
        "short": "Rappresentanza femminile",
        "descrizione": (
            "Misura la percentuale di donne sul totale dei dipendenti "
            "dell'impresa, come indicatore della rappresentanza femminile "
            "all'interno della forza lavoro."
        ),
    },
}


LIKERT = {
    1: "Per nulla rilevante",
    2: "Poco rilevante",
    3: "Moderatamente rilevante",
    4: "Molto rilevante",
    5: "Estremamente rilevante",
}

FAMILIARITA = {
    1: "Molto bassa",
    2: "Bassa",
    3: "Intermedia",
    4: "Elevata",
    5: "Molto elevata",
}


# ============================================================
# CSS
# ============================================================

CSS = """
<style>

html, body, .stApp,
[data-testid="stAppViewContainer"] {
    background: #F5F8F6 !important;
    color: #17352D !important;
}

.block-container {
    max-width: 940px !important;
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

#MainMenu, footer {
    visibility: hidden;
}

h1, h2, h3 {
    color: #17352D !important;
}

.stMarkdown p,
.stMarkdown li {
    color: #455E56;
    line-height: 1.7;
}

/* HERO */

.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #073C32 0%, #0C5748 60%, #19745F 100%);
    border-radius: 28px;
    padding: 55px;
    margin-bottom: 17px;
    box-shadow: 0 20px 50px rgba(7,60,50,.15);
}

.hero:after {
    content: "";
    position: absolute;
    width: 330px;
    height: 330px;
    border-radius: 50%;
    right: -110px;
    top: -190px;
    border: 1px solid rgba(255,255,255,.16);
    box-shadow:
        0 0 0 55px rgba(255,255,255,.025),
        0 0 0 110px rgba(255,255,255,.015);
}

.hero-eyebrow {
    position: relative;
    z-index: 2;
    color: #B9E5D9 !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .18em;
    margin-bottom: 20px;
}

.hero-title {
    position: relative;
    z-index: 2;
    color: #FFFFFF !important;
    font-size: 47px;
    line-height: 1.07;
    font-weight: 800;
    letter-spacing: -.035em;
    max-width: 690px;
}

.hero-description {
    position: relative;
    z-index: 2;
    color: #E5F3EE !important;
    font-size: 16px;
    line-height: 1.7;
    margin-top: 22px;
    max-width: 700px;
}

.academic-line {
    color: #687B74 !important;
    font-size: 12px;
    margin: 15px 6px 30px 6px;
}

/* PROGRESS */

.progress-label {
    color: #526A62 !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .12em;
    margin-bottom: 10px;
}

.progress-wrapper {
    display: flex;
    gap: 7px;
    margin-bottom: 38px;
}

.progress-segment {
    flex: 1;
    height: 5px;
    background: #D9E4DF;
    border-radius: 99px;
}

.progress-segment.active {
    background: #176D59;
}

/* SECTION */

.section-code {
    color: #176D59 !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .15em;
    margin-bottom: 8px;
}

.section-heading {
    color: #14352C !important;
    font-size: 34px;
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -.025em;
    margin-bottom: 10px;
}

.section-description {
    color: #5B7068 !important;
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 27px;
}

/* INFO */

.info-panel {
    background: #E9F3EF;
    border: 1px solid #D1E4DC;
    border-radius: 19px;
    padding: 25px 27px;
    margin: 25px 0;
    color: #284B41 !important;
}

.info-panel * {
    color: #284B41 !important;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.info-value {
    color: #073C32 !important;
    font-size: 29px;
    font-weight: 800;
}

.info-label {
    color: #60746D !important;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .08em;
    margin-top: 4px;
}

/* SCALE */

.scale-card {
    background: #FFFFFF;
    border: 1px solid #D9E5E0;
    border-radius: 18px;
    overflow: hidden;
    margin: 20px 0 27px 0;
    box-shadow: 0 5px 20px rgba(15,55,46,.035);
}

.scale-row {
    display: grid;
    grid-template-columns: 68px 1fr;
    align-items: center;
    min-height: 52px;
    border-bottom: 1px solid #E9EFEC;
}

.scale-row:last-child {
    border-bottom: none;
}

.scale-number {
    color: #126451 !important;
    font-size: 18px;
    font-weight: 800;
    text-align: center;
}

.scale-text {
    color: #405850 !important;
    font-size: 14px;
}

/* KPI */

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #D9E5E0;
    border-radius: 20px;
    padding: 29px 31px 26px 31px;
    margin: 31px 0 13px 0;
    box-shadow: 0 7px 25px rgba(15,55,46,.045);
}

.kpi-tag {
    display: inline-block;
    background: #E5F2ED;
    border: 1px solid #CEE5DC;
    color: #105845 !important;
    border-radius: 7px;
    padding: 6px 10px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .1em;
    margin-bottom: 15px;
}

.kpi-name {
    color: #102F27 !important;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -.02em;
    margin-bottom: 11px;
}

.kpi-description {
    color: #4D635C !important;
    font-size: 15px;
    line-height: 1.72;
}

/* RADIO */

[data-testid="stRadio"] {
    background: #FFFFFF;
    border: 1px solid #DFE9E5;
    border-radius: 16px;
    padding: 17px 19px 13px 19px;
    margin-bottom: 9px;
}

[data-testid="stRadio"] [role="radiogroup"] {
    gap: 16px !important;
}

[data-testid="stRadio"] label p {
    color: #28443B !important;
    font-weight: 600 !important;
}

[data-testid="stWidgetLabel"] p {
    color: #1E3A31 !important;
    font-weight: 650 !important;
}

/* INPUT */

[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #17352D !important;
}

[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: #17352D !important;
}

[data-testid="stNumberInput"] input {
    text-align: center;
    font-weight: 800;
}

/* TOTAL */

.total-panel {
    background: #E9F3EF;
    border: 1px solid #D1E4DC;
    border-radius: 18px;
    padding: 24px;
    margin: 27px 0;
    text-align: center;
}

.total-number {
    color: #073C32 !important;
    font-size: 36px;
    font-weight: 800;
}

.total-caption {
    color: #5B7068 !important;
    font-size: 12px;
    margin-top: 4px;
}

/* REVIEW */

.review-card {
    background: #FFFFFF;
    border: 1px solid #D9E5E0;
    border-radius: 16px;
    padding: 19px 21px;
    margin: 10px 0;
}

.review-name {
    color: #18352D !important;
    font-size: 14px;
    font-weight: 750;
}

.review-score {
    color: #126451 !important;
    font-size: 23px;
    font-weight: 800;
    margin-top: 5px;
}

.review-label {
    color: #687B74 !important;
    font-size: 12px;
    margin-top: 2px;
}

/* BUTTON */

.stButton > button {
    min-height: 52px !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    font-weight: 750 !important;
}

.stButton > button[kind="primary"] {
    background: #126451 !important;
    border: 1px solid #126451 !important;
    color: #FFFFFF !important;
    box-shadow: 0 5px 15px rgba(18,100,81,.14) !important;
}

.stButton > button[kind="primary"] * {
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover {
    background: #083F34 !important;
    border-color: #083F34 !important;
}

.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    border: 1px solid #C4D3CD !important;
    color: #173D33 !important;
}

/* SUCCESS */

.success-card {
    background: #FFFFFF;
    border: 1px solid #D9E5E0;
    border-radius: 26px;
    padding: 56px 40px;
    text-align: center;
    box-shadow: 0 15px 45px rgba(15,59,49,.07);
    margin-top: 45px;
}

.success-icon {
    width: 65px;
    height: 65px;
    border-radius: 50%;
    margin: 0 auto 22px auto;
    background: #E4F3EE;
    color: #126451 !important;
    font-size: 29px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
}

.success-title {
    color: #14352C !important;
    font-size: 31px;
    font-weight: 800;
    margin-bottom: 14px;
}

.success-text {
    color: #526860 !important;
    font-size: 15px;
    line-height: 1.72;
    max-width: 650px;
    margin: auto;
}

.success-badge {
    display: inline-block;
    background: #E6F2ED;
    color: #105744 !important;
    border-radius: 8px;
    padding: 8px 14px;
    margin-top: 25px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .09em;
}

@media (max-width: 700px) {

    .block-container {
        padding: 1rem 1rem 4rem 1rem !important;
    }

    .hero {
        padding: 36px 28px;
        border-radius: 21px;
    }

    .hero-title {
        font-size: 34px;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }
}

</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ============================================================
# RISULTATI AGGREGATI DEL ROUND 1
# ============================================================

ROUND1 = {
    "E1": {"mediana": 5, "iqr": 1.00, "peso": 17.00},
    "E2": {"mediana": 4, "iqr": 0.50, "peso": 13.29},
    "E3": {"mediana": 4, "iqr": 0.50, "peso": 14.86},
    "E4": {"mediana": 5, "iqr": 1.00, "peso": 14.71},
    "E5": {"mediana": 4, "iqr": 0.50, "peso": 13.57},
    "S1": {"mediana": 4, "iqr": 0.50, "peso": 14.14},
    "GS2": {"mediana": 4, "iqr": 1.00, "peso": 12.43},
}

# ============================================================
# SESSION STATE PERSISTENTE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "sending" not in st.session_state:
    st.session_state.sending = False
if "ratings" not in st.session_state:
    st.session_state.ratings = {}
if "weights" not in st.session_state:
    st.session_state.weights = {}
if "comment_saved" not in st.session_state:
    st.session_state.comment_saved = ""

# ============================================================
# FUNZIONI
# ============================================================

def go_to(page_number):
    st.session_state.page = page_number
    st.rerun()


def show_error(message):
    st.error(message, icon="⚠️")


def section_header(code, title, description):
    html = (
        f'<div class="section-code">{code}</div>'
        f'<div class="section-heading">{title}</div>'
        f'<div class="section-description">{description}</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def show_progress(current):
    labels = ["INTRODUZIONE", "RIVALUTAZIONE KPI", "PONDERAZIONE", "REVISIONE"]
    st.markdown(
        f'<div class="progress-label">STEP {current + 1} DI 4 · {labels[current]}</div>',
        unsafe_allow_html=True,
    )
    bars = "".join(
        f'<div class="progress-segment {"active" if i <= current else ""}"></div>'
        for i in range(4)
    )
    st.markdown(f'<div class="progress-wrapper">{bars}</div>', unsafe_allow_html=True)


def save_rating(codice):
    value = st.session_state.get(f"rating_widget_{codice}")
    if value is not None:
        st.session_state.ratings[codice] = int(value)


def sync_ratings():
    for codice in KPIS:
        value = st.session_state.get(f"rating_widget_{codice}")
        if value is not None:
            st.session_state.ratings[codice] = int(value)


def save_weight(codice):
    value = st.session_state.get(f"weight_widget_{codice}")
    if value is not None:
        st.session_state.weights[codice] = int(value)


def sync_weights():
    for codice in KPIS:
        value = st.session_state.get(f"weight_widget_{codice}")
        if value is not None:
            st.session_state.weights[codice] = int(value)


def save_comment():
    st.session_state.comment_saved = st.session_state.get("comment_widget", "")


def ratings_are_complete():
    return all(st.session_state.ratings.get(c) in LIKERT for c in KPIS)


def weights_are_complete():
    return all(st.session_state.weights.get(c) is not None for c in KPIS)


def weight_total():
    return sum(st.session_state.weights.get(c, 0) for c in KPIS)


def salva_risposta():
    data = {
        "rating_e1": st.session_state.ratings.get("E1"),
        "rating_e2": st.session_state.ratings.get("E2"),
        "rating_e3": st.session_state.ratings.get("E3"),
        "rating_e4": st.session_state.ratings.get("E4"),
        "rating_e5": st.session_state.ratings.get("E5"),
        "rating_s1": st.session_state.ratings.get("S1"),
        "rating_gs2": st.session_state.ratings.get("GS2"),
        "weight_e1": st.session_state.weights.get("E1"),
        "weight_e2": st.session_state.weights.get("E2"),
        "weight_e3": st.session_state.weights.get("E3"),
        "weight_e4": st.session_state.weights.get("E4"),
        "weight_e5": st.session_state.weights.get("E5"),
        "weight_s1": st.session_state.weights.get("S1"),
        "weight_gs2": st.session_state.weights.get("GS2"),
        "commento": st.session_state.comment_saved,
    }
    return supabase.table("delphi_round2").insert(data).execute()

# ============================================================
# HERO
# ============================================================

if not st.session_state.submitted:
    hero_html = (
        '<div class="hero">'
        '<div class="hero-eyebrow">DELPHI STUDY · ROUND 2</div>'
        '<div class="hero-title">Rivalutazione dei KPI<br>di sostenibilità</div>'
        '<div class="hero-description">'
        'Seconda fase della consultazione di esperti finalizzata alla definizione '
        'dei pesi di un sistema multidimensionale di indicatori di sostenibilità '
        'applicato al settore automotive.'
        '</div></div>'
        '<div class="academic-line">Ricerca accademica · Sapienza Università di Roma · Tesi di Laurea Magistrale</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

# ============================================================
# STEP 1 — INTRODUZIONE
# ============================================================

if st.session_state.page == 0 and not st.session_state.submitted:
    show_progress(0)
    section_header(
        "01 · INTRODUZIONE",
        "Secondo round della consultazione",
        "Il Round 2 consente di riesaminare le valutazioni alla luce dei risultati aggregati e anonimi emersi dal primo round.",
    )
    st.markdown(
        "Nel **Round 1 hanno partecipato 7 esperti**. In questa seconda fase vengono restituiti "
        "esclusivamente risultati aggregati del panel. Le valutazioni individuali restano anonime.\n\n"
        "Per ciascun KPI sono riportati la **mediana** e l'**intervallo interquartile (IQR)** "
        "dei giudizi di rilevanza, oltre al **peso medio** attribuito dal panel. Alla luce di queste "
        "informazioni, è possibile confermare o modificare liberamente il proprio giudizio."
    )
    st.markdown(
        '<div class="info-panel"><strong>Importante.</strong> Il feedback del panel ha funzione informativa: '
        'non è richiesto di uniformarsi alle valutazioni aggregate. Il secondo round serve a consentire '
        'una rivalutazione consapevole e indipendente.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Sintesi del Round 1")
    for codice, kpi in KPIS.items():
        r = ROUND1[codice]
        st.markdown(
            f"**{codice} · {kpi['short']}** — Mediana: **{r['mediana']}/5** · "
            f"IQR: **{r['iqr']:.2f}** · Peso medio: **{r['peso']:.2f}%**"
        )
    if st.button("Inizia il Round 2 →", type="primary", use_container_width=True):
        go_to(1)

# ============================================================
# STEP 2 — RIVALUTAZIONE KPI
# ============================================================

elif st.session_state.page == 1 and not st.session_state.submitted:
    show_progress(1)
    section_header(
        "02 · RIVALUTAZIONE",
        "Rilevanza dei KPI",
        "Rivaluti la rilevanza dei sette KPI considerando anche il feedback aggregato del Round 1.",
    )
    st.markdown(
        "Scala: **1 = Per nulla rilevante · 2 = Poco rilevante · 3 = Moderatamente rilevante · "
        "4 = Molto rilevante · 5 = Estremamente rilevante**"
    )
    for codice, kpi in KPIS.items():
        r = ROUND1[codice]
        st.markdown(
            '<div class="kpi-card">'
            f'<div class="kpi-tag">{codice} · {kpi["area"]}</div>'
            f'<div class="kpi-name">{kpi["nome"]}</div>'
            f'<div class="kpi-description">{kpi["descrizione"]}</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.info(
            f"Round 1 · Mediana: {r['mediana']}/5 · IQR: {r['iqr']:.2f} · Peso medio: {r['peso']:.2f}%",
            icon="📊",
        )
        key = f"rating_widget_{codice}"
        if key not in st.session_state and st.session_state.ratings.get(codice) is not None:
            st.session_state[key] = st.session_state.ratings[codice]
        st.radio(
            f"Quanto ritiene rilevante il KPI {codice} nel Round 2? *",
            options=[1, 2, 3, 4, 5], index=None, horizontal=True,
            format_func=lambda x: f"{x} · {LIKERT[x]}", key=key,
            on_change=save_rating, args=(codice,),
        )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Indietro", use_container_width=True):
            sync_ratings(); go_to(0)
    with c2:
        if st.button("Continua →", type="primary", use_container_width=True):
            sync_ratings()
            missing = [c for c in KPIS if st.session_state.ratings.get(c) not in LIKERT]
            if missing:
                show_error("È necessario valutare tutti i KPI. Mancano: " + ", ".join(missing) + ".")
            else:
                go_to(2)

# ============================================================
# STEP 3 — PONDERAZIONE
# ============================================================

elif st.session_state.page == 2 and not st.session_state.submitted:
    show_progress(2)
    section_header(
        "03 · PONDERAZIONE",
        "Attribuzione finale dei pesi",
        "Ridistribuisca 100 punti tra i sette KPI considerando il feedback aggregato del Round 1.",
    )
    st.markdown(
        '<div class="info-panel">I valori riportati accanto a ciascun KPI rappresentano il '
        '<strong>peso medio attribuito dal panel nel Round 1</strong>. Può confermare una distribuzione '
        'simile oppure modificarla secondo il Suo giudizio. La somma finale deve essere esattamente '
        '<strong>100 punti</strong>.</div>', unsafe_allow_html=True,
    )
    for codice, kpi in KPIS.items():
        r = ROUND1[codice]
        col_name, col_value = st.columns([4, 1])
        with col_name:
            st.markdown(f"**{codice} · {kpi['short']}**")
            st.caption(f"Peso medio Round 1: {r['peso']:.2f}%")
        with col_value:
            key = f"weight_widget_{codice}"
            if key not in st.session_state and st.session_state.weights.get(codice) is not None:
                st.session_state[key] = st.session_state.weights[codice]
            st.number_input(
                f"Punti {codice}", min_value=0, max_value=100, value=None, step=1,
                placeholder="0", key=key, label_visibility="collapsed",
                on_change=save_weight, args=(codice,),
            )
    sync_weights()
    total = weight_total()
    if total == 100:
        st.success("Totale attribuito: 100 / 100 ✓")
    elif total < 100:
        st.info(f"Totale attribuito: {total} / 100 · Restano {100-total} punti da distribuire.")
    else:
        st.error(f"Totale attribuito: {total} / 100 · Ridurre di {total-100} punti.")
    st.text_area(
        "Motivazione / osservazioni (facoltativo)",
        value=st.session_state.comment_saved,
        key="comment_widget",
        on_change=save_comment,
        placeholder="Eventuali osservazioni sulla rivalutazione o sulla ponderazione dei KPI...",
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Indietro", use_container_width=True):
            sync_weights(); save_comment(); go_to(1)
    with c2:
        if st.button("Continua →", type="primary", use_container_width=True):
            sync_weights(); save_comment()
            if not weights_are_complete():
                show_error("È necessario attribuire un valore a tutti i KPI.")
            elif weight_total() != 100:
                show_error("La somma dei pesi deve essere esattamente pari a 100.")
            else:
                go_to(3)

# ============================================================
# STEP 4 — REVISIONE E INVIO
# ============================================================

elif st.session_state.page == 3 and not st.session_state.submitted:
    show_progress(3)
    section_header(
        "04 · REVISIONE",
        "Riepilogo della valutazione",
        "Verifichi le risposte prima dell'invio definitivo del Round 2.",
    )
    st.markdown("### Rilevanza dei KPI")
    for codice, kpi in KPIS.items():
        score = st.session_state.ratings.get(codice)
        label = LIKERT.get(score, "Valutazione mancante")
        st.markdown(f"**{codice} · {kpi['short']}** — **{score if score else '—'} / 5** · {label}")
    st.markdown("### Pesi attribuiti")
    for codice, kpi in KPIS.items():
        weight = st.session_state.weights.get(codice)
        st.markdown(f"**{codice} · {kpi['short']}** — **{weight if weight is not None else '—'} punti**")
    st.success(f"Totale attribuito: {weight_total()} / 100 ✓" if weight_total() == 100 else f"Totale: {weight_total()} / 100")
    if st.session_state.comment_saved.strip():
        st.markdown("### Motivazione / osservazioni")
        st.write(st.session_state.comment_saved)
    st.divider()
    st.markdown("Con l'invio, le risposte saranno considerate definitive per il **Round 2 della consultazione Delphi**.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Modifica risposte", use_container_width=True):
            go_to(2)
    with c2:
        if st.button("Invia valutazione", type="primary", use_container_width=True, disabled=st.session_state.sending):
            if not ratings_are_complete():
                show_error("Una o più valutazioni di rilevanza risultano mancanti.")
            elif not weights_are_complete():
                show_error("È necessario attribuire un valore a tutti i KPI.")
            elif weight_total() != 100:
                show_error("La somma dei pesi deve essere esattamente pari a 100.")
            else:
                st.session_state.sending = True
                try:
                    salva_risposta()
                    st.session_state.submitted = True
                    st.session_state.sending = False
                    st.rerun()
                except Exception as e:
                    st.session_state.sending = False
                    st.error("Non è stato possibile registrare la risposta. La valutazione non è stata inviata. La preghiamo di riprovare.")
                    st.exception(e)

# ============================================================
# PAGINA FINALE
# ============================================================

if st.session_state.submitted:
    success_html = (
        '<div class="success-card">'
        '<div class="success-icon">✓</div>'
        '<div class="section-code">DELPHI STUDY · ROUND 2</div>'
        '<div class="success-title">Grazie per il Suo contributo.</div>'
        '<div class="success-text">La rivalutazione è stata completata correttamente.<br><br>'
        'Le risposte del secondo round saranno analizzate in forma aggregata per verificare '
        'la convergenza dei giudizi e determinare i pesi finali degli indicatori.</div>'
        '<div class="success-badge">ROUND 2 · COMPLETATO</div>'
        '</div>'
    )
    st.markdown(success_html, unsafe_allow_html=True)

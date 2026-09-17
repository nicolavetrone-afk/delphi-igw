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


# ============================================================
# SCALE
# ============================================================

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
    background: linear-gradient(
        135deg,
        #073C32 0%,
        #0C5748 60%,
        #19745F 100%
    );
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


/* TITOLI SEZIONE */

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


/* SCALA */

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
    transition: all .15s ease !important;
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

.stButton > button[kind="secondary"] * {
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


/* MOBILE */

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
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = 0

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "ratings" not in st.session_state:
    st.session_state.ratings = {}

if "weights" not in st.session_state:
    st.session_state.weights = {}


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

    labels = [
        "INTRODUZIONE",
        "PROFILO",
        "VALUTAZIONE KPI",
        "PONDERAZIONE",
        "REVISIONE",
    ]

    st.markdown(
        '<div class="progress-label">'
        f'STEP {current + 1} DI 5 · {labels[current]}'
        '</div>',
        unsafe_allow_html=True,
    )

    bars = ""

    for i in range(5):

        css_class = (
            "progress-segment active"
            if i <= current
            else "progress-segment"
        )

        bars += f'<div class="{css_class}"></div>'

    st.markdown(
        '<div class="progress-wrapper">'
        + bars
        + '</div>',
        unsafe_allow_html=True,
    )


def save_rating(codice):

    widget_key = f"rating_widget_{codice}"

    value = st.session_state.get(widget_key)

    if value is not None:
        st.session_state.ratings[codice] = int(value)


def save_weight(codice):

    widget_key = f"weight_widget_{codice}"

    value = st.session_state.get(widget_key)

    if value is not None:
        st.session_state.weights[codice] = int(value)


def sync_ratings():

    for codice in KPIS:

        value = st.session_state.get(
            f"rating_widget_{codice}"
        )

        if value is not None:
            st.session_state.ratings[codice] = int(value)


def sync_weights():

    for codice in KPIS:

        value = st.session_state.get(
            f"weight_widget_{codice}"
        )

        if value is not None:
            st.session_state.weights[codice] = int(value)


def salva_risposta():

    data = {
        "ambiti": "; ".join(
            st.session_state.get("ambiti", [])
        ),
        "anni_esperienza": st.session_state.get(
            "anni",
            "",
        ),
        "familiarita_esg": st.session_state.get(
            "familiarita"
        ),
        "esperienza_automotive": st.session_state.get(
            "automotive",
            "",
        ),

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

        "commento": st.session_state.get(
            "commento",
            "",
        ),
    }

    result = (
        supabase
        .table("delphi_responses")
        .insert(data)
        .execute()
    )

    return result


# ============================================================
# HERO
# ============================================================

if not st.session_state.submitted:

    hero_html = (
        '<div class="hero">'
        '<div class="hero-eyebrow">DELPHI STUDY · ROUND 1</div>'
        '<div class="hero-title">'
        'Ponderazione dei KPI<br>'
        'di sostenibilità'
        '</div>'
        '<div class="hero-description">'
        'Consultazione di esperti finalizzata alla definizione '
        'dei pesi di un sistema multidimensionale di indicatori '
        'di sostenibilità applicato al settore automotive.'
        '</div>'
        '</div>'
        '<div class="academic-line">'
        'Ricerca accademica · Sapienza Università di Roma · '
        'Laurea Magistrale in Ingegneria Gestionale'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )

    show_progress(st.session_state.page)


# ============================================================
# STEP 1 — INTRODUZIONE
# ============================================================

if st.session_state.page == 0 and not st.session_state.submitted:

    section_header(
        "01 · INTRODUZIONE",
        "Benvenuto/a",
        "Prima di iniziare, La invitiamo a leggere brevemente "
        "le finalità e le modalità della consultazione.",
    )

    st.markdown(
        "Gentile Esperto/a,\n\n"
        "il presente questionario è parte di una **ricerca accademica** "
        "finalizzata allo sviluppo di un modello quantitativo per "
        "l'analisi della sostenibilità aziendale nel **settore automotive**.\n\n"
        "Nell'ambito della ricerca sono stati individuati **sette Key "
        "Performance Indicators (KPI)** relativi a differenti dimensioni "
        "della sostenibilità.\n\n"
        "L'obiettivo della consultazione è supportare la definizione dei "
        "**pesi da attribuire ai sette KPI**, sulla base del giudizio di "
        "un panel di esperti in sostenibilità, ESG e ambiti correlati.\n\n"
        "La consultazione segue un'impostazione **Delphi**. In questo primo "
        "round Le viene richiesto di formulare una valutazione individuale "
        "e indipendente. Le risposte saranno successivamente elaborate "
        "in forma aggregata.\n\n"
        "**Non esistono risposte corrette o errate:** ciò che interessa "
        "è il Suo giudizio professionale."
    )

    info_html = (
        '<div class="info-panel">'
        '<div class="info-grid">'
        '<div>'
        '<div class="info-value">5–7</div>'
        '<div class="info-label">MINUTI STIMATI</div>'
        '</div>'
        '<div>'
        '<div class="info-value">7</div>'
        '<div class="info-label">KPI DA VALUTARE</div>'
        '</div>'
        '<div>'
        '<div class="info-value">1–5</div>'
        '<div class="info-label">SCALA DI RILEVANZA</div>'
        '</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        info_html,
        unsafe_allow_html=True,
    )

    consenso = st.checkbox(
        "Ho letto le informazioni sopra riportate e acconsento "
        "a partecipare alla consultazione.",
        key="consenso",
    )

    st.caption("* Conferma obbligatoria.")

    if st.button(
        "Inizia la consultazione →",
        type="primary",
        use_container_width=True,
    ):

        if not consenso:

            show_error(
                "Per proseguire è necessario "
                "confermare la partecipazione."
            )

        else:

            go_to(1)


# ============================================================
# STEP 2 — PROFILO
# ============================================================

elif st.session_state.page == 1 and not st.session_state.submitted:

    section_header(
        "02 · PROFILO",
        "Profilo dell'esperto",
        "Le informazioni richieste saranno utilizzate esclusivamente "
        "per descrivere in forma aggregata la composizione del panel.",
    )

    st.caption(
        "* Tutte le domande di questa sezione sono obbligatorie."
    )

    ambiti = st.multiselect(
        "Ambito/i principale/i di competenza *",
        [
            "Sustainability / ESG",
            "Environmental Sustainability",
            "Social Sustainability",
            "ESG / Sustainability Reporting",
            "Sustainable Finance",
            "Sustainable Supply Chain / Procurement",
            "Corporate Governance",
            "Automotive / Mobility",
            "Ricerca accademica",
            "Altro",
        ],
        key="ambiti",
    )

    anni = st.selectbox(
        "Anni di esperienza professionale o accademica "
        "in sostenibilità/ESG o ambiti correlati *",
        [
            "Selezionare...",
            "Meno di 2 anni",
            "2–5 anni",
            "6–10 anni",
            "11–15 anni",
            "Oltre 15 anni",
        ],
        key="anni",
    )

    familiarita = st.radio(
        "Livello di familiarità con la misurazione "
        "delle performance ESG/sostenibilità *",
        options=[1, 2, 3, 4, 5],
        index=None,
        horizontal=True,
        format_func=lambda x: f"{x} · {FAMILIARITA[x]}",
        key="familiarita",
    )

    automotive = st.selectbox(
        "Esperienza o conoscenza del settore automotive *",
        [
            "Selezionare...",
            "Esperienza professionale diretta",
            "Conoscenza professionale o accademica",
            "Conoscenza generale",
            "Nessuna esperienza specifica",
        ],
        key="automotive",
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Indietro",
            use_container_width=True,
        ):

            go_to(0)

    with col2:

        if st.button(
            "Continua →",
            type="primary",
            use_container_width=True,
        ):

            errors = []

            if not ambiti:
                errors.append(
                    "selezionare almeno un ambito di competenza"
                )

            if anni == "Selezionare...":
                errors.append(
                    "indicare gli anni di esperienza"
                )

            if familiarita is None:
                errors.append(
                    "indicare il livello di familiarità ESG"
                )

            if automotive == "Selezionare...":
                errors.append(
                    "indicare la conoscenza del settore automotive"
                )

            if errors:

                show_error(
                    "Per continuare è necessario "
                    + "; ".join(errors)
                    + "."
                )

            else:

                go_to(2)


# ============================================================
# STEP 3 — VALUTAZIONE KPI
# ============================================================

elif st.session_state.page == 2 and not st.session_state.submitted:

    section_header(
        "03 · VALUTAZIONE",
        "Rilevanza dei KPI",
        "Considerando le caratteristiche del settore automotive, "
        "valuti quanto ciascun KPI sia rilevante nel rappresentare "
        "la performance di sostenibilità di un'impresa.",
    )

    st.markdown(
        "Per ciascun indicatore utilizzi la seguente "
        "**scala di rilevanza a 5 punti**."
    )

    scale_html = (
        '<div class="scale-card">'
        '<div class="scale-row">'
        '<div class="scale-number">1</div>'
        '<div class="scale-text">Per nulla rilevante</div>'
        '</div>'
        '<div class="scale-row">'
        '<div class="scale-number">2</div>'
        '<div class="scale-text">Poco rilevante</div>'
        '</div>'
        '<div class="scale-row">'
        '<div class="scale-number">3</div>'
        '<div class="scale-text">Moderatamente rilevante</div>'
        '</div>'
        '<div class="scale-row">'
        '<div class="scale-number">4</div>'
        '<div class="scale-text">Molto rilevante</div>'
        '</div>'
        '<div class="scale-row">'
        '<div class="scale-number">5</div>'
        '<div class="scale-text">Estremamente rilevante</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        scale_html,
        unsafe_allow_html=True,
    )

    st.caption(
        "Tutte le valutazioni sono obbligatorie. "
        "Nessuna risposta è preselezionata."
    )

    for codice, kpi in KPIS.items():

        kpi_html = (
            '<div class="kpi-card">'
            f'<div class="kpi-tag">{codice} · {kpi["area"]}</div>'
            f'<div class="kpi-name">{kpi["nome"]}</div>'
            f'<div class="kpi-description">{kpi["descrizione"]}</div>'
            '</div>'
        )

        st.markdown(
            kpi_html,
            unsafe_allow_html=True,
        )

        widget_key = f"rating_widget_{codice}"

        if (
            widget_key not in st.session_state
            and codice in st.session_state.ratings
        ):
            st.session_state[widget_key] = (
                st.session_state.ratings[codice]
            )

        st.radio(
            f"Quanto ritiene rilevante il KPI {codice}? *",
            options=[1, 2, 3, 4, 5],
            index=None,
            horizontal=True,
            format_func=lambda x: f"{x} · {LIKERT[x]}",
            key=widget_key,
            on_change=save_rating,
            args=(codice,),
        )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Indietro",
            use_container_width=True,
        ):

            sync_ratings()
            go_to(1)

    with col2:

        if st.button(
            "Continua →",
            type="primary",
            use_container_width=True,
        ):

            sync_ratings()

            missing = [
                codice
                for codice in KPIS
                if st.session_state.ratings.get(codice) not in LIKERT
            ]

            if missing:

                show_error(
                    "È necessario valutare tutti i KPI. "
                    "Mancano: "
                    + ", ".join(missing)
                    + "."
                )

            else:

                go_to(3)


# ============================================================
# STEP 4 — PONDERAZIONE
# ============================================================

elif st.session_state.page == 3 and not st.session_state.submitted:

    section_header(
        "04 · PONDERAZIONE",
        "Attribuzione dei pesi",
        "Consideri ora i sette KPI contemporaneamente e ne valuti "
        "l'importanza relativa ai fini della costruzione "
        "dell'indice complessivo.",
    )

    weight_info_html = (
        '<div class="info-panel">'
        'Distribuisca <strong>100 punti complessivi</strong> '
        'tra i sette KPI. Un numero maggiore di punti indica '
        'che, secondo il Suo giudizio, quel KPI dovrebbe avere '
        'un peso maggiore nella valutazione complessiva della '
        'performance di sostenibilità.'
        '<br><br>'
        '<strong>La somma finale deve essere esattamente '
        'pari a 100.</strong>'
        '</div>'
    )

    st.markdown(
        weight_info_html,
        unsafe_allow_html=True,
    )

    for codice, kpi in KPIS.items():

        col_name, col_value = st.columns([4, 1])

        with col_name:

            st.markdown(
                f"**{codice} · {kpi['short']}**"
            )

            st.caption(
                kpi["nome"]
            )

        with col_value:

            widget_key = f"weight_widget_{codice}"

            if (
                widget_key not in st.session_state
                and codice in st.session_state.weights
            ):
                st.session_state[widget_key] = (
                    st.session_state.weights[codice]
                )

            st.number_input(
                f"Punti {codice}",
                min_value=0,
                max_value=100,
                value=None,
                step=1,
                placeholder="0",
                key=widget_key,
                label_visibility="collapsed",
                on_change=save_weight,
                args=(codice,),
            )

    sync_weights()

    total = sum(
        st.session_state.weights.get(codice, 0)
        for codice in KPIS
    )

    if total == 100:

        total_html = (
            '<div class="total-panel">'
            '<div class="total-number">100 / 100 ✓</div>'
            '<div class="total-caption">'
            'Distribuzione completata correttamente'
            '</div>'
            '</div>'
        )

        st.markdown(
            total_html,
            unsafe_allow_html=True,
        )

    elif total < 100:

        remaining = 100 - total

        total_html = (
            '<div class="total-panel">'
            f'<div class="total-number">{total} / 100</div>'
            '<div class="total-caption">'
            f'Restano da assegnare {remaining} punti'
            '</div>'
            '</div>'
        )

        st.markdown(
            total_html,
            unsafe_allow_html=True,
        )

    else:

        st.error(
            f"Sono stati assegnati {total} punti. "
            f"È necessario rimuovere {total - 100} punti."
        )

    st.markdown("### Motivazione e osservazioni")

    st.text_area(
        "Se lo desidera, può motivare brevemente i pesi attribuiti "
        "o aggiungere osservazioni utili ai fini della ricerca.",
        placeholder=(
            "Ad esempio: motivazioni relative ai pesi attribuiti, "
            "specificità del settore automotive o considerazioni "
            "sulla rilevanza degli indicatori..."
        ),
        height=145,
        key="commento",
    )

    st.caption("Campo facoltativo.")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Indietro",
            use_container_width=True,
        ):

            sync_weights()
            go_to(2)

    with col2:

        if st.button(
            "Rivedi le risposte →",
            type="primary",
            use_container_width=True,
        ):

            sync_weights()

            missing_weights = [
                codice
                for codice in KPIS
                if st.session_state.get(
                    f"weight_widget_{codice}"
                ) is None
            ]

            final_total = sum(
                st.session_state.weights.get(codice, 0)
                for codice in KPIS
            )

            if missing_weights:

                show_error(
                    "È necessario attribuire un valore "
                    "a tutti i sette KPI. "
                    "Mancano: "
                    + ", ".join(missing_weights)
                    + "."
                )

            elif final_total != 100:

                show_error(
                    "La somma dei pesi deve essere "
                    "esattamente pari a 100."
                )

            else:

                go_to(4)


# ============================================================
# STEP 5 — REVISIONE
# ============================================================

elif st.session_state.page == 4 and not st.session_state.submitted:

    # Sincronizzazione preventiva dei dati
    sync_ratings()
    sync_weights()

    section_header(
        "05 · REVISIONE",
        "Riepilogo della valutazione",
        "Controlli le risposte prima dell'invio definitivo. "
        "È ancora possibile tornare indietro e modificarle.",
    )

    st.markdown("### Rilevanza dei KPI")

    for codice, kpi in KPIS.items():

        score = st.session_state.ratings.get(codice)

        if score in LIKERT:

            score_text = f"{score} / 5"
            label_text = LIKERT[score]

        else:

            score_text = "Non compilato"
            label_text = "Valutazione mancante"

        review_html = (
            '<div class="review-card">'
            f'<div class="review-name">'
            f'{codice} · {kpi["short"]}'
            '</div>'
            f'<div class="review-score">{score_text}</div>'
            f'<div class="review-label">{label_text}</div>'
            '</div>'
        )

        st.markdown(
            review_html,
            unsafe_allow_html=True,
        )

    st.markdown("### Pesi attribuiti")

    final_total = 0

    for codice, kpi in KPIS.items():

        weight = st.session_state.weights.get(
            codice
        )

        if weight is None:
            weight_text = "Non compilato"
        else:
            weight_text = f"{weight} punti"
            final_total += weight

        st.write(
            f"**{codice} · {kpi['short']}** — "
            f"**{weight_text}**"
        )

    if final_total == 100:

        st.success(
            "Totale attribuito: 100 / 100 ✓"
        )

    else:

        st.warning(
            f"Totale attribuito: {final_total} / 100"
        )

    comment = st.session_state.get(
        "commento",
        "",
    )

    if comment:

        st.markdown(
            "### Motivazione / osservazioni"
        )

        st.write(comment)

    st.divider()

    st.markdown(
        "Con l'invio, le risposte saranno considerate definitive "
        "per il **Round 1 della consultazione Delphi**."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Modifica risposte",
            use_container_width=True,
        ):

            go_to(3)

    with col2:

        if st.button(
            "Invia valutazione",
            type="primary",
            use_container_width=True,
        ):

            # Sincronizzazione finale prima del controllo
            sync_ratings()
            sync_weights()

            # Verifica dei rating
            ratings_complete = all(
                st.session_state.ratings.get(codice) in LIKERT
                for codice in KPIS
            )

            # Verifica dei pesi
            weights_complete = all(
                st.session_state.weights.get(codice) is not None
                for codice in KPIS
            )

            # Totale finale dei pesi
            final_total = sum(
                st.session_state.weights.get(codice, 0)
                for codice in KPIS
            )

            if not ratings_complete:

                show_error(
                    "Una o più valutazioni di rilevanza "
                    "risultano mancanti."
                )

            elif not weights_complete:

                show_error(
                    "È necessario attribuire un valore "
                    "a tutti i KPI."
                )

            elif final_total != 100:

                show_error(
                    "La somma dei pesi deve essere "
                    "esattamente pari a 100."
                )

            else:

                try:

                    salva_risposta()

                    st.session_state.submitted = True

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Non è stato possibile registrare la risposta. "
                        "La valutazione non è stata inviata. "
                        "La preghiamo di riprovare."
                    )

                    st.exception(e)


# ============================================================
# PAGINA FINALE
# ============================================================

if st.session_state.submitted:

    success_html = (
        '<div class="success-card">'
        '<div class="success-icon">✓</div>'
        '<div class="section-code">'
        'DELPHI STUDY · ROUND 1'
        '</div>'
        '<div class="success-title">'
        'Grazie per il Suo contributo.'
        '</div>'
        '<div class="success-text">'
        'La valutazione è stata completata correttamente.'
        '<br><br>'
        'Le risposte del panel saranno analizzate in forma aggregata. '
        'I risultati del primo round saranno utilizzati per valutare '
        'il grado di convergenza tra i giudizi degli esperti e per '
        'la successiva definizione dei pesi degli indicatori.'
        '</div>'
        '<div class="success-badge">'
        'ROUND 1 · COMPLETATO'
        '</div>'
        '</div>'
    )

    st.markdown(
        success_html,
        unsafe_allow_html=True,
    )

import html
import json
import os
import re

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

# ----------------------------- Page setup -----------------------------
st.set_page_config(
    page_title="Nyaya AI | Indian Legal Information",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# ----------------------------- Styling -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --navy: #10233f;
        --navy-mid: #183a61;
        --gold: #d6a84f;
        --ink: #1b2a41;
        --muted: #66758b;
        --line: #e1e7ef;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 92% 0%, rgba(214,168,79,.10), transparent 25rem),
            linear-gradient(180deg, #f8fafd 0%, #f1f5fa 100%);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(248,250,253,.92);
    }

    .block-container {
        max-width: 1220px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10233f 0%, #18365b 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }

    [data-testid="stSidebar"] * {
        color: #f5f7fb;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.18);
    }

    .sidebar-brand {
        font-family: 'Manrope', sans-serif;
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: .2rem;
    }

    .sidebar-subtitle {
        color: #d2deec;
        font-size: .83rem;
        line-height: 1.6;
    }

    .hero {
        position: relative;
        isolation: isolate;
        overflow: hidden;
        box-sizing: border-box;
        width: 100%;
        padding: clamp(1.6rem, 4vw, 3rem);
        border-radius: 24px;
        background: linear-gradient(125deg, #10233f 0%, #183a61 58%, #244d76 100%);
        box-shadow: 0 18px 42px rgba(16,35,63,.16);
        margin-bottom: 2.1rem;
    }

    .hero::before {
        content: "";
        position: absolute;
        width: 320px;
        height: 320px;
        right: -125px;
        top: -165px;
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 50%;
        box-shadow:
            0 0 0 28px rgba(255,255,255,.025),
            0 0 0 58px rgba(255,255,255,.025),
            0 0 0 88px rgba(255,255,255,.02);
        z-index: -1;
        pointer-events: none;
    }

    .hero-content {
        position: relative;
        max-width: 900px;
    }

    .hero-badge {
        color: #f1ca78;
        font-size: .74rem;
        font-weight: 800;
        letter-spacing: .16em;
        line-height: 1.8;
        margin-bottom: 1.25rem;
    }

    .hero-title {
        color: #fff !important;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 4.2vw, 3.25rem) !important;
        font-weight: 800 !important;
        line-height: 1.17 !important;
        letter-spacing: -.035em;
        margin: 0 0 1.1rem !important;
        padding: 0 !important;
    }

    .hero-title span {
        display: block;
        color: #e3b95d;
    }

    .hero-description {
        color: #e0e8f2 !important;
        font-size: clamp(.98rem, 1.6vw, 1.08rem);
        line-height: 1.85;
        max-width: 740px;
        margin: 0;
    }

    .hero-features {
        display: flex;
        flex-wrap: wrap;
        gap: .6rem;
        margin-top: 1.6rem;
    }

    .hero-feature {
        color: #fff;
        background: rgba(255,255,255,.09);
        border: 1px solid rgba(255,255,255,.16);
        border-radius: 999px;
        padding: .55rem .8rem;
        font-size: .77rem;
        font-weight: 600;
    }

    .section-label {
        color: #9a7128;
        font-size: .73rem;
        font-weight: 800;
        letter-spacing: .16em;
        margin: .35rem 0 .45rem;
    }

    .section-title {
        color: #10233f;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(1.4rem, 2.5vw, 1.75rem);
        font-weight: 800;
        letter-spacing: -.025em;
        line-height: 1.35;
        margin: 0 0 .4rem;
    }

    .section-subtitle {
        color: #66758b;
        font-size: .92rem;
        line-height: 1.75;
        margin: 0 0 1.25rem;
    }

    .topic-card {
        box-sizing: border-box;
        background: rgba(255,255,255,.96);
        border: 1px solid #e1e7ef;
        border-radius: 16px;
        padding: 1.2rem;
        min-height: 165px;
        margin-bottom: .85rem;
        box-shadow: 0 5px 18px rgba(16,35,63,.04);
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .topic-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 26px rgba(16,35,63,.09);
    }

    .topic-icon {
        font-size: 1.7rem;
        margin-bottom: .7rem;
    }

    .topic-title {
        color: #10233f;
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: .4rem;
    }

    .topic-description {
        color: #66758b;
        font-size: .84rem;
        line-height: 1.65;
    }

    .privacy-notice {
        color: #72551c;
        background: #fff8e9;
        border: 1px solid #f0dfb7;
        border-left: 4px solid #d6a84f;
        border-radius: 10px;
        padding: .85rem 1rem;
        font-size: .84rem;
        line-height: 1.7;
        margin: .2rem 0 1rem;
    }

    .stTextArea textarea {
        background: #fff !important;
        color: #1b2a41 !important;
        border: 1px solid #dce3ed !important;
        border-radius: 13px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        line-height: 1.65 !important;
        box-shadow: none !important;
    }

    .stTextArea textarea:focus {
        border-color: #bd9140 !important;
        box-shadow: 0 0 0 3px rgba(214,168,79,.15) !important;
    }

    .stFormSubmitButton > button {
        background: linear-gradient(110deg, #c8993e, #e0b95e) !important;
        color: #10233f !important;
        border: 0 !important;
        border-radius: 11px !important;
        min-height: 3.1rem;
        font-weight: 800 !important;
        box-shadow: 0 8px 18px rgba(190,143,52,.18);
    }

    .stFormSubmitButton > button:hover {
        filter: brightness(1.04);
        transform: translateY(-1px);
    }

    .result-card {
        background: #fff;
        border: 1px solid #e1e7ef;
        border-radius: 15px;
        padding: 1.1rem 1.2rem;
        margin: .45rem 0 .85rem;
        box-shadow: 0 6px 20px rgba(16,35,63,.035);
        overflow-wrap: anywhere;
    }

    .result-card h3 {
        color: #10233f;
        font-size: 1rem;
        margin: 0 0 .7rem;
    }

    .category-pill {
        display: inline-block;
        background: #edf3fb;
        color: #244d76;
        border: 1px solid #d7e4f5;
        border-radius: 999px;
        padding: .4rem .75rem;
        font-size: .84rem;
        font-weight: 700;
    }

    .keyword {
        display: inline-block;
        margin: .18rem .22rem .18rem 0;
        padding: .36rem .65rem;
        border-radius: 999px;
        background: #fbf4e5;
        color: #79591c;
        border: 1px solid #efdfb9;
        font-size: .81rem;
        font-weight: 700;
    }

    .notice {
        background: #fff8e9;
        border: 1px solid #f0dba8;
        border-left: 4px solid #d6a84f;
        border-radius: 12px;
        padding: .95rem 1rem;
        color: #6b531f;
        font-size: .87rem;
        line-height: 1.7;
        margin-top: 1rem;
    }

    div[data-testid="stExpander"] {
        background: #fff;
        border: 1px solid #e1e7ef;
        border-radius: 13px;
        overflow: hidden;
    }

    .footer {
        background: linear-gradient(125deg, #10233f, #244d76);
        color: #dce6f2;
        text-align: center;
        padding: 1.8rem 1rem;
        border-radius: 18px;
        margin-top: 3rem;
        line-height: 1.8;
    }

    .footer strong {
        color: #fff;
    }

    @media (max-width: 640px) {
        .hero { padding: 1.5rem; border-radius: 18px; }
        .hero::before { right: -220px; }
        .hero-feature { font-size: .7rem; padding: .45rem .65rem; }
        .topic-card { padding: 1rem; min-height: 150px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- Sidebar -----------------------------
with st.sidebar:
    st.markdown("<div style='font-size:2.3rem'>⚖️</div>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-brand">Nyaya AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-subtitle">AI-Powered Indian Legal Information Assistant</div>',
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("### Explore legal topics")
    st.markdown(
        "🏛️ Constitution & rights\n\n"
        "📜 Criminal law: IPC / BNS\n\n"
        "🛡️ Cybercrime & digital safety\n\n"
        "👮 FIR & police complaints\n\n"
        "🧾 Consumer protection\n\n"
        "⚖️ Court procedures"
    )
    st.divider()
    st.markdown("### How it works")
    st.markdown(
        "1. Describe your question in plain language.\n"
        "2. Submit it for AI analysis.\n"
        "3. Review the structured information.\n"
        "4. Verify important details with official sources."
    )
    st.divider()
    st.caption(
        "Avoid sharing names, addresses, phone numbers, case numbers "
        "or confidential documents."
    )

# ----------------------------- Hero section -----------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="hero-badge">
                ⚖️ &nbsp; AI-POWERED LEGAL INFORMATION
            </div>
            <h1 class="hero-title">
                Understand your legal options
                <span>with clarity.</span>
            </h1>
            <p class="hero-description">
                Ask questions about Indian laws, police procedures,
                cybercrime, consumer rights and court processes.
                Get a structured starting point to understand
                possible legal options and next steps.
            </p>
            <div class="hero-features">
                <div class="hero-feature">🇮🇳 Indian Legal System</div>
                <div class="hero-feature">🤖 Generative AI</div>
                <div class="hero-feature">📋 Structured Analysis</div>
                <div class="hero-feature">🛡️ Victim Guidance</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- Knowledge areas -----------------------------
st.markdown('<div class="section-label">KNOWLEDGE AREAS</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-title">What can I help you understand?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-subtitle">Explore common legal topics or describe your situation below.</div>',
    unsafe_allow_html=True,
)

topics = [
    ("🏛️", "Constitution", "Fundamental rights, constitutional provisions and protections."),
    ("🛡️", "Cybercrime", "Online fraud, cyber abuse and digital safety."),
    ("📜", "IPC & BNS", "Criminal offences, legal provisions and consequences."),
    ("🧾", "Consumer Rights", "Consumer complaints, rights and available remedies."),
    ("👮", "FIR & Police", "Police complaints, FIR procedures and reporting options."),
    ("⚖️", "Court Procedures", "General court processes and possible next steps."),
]

topic_columns = st.columns(3)
for index, (icon, title, description) in enumerate(topics):
    with topic_columns[index % 3]:
        st.markdown(
            f"""
            <div class="topic-card">
                <div class="topic-icon">{icon}</div>
                <div class="topic-title">{title}</div>
                <div class="topic-description">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------- Legal system prompt -----------------------------
LEGAL_PROMPT = """
You are an Indian legal information assistant. Provide cautious, plain-language
general information about Indian laws and procedures. You are not a lawyer and
must not claim to provide professional legal advice.

Accuracy rules:
- Applicable law can depend on the incident date, location and facts.
- Do not automatically apply IPC and BNS together to one incident.
- Do not invent legal sections, penalties, fines, bail status or helplines.
- If uncertain, say that the detail needs verification against official sources.
- Do not guarantee legal outcomes.
- For immediate danger, advise contacting local emergency services.
- Encourage lawful evidence preservation and professional advice.
- Avoid asking for unnecessary sensitive personal information.
- Distinguish general information from a case-specific legal conclusion.
- Keep the explanation clear, practical and reasonably concise.

Classify the query into a relevant category such as Constitution, IPC, BNS,
Criminal Procedure, Cyber Crime Law, Consumer Rights, RTI Act, Family Law,
Property Law, Supreme Court, High Court, FIR & Police Complaints, Human Rights,
Digital Law, Legal Information, or Other. Extract 3-5 relevant keywords.

Return ONLY valid JSON, without Markdown or text outside JSON, using this structure:
{{
 "Category": "",
 "Keywords": ["", "", ""],
 "Explanation": "",
 "Legal Sections": [""],
 "Punishment": {{
   "Jail Term": "",
   "Fine": "",
   "Imprisonment Type": "",
   "Legal Consequences": ""
 }},
 "Bailable/Non-Bailable": "",
 "Cognizable/Non-Cognizable": "",
 "Victim Guidance": {{
   "Immediate Actions": [""],
   "Medical Actions": [""],
   "Evidence Collection": [""],
   "Police Procedure": [""],
   "Legal Rights": [""],
   "Safety Precautions": [""],
   "Mistakes To Avoid": [""],
   "Emergency Contacts": [""]
 }},
 "Resources": [""]
}}
"""


def normalize_list(value):
    """Convert an optional model field to a clean list of strings."""
    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if item is not None and str(item).strip()
        ]
    if value is None:
        return []
    if isinstance(value, str) and not value.strip():
        return []
    return [str(value).strip()]


def safe_text(value, default="Not specified"):
    """Return readable text even if the model returns a non-string value."""
    if value is None:
        return default
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    text_value = str(value).strip()
    return text_value if text_value else default


def show_list(items):
    values = normalize_list(items)
    if not values:
        st.caption("No information provided.")
        return
    for item in values:
        st.markdown(f"- {item}")


def parse_json_response(raw_response):
    """Parse JSON, tolerating a model that wraps it in a Markdown code fence."""
    cleaned = raw_response.strip()
    cleaned = re.sub(r"^\s*```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```\s*$", "", cleaned)
    return json.loads(cleaned)


def analyze_question(question):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found. Add it to your .env file and restart the app."
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", LEGAL_PROMPT),
            ("human", "{question}"),
        ]
    )
    llm = ChatGroq(
        model=MODEL_NAME,
        temperature=0,
        api_key=api_key,
        max_retries=2,
    )
    chain = prompt | llm | StrOutputParser()
    result = parse_json_response(chain.invoke({"question": question}))

    if not isinstance(result, dict):
        raise ValueError("The AI returned an unexpected response format.")
    return result


# ----------------------------- Question form -----------------------------
st.markdown('<div class="section-label">YOUR QUESTION</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Tell us what happened</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Describe your situation in simple language. '
    'Avoid sharing personally identifiable or confidential information.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="privacy-notice">🔒 For your privacy, do not include names, phone numbers, '
    'addresses, passwords, bank details or case numbers.</div>',
    unsafe_allow_html=True,
)

with st.form("legal_question_form", clear_on_submit=False):
    user_input = st.text_area(
        "Describe your legal question",
        height=160,
        placeholder=(
            "Example: Someone entered my room and assaulted me. "
            "What legal steps can I take in India?"
        ),
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button(
        "⚖️  Analyze Legal Query",
        use_container_width=True,
        type="primary",
    )

# ----------------------------- Analysis and results -----------------------------
if submitted:
    if not user_input.strip():
        st.warning("Please enter a legal question before continuing.")
    elif not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY was not found. Add it to your local .env file and restart Streamlit.")
    else:
        try:
            with st.spinner("Reviewing your question and preparing a structured response..."):
                result = analyze_question(user_input.strip())

            st.success("Your legal information overview is ready.")
            st.markdown('<div class="section-label">ANALYSIS OVERVIEW</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Your results</div>', unsafe_allow_html=True)

            left, right = st.columns([1, 2])
            with left:
                category = html.escape(safe_text(result.get("Category"), "Not specified"))
                st.markdown(
                    f'<div class="result-card"><h3>📌 Query category</h3>'
                    f'<span class="category-pill">{category}</span></div>',
                    unsafe_allow_html=True,
                )
            with right:
                keyword_html = "".join(
                    f'<span class="keyword">{html.escape(word)}</span>'
                    for word in normalize_list(result.get("Keywords"))
                )
                st.markdown(
                    f'<div class="result-card"><h3>🔑 Key concepts</h3>'
                    f'{keyword_html or "No keywords returned."}</div>',
                    unsafe_allow_html=True,
                )

            with st.container(border=True):
                st.markdown("### 📖 Plain-language explanation")
                st.write(safe_text(result.get("Explanation"), "No explanation returned."))

            st.markdown("### ⚖️ Relevant legal provisions")
            show_list(result.get("Legal Sections"))

            punishment = result.get("Punishment") or {}
            if not isinstance(punishment, dict):
                punishment = {}

            st.markdown("### 🚨 Punishment & legal consequences")
            punishment_items = [
                ("🔒 Jail term", punishment.get("Jail Term")),
                ("💰 Fine", punishment.get("Fine")),
                ("🏛️ Imprisonment type", punishment.get("Imprisonment Type")),
                ("⚠️ Legal consequences", punishment.get("Legal Consequences")),
            ]
            punishment_columns = st.columns(2)
            for index, (heading, value) in enumerate(punishment_items):
                with punishment_columns[index % 2]:
                    with st.container(border=True):
                        st.markdown(f"#### {heading}")
                        st.write(safe_text(value))

            st.markdown("### 🧭 Legal classification")
            status_columns = st.columns(2)
            with status_columns[0]:
                with st.container(border=True):
                    st.markdown("#### ⚖️ Bail classification")
                    st.write(
                        safe_text(
                            result.get("Bailable/Non-Bailable"),
                            "Requires verification.",
                        )
                    )
            with status_columns[1]:
                with st.container(border=True):
                    st.markdown("#### 📜 Cognizability")
                    st.write(
                        safe_text(
                            result.get("Cognizable/Non-Cognizable"),
                            "Requires verification.",
                        )
                    )

            guidance = result.get("Victim Guidance") or {}
            if not isinstance(guidance, dict):
                guidance = {}

            st.markdown("### 🛡️ Victim guidance")
            guidance_items = [
                ("🚨 Immediate actions", "Immediate Actions"),
                ("🏥 Medical actions", "Medical Actions"),
                ("📸 Evidence collection", "Evidence Collection"),
                ("👮 Police procedure", "Police Procedure"),
                ("⚖️ Legal rights", "Legal Rights"),
                ("🔐 Safety precautions", "Safety Precautions"),
                ("⛔ Mistakes to avoid", "Mistakes To Avoid"),
                ("☎️ Emergency contacts", "Emergency Contacts"),
            ]

            guidance_columns = st.columns(2)
            for index, (heading, key) in enumerate(guidance_items):
                with guidance_columns[index % 2]:
                    with st.expander(heading, expanded=(index == 0)):
                        show_list(guidance.get(key))

            st.markdown("### 🌐 Legal resources")
            show_list(result.get("Resources"))

            st.markdown(
                """
                <div class="notice">
                    <strong>Important legal notice:</strong>
                    This application provides AI-generated general legal information,
                    not professional legal advice. AI responses may be inaccurate or
                    outdated. Verify laws, legal sections, penalties, procedures and
                    helplines with official sources or a qualified legal professional.
                    If someone is in immediate danger, contact local emergency services.
                </div>
                """,
                unsafe_allow_html=True,
            )

        except json.JSONDecodeError:
            st.error("The AI response was not valid JSON. Please try again.")
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            message = str(exc).lower()
            if "model_not_found" in message or "model_decommissioned" in message:
                st.error(
                    f"The Groq model '{MODEL_NAME}' is unavailable or your account "
                    "cannot access it. Check the current Groq model list and update "
                    "GROQ_MODEL in your .env file."
                )
            elif "401" in message or "authentication" in message or "invalid_api_key" in message:
                st.error("Groq authentication failed. Check GROQ_API_KEY in your .env file.")
            elif "429" in message or "rate_limit" in message:
                st.warning("The Groq API rate limit was reached. Wait briefly and try again.")
            else:
                st.error("Unable to analyze this question right now. Check your connection and Groq API settings.")
                with st.expander("Technical details"):
                    st.code(str(exc))

# ----------------------------- Footer -----------------------------
st.markdown(
    """
    <div class="footer">
        <div style="font-size: 22px; margin-bottom: 6px;">⚖️</div>
        <strong style="font-size: 19px;">Nyaya AI</strong><br>
        AI-Powered Indian Legal Information Assistant
        <div style="margin-top: 16px;">
            Built with <strong>Python</strong> · <strong>Streamlit</strong> ·
            <strong>LangChain</strong> · <strong>Groq</strong>
        </div>
        <div style="margin-top: 14px; font-size: 12px;">
            For educational and informational purposes only.
            Not a substitute for professional legal advice.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import json
import re
import os


load_dotenv()


st.set_page_config(
    page_title="Indian Judicial System Assistant",
    page_icon="⚖️",
    layout="wide"
)


st.title("⚖️ GEN AI - Powered Indian Judicial System Assistant")

st.markdown("""
### Ask Questions Related to:
- IPC & BNS Laws
- FIR & Police Complaints
- Cyber Crime
- Constitution
- Consumer Rights
- Court Procedures
- Legal Punishments
- Victim Guidance
""")


template = """
You are an expert Indian Judicial System and Legal AI Assistant with deep knowledge of:
- Indian Penal Code (IPC)
- Bharatiya Nyaya Sanhita (BNS)
- Constitution of India
- Cyber Crime Laws
- FIR Procedures
- Consumer Rights
- Family Law
- Property Law
- Human Rights
- Supreme Court and High Court procedures

Your tasks are:

1. Classify the user's query into one of the following categories:
- Indian Constitution
- IPC
- BNS
- CrPC
- Cyber Crime Law
- Consumer Rights
- RTI Act
- Family Law
- Property Law
- Supreme Court
- High Court
- FIR & Police Complaints
- Human Rights
- Digital Law
- Legal Advice
- Other

2. Extract 3-5 highly relevant legal keywords from the query.

3. Explain the answer clearly in simple language within 100-200 words.

4. Mention all applicable:
- IPC Sections
- BNS Sections
- Legal Acts
- Constitutional Articles

5. Explain legal consequences for the accused including:
- jail punishment duration
- imprisonment type
- fine amount
- legal consequences
- criminal record impact
- possible court action

6. Mention whether offense is:
- Bailable or Non-Bailable
- Cognizable or Non-Cognizable

7. VERY IMPORTANT:
Provide detailed victim guidance explaining:
- what victim should do immediately
- safety precautions
- medical actions
- evidence collection steps
- FIR filing procedure
- whom to contact
- what mistakes to avoid
- legal rights of victim
- emergency helplines
- cyber safety precautions if online crime
- how to behave during police investigation

8. Suggest useful legal resources and government helplines.

IMPORTANT RULES:
- Return ONLY valid JSON
- Do NOT use markdown
- Do NOT add explanations outside JSON
- Ensure proper JSON formatting

Return STRICTLY in this JSON format:

{{
    "Category": "",

    "Keywords": [
        "",
        "",
        ""
    ],

    "Explanation": "",

    "Legal Sections": [
        ""
    ],

    "Punishment": {{
        "Jail Term": "",
        "Fine": "",
        "Imprisonment Type": "",
        "Legal Consequences": ""
    }},

    "Bailable/Non-Bailable": "",

    "Cognizable/Non-Cognizable": "",

    "Victim Guidance": {{

        "Immediate Actions": [
            "",
            ""
        ],

        "Medical Actions": [
            "",
            ""
        ],

        "Evidence Collection": [
            "",
            ""
        ],

        "Police Procedure": [
            "",
            ""
        ],

        "Legal Rights": [
            "",
            ""
        ],

        "Safety Precautions": [
            "",
            ""
        ],

        "Mistakes To Avoid": [
            "",
            ""
        ],

        "Emergency Contacts": [
            "",
            ""
        ]
    }},

    "Resources": [
        "",
        ""
    ]
}}
"""


user_input = st.text_area(
    "Enter your Legal Question:",
    height=180,
    placeholder="Example: Someone entered my room and beat me. What legal action can I take?"
)


prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        ("human", "{question}")
    ]
)


model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


parser = StrOutputParser()


chain = prompt_template | model | parser


if st.button("Analyze Legal Query"):

    
    if not user_input.strip():

        st.warning("Please enter a legal question.")

    else:

        try:

            with st.spinner("Analyzing Legal Query..."):

                
                raw_response = chain.invoke(
                    {"question": user_input}
                )

                
                raw_response = raw_response.strip()

                
                raw_response = re.sub(
                    r"```json|```",
                    "",
                    raw_response
                )

                
                response = json.loads(raw_response)

            st.success("Analysis Completed Successfully ✅")

            
            st.subheader("📌 Category")
            st.write(response.get("Category", "N/A"))

            
            st.subheader("🔑 Keywords")

            keywords = response.get("Keywords", [])

            if keywords:

                for keyword in keywords:
                    st.write(f"✅ {keyword}")

            else:
                st.write("No keywords available.")

            
            st.subheader("📖 Explanation")
            st.write(response.get("Explanation", ""))

            
            st.subheader("⚖️ Legal Sections")

            sections = response.get("Legal Sections", [])

            if sections:

                for section in sections:
                    st.write(f"📜 {section}")

            else:
                st.write("No legal sections available.")

            
            st.subheader("🚨 Punishment Details")

            punishment = response.get("Punishment", {})

            st.write(
                f"🔒 Jail Term: {punishment.get('Jail Term', 'N/A')}"
            )

            st.write(
                f"💰 Fine: {punishment.get('Fine', 'N/A')}"
            )

            st.write(
                f"🏛️ Imprisonment Type: {punishment.get('Imprisonment Type', 'N/A')}"
            )

            st.write(
                f"⚠️ Legal Consequences: {punishment.get('Legal Consequences', 'N/A')}"
            )

            
            st.subheader("⚖️ Bailable / Non-Bailable")

            st.write(
                response.get(
                    "Bailable/Non-Bailable",
                    "N/A"
                )
            )

            
            st.subheader("📜 Cognizable / Non-Cognizable")

            st.write(
                response.get(
                    "Cognizable/Non-Cognizable",
                    "N/A"
                )
            )

            
            st.subheader("🛡️ Victim Guidance")

            victim_guidance = response.get(
                "Victim Guidance",
                {}
            )

            
            st.markdown("### 🚨 Immediate Actions")

            for item in victim_guidance.get(
                "Immediate Actions",
                []
            ):
                st.write(f"✅ {item}")

            
            st.markdown("### 🏥 Medical Actions")

            for item in victim_guidance.get(
                "Medical Actions",
                []
            ):
                st.write(f"✅ {item}")

            
            st.markdown("### 📸 Evidence Collection")

            for item in victim_guidance.get(
                "Evidence Collection",
                []
            ):
                st.write(f"✅ {item}")

            
            st.markdown("### 👮 Police Procedure")

            for item in victim_guidance.get(
                "Police Procedure",
                []
            ):
                st.write(f"✅ {item}")

            
            st.markdown("### ⚖️ Legal Rights")

            for item in victim_guidance.get(
                "Legal Rights",
                []
            ):
                st.write(f"✅ {item}")

            
            st.subheader("🌐 Legal Resources")

            resources = response.get(
                "Resources",
                []
            )

            if resources:

                for resource in resources:
                    st.write(resource)

            else:
                st.write("No resources available.")



        except Exception as e:

            st.error(f"Error: {str(e)}")


st.caption(
    "⚖️ Built with Streamlit + LangChain + Groq LLM"
)
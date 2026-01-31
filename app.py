import streamlit as st

from ingestion.pdf_parser import extract_pdf_text
from ingestion.docx_parser import extract_docx_text
from ingestion.language_detector import detect_language

from nlp.clause_splitter import split_into_clauses
from nlp.ner_extractor import extract_entities
from nlp.obligation_classifier import classify_clause
from nlp.translator import translate_hi_to_en

from risk_engine.clause_risk import assess_clause_risk
from risk_engine.contract_risk import calculate_contract_risk

from llm.explain_clause import explain_clause
from llm.suggest_alternatives import suggest_alternative


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Contract Risk Analyzer MVP",
    page_icon="📑",
    layout="wide"
)

st.title("📑 Contract Risk Analyzer — Startup MVP")
st.caption("AI-powered contract risk detection for SMEs (English + Hindi)")

# ================= FILE UPLOAD =================

uploaded = st.file_uploader(
    "Upload Contract (PDF / DOCX / TXT)",
    type=["pdf","docx","txt"]
)

if uploaded:

    # ---------- READ FILE ----------
    if uploaded.name.endswith(".pdf"):
        text = extract_pdf_text(uploaded)
    elif uploaded.name.endswith(".docx"):
        text = extract_docx_text(uploaded)
    else:
        text = uploaded.read().decode("utf-8")

    # ---------- LANGUAGE DETECTION ----------
    lang = detect_language(text)

    if lang == "hi":
        st.warning("Hindi contract detected — translating to English for analysis...")
        text = translate_hi_to_en(text)

    # ---------- NLP PIPELINE ----------
    clauses = split_into_clauses(text)

    results = []

    for clause in clauses:
        risks = assess_clause_risk(clause["text"])
        results.append({
            "text": clause["text"],
            "type": classify_clause(clause["text"]),
            "entities": extract_entities(clause["text"]),
            "risks": risks
        })

    overall_risk = calculate_contract_risk(results)
    risky_count = sum(1 for r in results if r["risks"])

    # ================= MVP TABS =================

    tab1, tab2, tab3 = st.tabs([
        "📊 Risk Dashboard",
        "📄 Clause Analysis",
        "🧾 Summary Report"
    ])

    # =====================================================
    # TAB 1 — DASHBOARD
    # =====================================================

    with tab1:

        col1, col2, col3 = st.columns(3)

        col1.metric("📄 Total Clauses", len(results))
        col2.metric("⚠ Risky Clauses", risky_count)

        if overall_risk == "High":
            col3.error("🔴 Overall Risk: HIGH")
        elif overall_risk == "Medium":
            col3.warning("🟠 Overall Risk: MEDIUM")
        else:
            col3.success("🟢 Overall Risk: LOW")

        st.progress(risky_count / max(len(results),1))

        st.subheader("Risk Distribution")

        high = sum(1 for r in results if any(x["risk"]=="High" for x in r["risks"]))
        med  = sum(1 for r in results if any(x["risk"]=="Medium" for x in r["risks"]))
        low  = len(results) - high - med

        st.write(f"🔴 High Risk Clauses: {high}")
        st.write(f"🟠 Medium Risk Clauses: {med}")
        st.write(f"🟢 Low Risk Clauses: {low}")

    # =====================================================
    # TAB 2 — CLAUSE ANALYSIS (YOUR CARD UI — ENHANCED)
    # =====================================================

    with tab2:

        st.header("Clause-by-Clause Analysis")

        for i, r in enumerate(results, 1):

            # Risk color border
            if any(x["risk"]=="High" for x in r["risks"]):
                border_color = "#ff4b4b"
            elif any(x["risk"]=="Medium" for x in r["risks"]):
                border_color = "#ffa500"
            else:
                border_color = "#2ecc71"

            st.markdown(
                f"""
                <div style="
                    border-left: 6px solid {border_color};
                    padding: 14px;
                    margin-bottom: 14px;
                    background-color: #111827;
                    border-radius: 10px;
                ">
                """,
                unsafe_allow_html=True
            )

            with st.expander(f"Clause {i}"):

                st.write(r["text"])
                st.write("**Type:**", r["type"])

                # ---------- ENTITIES ----------
                if r["entities"]:
                    st.write("**Entities Detected:**")
                    for ent, label in r["entities"]:
                        st.code(f"{ent} → {label}")

                # ---------- RISKS ----------
                if r["risks"]:
                    st.write("**Risks Detected:**")
                    for risk in r["risks"]:
                        if risk["risk"] == "High":
                            st.error(f"{risk['type']} — HIGH")
                        elif risk["risk"] == "Medium":
                            st.warning(f"{risk['type']} — MEDIUM")
                        else:
                            st.success(f"{risk['type']} — LOW")

                    st.info("Explanation")
                    st.write(explain_clause(r["text"]))

                    st.success("Suggested Alternative")
                    st.write(suggest_alternative(r["text"]))

                else:
                    st.success("No major risk detected")

            st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # TAB 3 — SUMMARY REPORT (MVP FEATURE)
    # =====================================================

    with tab3:

        st.subheader("Plain Language Risk Summary")

        if risky_count == 0:
            st.success("This contract has no major high-risk clauses detected.")
        else:
            for r in results:
                if r["risks"]:
                    st.write(
                        f"• Clause contains **{r['risks'][0]['type']}** risk"
                    )

        st.divider()

        st.subheader("SME Recommendation")

        if overall_risk == "High":
            st.error("Recommended: Legal review before signing.")
        elif overall_risk == "Medium":
            st.warning("Recommended: Negotiate flagged clauses.")
        else:
            st.success("Risk acceptable — basic review advised.")

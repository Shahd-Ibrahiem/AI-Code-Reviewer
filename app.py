import streamlit as st
import pandas as pd
from src.analyzer import CodeAnalyzerEngine

st.set_page_config(
    page_title="AI Code Reviewer & Refactor Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Code Review & Refactoring Assistant")
st.caption("Automated security vulnerability checks, performance optimization, and AST-aware refactoring.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    groq_key = st.text_input("Groq API Key", type="password")
    openai_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    language = st.selectbox("Programming Language", ["Python", "JavaScript", "TypeScript", "Go", "Java", "C++"])

col_code, col_review = st.columns([1, 1])

with col_code:
    st.subheader("💻 Input Source Code")
    default_code = """def process_user_data(user_list):\n    # Unsafe & inefficient user processor\n    results = []\n    for i in range(len(user_list)):\n        user = user_list[i]\n        if user['active'] == True:\n            # Potential Key Error & inefficient SQL-like search\n            results.append(user['name'].upper())\n    return results"""
    
    code_input = st.text_area(
        "Paste your code here:",
        value=default_code,
        height=380
    )
    
    run_review = st.button("🔍 Run Full Code Audit", type="primary", use_container_width=True)

with col_review:
    st.subheader("📊 Audit & Refactoring Report")

    if run_review and code_input:
        with st.spinner("Analyzing code quality, security vulnerabilities, and AST metrics..."):
            try:
                engine = CodeAnalyzerEngine(groq_key=groq_key, openai_key=openai_key)
                report = engine.analyze_code(code_snippet=code_input, language=language)

                # Score Metrics
                score_color = "🟢" if report.overall_score >= 80 else ("🟡" if report.overall_score >= 60 else "🔴")
                st.markdown(f"### Overall Code Health: {score_color} `{report.overall_score}/100`")
                st.info(f"**Summary:** {report.summary}")

                # Metrics Row
                m1, m2 = st.columns(2)
                m1.metric("Cyclomatic Complexity", report.cyclomatic_complexity)
                m2.metric("Total Issues Found", len(report.issues))

                # Issues List
                if report.issues:
                    st.markdown("### ⚠️ Identified Issues")
                    issues_data = [issue.model_dump() for issue in report.issues]
                    st.dataframe(pd.DataFrame(issues_data), use_container_width=True)

                # Refactored Code Output
                st.markdown("### ✨ Optimized Refactored Code")
                st.code(report.refactoring.refactored_code, language=language.lower())

                with st.expander("🚀 View Refactoring Improvements & Impact"):
                    for imp in report.refactoring.improvements_made:
                        st.write(f"- {imp}")
                    st.caption(f"**Performance Impact:** {report.refactoring.performance_impact}")

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
    else:
        st.info("Paste your code on the left panel and click **Run Full Code Audit**.")
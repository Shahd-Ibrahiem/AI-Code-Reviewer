# 🤖 AI Code Review & Refactoring Assistant

An automated code audit and AST-aware refactoring platform designed to detect security vulnerabilities (OWASP), performance bottlenecks, and code smells while generating optimized code payloads using Pydantic V2 and Radon.

## 🌟 Key Features

• Security & Bug Audit: Identifies OWASP top vulnerabilities, logic bugs, and structural code smells across multiple programming languages.
• AST & Complexity Evaluation: Calculates static cyclomatic complexity metrics using Python AST and Radon static analysis.
• Enforced Output Schema: Uses Pydantic V2 models to guarantee structured, type-safe JSON audit scorecards and refactored payloads.
• Side-by-Side Refactoring: Generates clean, refactored code alongside detailed performance impact breakdowns and fix summaries.

## 🛠️ Tech Stack

• Python 3.10+
• Groq API / OpenAI API
• Pydantic V2 & Radon
• Streamlit & Pandas

## 🚀 Quickstart
```bash
# Clone repository
git clone https://github.com/Shahd-Ibrahiem/ai-code-reviewer.git
cd ai-code-reviewer

# Install dependencies
python -m venv venv
venv\Scripts\activate  # On macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# Configure Environment
echo "GROQ_API_KEY=your_key_here" > .env
echo "OPENAI_API_KEY=your_key_here" >> .env

# Run Application
streamlit run app.py

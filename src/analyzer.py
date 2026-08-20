import os
import ast
import json
from typing import Dict, Any
from dotenv import load_dotenv
from radon.complexity import cc_visit

from groq import Groq
from openai import OpenAI
from src.schemas import CodeReviewReport

load_dotenv()

class CodeAnalyzerEngine:
    def __init__(self, groq_key: str = None, openai_key: str = None):
        self.groq_key = groq_key or os.getenv("GROQ_API_KEY")
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")

        if self.groq_key:
            self.groq_client = Groq(api_key=self.groq_key)
        else:
            self.groq_client = None

        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
        else:
            self.openai_client = None

    def validate_python_syntax(self, code_str: str) -> Dict[str, Any]:
        """Validates Python syntax and measures cyclomatic complexity using AST & Radon."""
        try:
            ast.parse(code_str)
            complexity_blocks = cc_visit(code_str)
            avg_complexity = (
                sum(b.complexity for b in complexity_blocks) / len(complexity_blocks)
                if complexity_blocks else 1.0
            )
            return {
                "valid_syntax": True,
                "error": None,
                "avg_complexity": round(avg_complexity, 2)
            }
        except SyntaxError as e:
            return {
                "valid_syntax": False,
                "error": f"SyntaxError on line {e.lineno}: {e.msg}",
                "avg_complexity": 0.0
            }

    def analyze_code(self, code_snippet: str, language: str = "Python") -> CodeReviewReport:
        """Executes automated code review, security analysis, and refactoring using LLM schema models."""
        syntax_check = self.validate_python_syntax(code_snippet) if language.lower() == "python" else {"valid_syntax": True, "avg_complexity": "N/A"}

        meta_prompt = f"""
        You are a Principal Software Engineer and Automated Code Review System.
        Analyze the provided {language} code snippet for bugs, security vulnerabilities (OWASP), performance bottlenecks, and architectural improvements.

        Static Analysis Context:
        - Syntax Validity: {syntax_check.get('valid_syntax')}
        - Static Cyclomatic Complexity Index: {syntax_check.get('avg_complexity')}

        Input Code:
        ```{language.lower()}
        {code_snippet}
        ```

        Output Requirement:
        Provide a complete JSON response matching this exact Pydantic schema:
        {json.dumps(CodeReviewReport.model_json_schema(), indent=2)}
        """

        if self.groq_client:
            response = self.groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",  # Active production model on Groq
                messages=[{"role": "system", "content": meta_prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            raw_json = response.choices[0].message.content
            return CodeReviewReport.model_validate_json(raw_json)

        elif self.openai_client:
            response = self.openai_client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": meta_prompt}],
                response_format=CodeReviewReport,
                temperature=0.2
            )
            return response.choices[0].message.parsed
        else:
            raise ValueError("No valid Groq or OpenAI API key available.")
from pydantic import BaseModel, Field
from typing import List, Optional

class CodeIssue(BaseModel):
    issue_type: str = Field(description="Category: Security, Performance, Bug, Style, or Code Smell")
    severity: str = Field(description="Severity rating: Critical, High, Medium, Low")
    line_number: Optional[int] = Field(default=None, description="Line number where issue occurs")
    description: str = Field(description="Clear explanation of the problem")
    recommendation: str = Field(description="Actionable suggestion to fix the issue")

class RefactoringSuggestion(BaseModel):
    refactored_code: str = Field(description="Complete refactored version of input code")
    improvements_made: List[str] = Field(description="List of specific refactoring fixes applied")
    performance_impact: str = Field(description="Estimated runtime or memory impact of changes")

class CodeReviewReport(BaseModel):
    overall_score: int = Field(description="Quality score from 0 to 100")
    summary: str = Field(description="Concise 2-3 sentence assessment of overall code health")
    cyclomatic_complexity: str = Field(default="Low", description="Code complexity assessment")
    issues: List[CodeIssue] = Field(default_factory=list, description="Detailed list of identified issues")
    refactoring: RefactoringSuggestion = Field(description="Refactored code payload and notes")
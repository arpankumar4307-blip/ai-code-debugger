import os

def explain_bug(bug, code_snippet):
    prompt = f"""
You are a senior software engineer.

Bug detected:
Title: {bug['title']}
Description: {bug['description']}

Code:
{code_snippet}

Explain why this is wrong and suggest a correct version.
"""

    # For now return mock (replace later with real LLM)
    return {
        "explanation": f"The issue '{bug['title']}' can cause security or logic problems.",
        "fix": "Use environment variables or safer coding practices."
    }

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root test
@app.get("/")
def read_root():
    return {"status": "AI Code Debugger Backend Running"}

# ---- SIMPLE AI EXPLANATION ENGINE (MOCK FOR NOW) ----
def explain_bug(bug, code):
    explanations = {
        "Hardcoded Password": {
            "explanation": "Hardcoding passwords is insecure because anyone who gets access to the code can see sensitive credentials.",
            "fix": "Use environment variables or a secure secrets manager instead of hardcoding passwords."
        },
        "Debug Statement": {
            "explanation": "Debug statements can expose internal data and reduce performance in production.",
            "fix": "Remove debug logs or use a proper logging library with log levels."
        },
        "Long Line": {
            "explanation": "Long lines make code hard to read and maintain.",
            "fix": "Break the line into smaller, readable parts or refactor the logic."
        }
    }

    return explanations.get(
        bug["title"],
        {
            "explanation": "This issue may cause maintainability or security problems.",
            "fix": "Follow best coding practices to resolve this issue."
        }
    )

# Analyze code endpoint
@app.post("/analyze")
async def analyze_code(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode("utf-8", errors="ignore")

    bugs = []

    # Rule 1: Hardcoded password
    if "password" in code.lower():
        bug = {
            "title": "Hardcoded Password",
            "description": "Sensitive keyword 'password' found in code",
            "severity": "high"
        }

        ai = explain_bug(bug, code)
        bug["ai_explanation"] = ai["explanation"]
        bug["ai_fix"] = ai["fix"]

        bugs.append(bug)

    # Rule 2: Console log
    if "console.log" in code:
        bug = {
            "title": "Debug Statement",
            "description": "console.log found remove before production",
            "severity": "low"
        }

        ai = explain_bug(bug, code)
        bug["ai_explanation"] = ai["explanation"]
        bug["ai_fix"] = ai["fix"]

        bugs.append(bug)

    # Rule 3: Long lines
    for line in code.splitlines():
        if len(line) > 120:
            bug = {
                "title": "Long Line",
                "description": "Line exceeds 120 characters",
                "severity": "medium"
            }

            ai = explain_bug(bug, code)
            bug["ai_explanation"] = ai["explanation"]
            bug["ai_fix"] = ai["fix"]

            bugs.append(bug)
            break

    response = {
        "files": 1,
        "bugs": bugs,
        "bugCount": len(bugs),
        "securityCount": len([b for b in bugs if b["severity"] == "high"]),
        "performanceCount": len([b for b in bugs if b["severity"] == "low"])
    }

    return response



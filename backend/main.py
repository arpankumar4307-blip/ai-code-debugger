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

# Analyze code endpoint
@app.post("/analyze")
async def analyze_code(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode("utf-8", errors="ignore")

    bugs = []

    # Rule 1: Hardcoded password
    if "password" in code.lower():
        bugs.append({
            "title": "Hardcoded Password",
            "description": "Sensitive keyword 'password' found in code",
            "severity": "high"
        })

    # Rule 2: Console log
    if "console.log" in code:
        bugs.append({
            "title": "Debug Statement",
            "description": "console.log found remove before production",
            "severity": "low"
        })

    # Rule 3: Long lines
    for line in code.splitlines():
        if len(line) > 120:
            bugs.append({
                "title": "Long Line",
                "description": "Line exceeds 120 characters",
                "severity": "medium"
            })
            break

    response = {
        "files": 1,
        "bugs": bugs,
        "bugCount": len(bugs),
        "securityCount": len([b for b in bugs if b["severity"] == "high"]),
        "performanceCount": len([b for b in bugs if b["severity"] == "low"])
    }

    return response


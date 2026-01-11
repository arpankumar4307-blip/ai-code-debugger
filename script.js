// Get elements
const analyzeBtn = document.getElementById("analyzeBtn");
const fileInput = document.getElementById("codeFile");

const filesCount = document.getElementById("filesCount");
const bugsCount = document.getElementById("bugsCount");
const securityCount = document.getElementById("securityCount");
const performanceCount = document.getElementById("performanceCount");

const bugList = document.getElementById("bugList");

// Button click
analyzeBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    alert("Please upload a file first");
    return;
  }

  await runAnalysis();
});

// REAL analysis function
async function runAnalysis() {
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("https://friendly-space-memory-q7jxq5xg6w9p3xq5w-8000.app.github.dev/", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Backend error");
    }

    const data = await response.json();

    // Update dashboard numbers
    filesCount.textContent = data.files;
    bugsCount.textContent = data.bugCount;
    securityCount.textContent = data.securityCount;
    performanceCount.textContent = data.performanceCount;

    // Render bugs
    bugList.innerHTML = "";

    if (data.bugs.length === 0) {
      bugList.innerHTML = "<p>No issues found 🎉</p>";
      return;
    }

    data.bugs.forEach(bug => {
      const bugItem = document.createElement("article");
      bugItem.classList.add(bug.severity);

      bugItem.innerHTML = `
        <h3>${bug.title}</h3>
        <p>${bug.description}</p>
      `;

      bugList.appendChild(bugItem);
    });

  } catch (error) {
    alert("Failed to analyze code. Is backend running?");
    console.error(error);
  }
}


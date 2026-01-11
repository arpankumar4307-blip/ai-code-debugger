const analyzeBtn = document.getElementById("analyzeBtn");
const fileInput = document.getElementById("codeFile");

const filesCount = document.getElementById("filesCount");
const bugsCount = document.getElementById("bugsCount");
const securityCount = document.getElementById("securityCount");
const performanceCount = document.getElementById("performanceCount");

const bugList = document.getElementById("bugList");

analyzeBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    alert("Please select a file first");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch(
      "https://friendly-space-memory-q7jxq5xg6w9p3xq5w-8000.app.github.dev/analyze",
      {
        method: "POST",
        body: formData
      }
    );

    const data = await response.json();

    // Update summary
    filesCount.textContent = data.files;
    bugsCount.textContent = data.bugCount;
    securityCount.textContent = data.securityCount;
    performanceCount.textContent = data.performanceCount;

    // Clear previous bugs
    bugList.innerHTML = "";

    if (data.bugs.length === 0) {
      bugList.innerHTML = "<p>No issues found 🎉</p>";
      return;
    }

    data.bugs.forEach(bug => {
      const div = document.createElement("div");
      div.innerHTML = `
        <h3>${bug.title}</h3>
        <p>${bug.description}</p>
        <p><b>AI Explanation:</b> ${bug.ai_explanation}</p>
        <p><b>Suggested Fix:</b> ${bug.ai_fix}</p>
        <hr>
      `;
      bugList.appendChild(div);
    });

  } catch (error) {
    console.error(error);
    alert("Backend not reachable");
  }
});

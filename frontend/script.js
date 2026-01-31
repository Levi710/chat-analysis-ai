const form = document.getElementById("analyzeForm");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const analysisText = document.getElementById("analysisText");
const confidenceText = document.getElementById("confidenceText");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const questionInput = document.getElementById("questionInput");

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("question", questionInput.value);

  // Smooth transition
  loading.classList.remove("hidden");
  result.classList.add("hidden");
  form.style.opacity = "0.5";
  form.style.pointerEvents = "none";

  try {
    const response = await fetch("https://chat-analysis-ai.onrender.com/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    analysisText.textContent = data.analysis;
    // Pretty print the JSON confidence data
    confidenceText.textContent = JSON.stringify(data.confidence, null, 2);

    result.classList.remove("hidden");
    // Scroll to result
    result.scrollIntoView({ behavior: 'smooth' });
    
  } catch (err) {
    alert("The server is ghosting us. Try again later.");
    console.error(err);
  } finally {
    loading.classList.add("hidden");
    form.style.opacity = "1";
    form.style.pointerEvents = "auto";
  }
});


// const form = document.getElementById("analyzeForm");
// const loading = document.getElementById("loading");
// const result = document.getElementById("result");
// const analysisText = document.getElementById("analysisText");
// const confidenceText = document.getElementById("confidenceText");

// form.addEventListener("submit", async (e) => {
//   e.preventDefault();

//   const fileInput = document.getElementById("fileInput");
//   const questionInput = document.getElementById("questionInput");

//   const formData = new FormData();
//   formData.append("file", fileInput.files[0]);
//   formData.append("question", questionInput.value);

//   loading.classList.remove("hidden");
//   result.classList.add("hidden");

//   try {
//     const response = await fetch("http://127.0.0.1:8000/analyze", {
//       method: "POST",
//       body: formData,
//     });

//     const data = await response.json();

//     analysisText.textContent = data.analysis;
//     confidenceText.textContent = JSON.stringify(data.confidence, null, 2);

//     result.classList.remove("hidden");
//   } catch (err) {
//     alert("Error analyzing chat.");
//     console.error(err);
//   } finally {
//     loading.classList.add("hidden");
//   }
// });

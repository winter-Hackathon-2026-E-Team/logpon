const programSelect = document.getElementById("programId");
const postBtn = document.getElementById("postProgramBtn");
const config = document.getElementById("config");

const postUrl = config?.dataset.postUrl;
const csrf = config?.dataset.csrf;

postBtn.addEventListener("click", async () => {
  const programId = programSelect.value;

  try {
    const res = await fetch(postUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify({ program_id: programId }),
    });
    const data = await res.json();
    const redirect = await data.redirect_url;
    window.location.href = await redirect;
  } catch (error) {
    console.error("エラーが発生しました:", error.message);
  }
});

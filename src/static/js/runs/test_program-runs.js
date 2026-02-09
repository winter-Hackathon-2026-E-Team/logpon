const programSelect = document.getElementById("programId");
const postBtn = document.getElementById("postProgramBtn");
const config = document.getElementById("config");

const postUrl = config?.dataset.postUrl;
const csrf = config?.dataset.csrf;

postBtn.addEventListener("click", async () => {
  console.log("送信ボタン");
  const programId = programSelect.value;

  const res = await fetch(postUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
      "X-Requested-With": "XMLHttpRequest",
    },
    body: JSON.stringify({ program_id: programId }),
  });
});

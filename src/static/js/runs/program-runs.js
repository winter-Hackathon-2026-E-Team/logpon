// メモモーダルの開閉
const modal = document.getElementById("modal");

// モーダルを閉じる処理
const closeBtn = document.getElementById("closeBtn");
const overlay = document.getElementById("modalOverlay");

closeBtn.addEventListener("click", () => {
  modal.hidden = true;
});

overlay.addEventListener("click", () => {
  modal.hidden = true;
});
// modaiAreaのクリックは親要素に伝わらないようにブロック、eはイベントオブジェクト
const modalArea = document.getElementById("modalArea");
modalArea.addEventListener("click", (e) => {
  e.stopPropagation();
});

// タイマーをクリックしてモーダルを開く
const timerList = document.getElementById("executeTimerList");

timerList.addEventListener("click", (e) => {
  const timerEl = e.target.closest(".oneTimer");
  if (!timerEl) return;

  const category = timerEl.dataset.category;
  if (category !== "集中") {
    return;
  }

  const timerRunId = timerEl.dataset.timerRunId;
  openMemoModal(timerRunId);
});

// timerRunIDを受けてモーダルを開く関数を定義
function openMemoModal(timerRunId) {
  console.log("open modal for timer:", timerRunId); //この表示は確認用

  modal.hidden = false;
}

// 【追加】プログラムメニュー選択時のfetchAPI(POST)
const programSelect = document.getElementById("programId");
const config = document.getElementById("config");

const postUrl = config?.dataset.postUrl;
const csrf = config?.dataset.csrf;

programSelect.addEventListener("change", async () => {
  const programId = programSelect.value;
  if (!programId) return;

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

// 【追加】リダイレクト後の操作
document.addEventListener("DOMContentLoaded", async () => {
  const executePage = document.querySelector(".execute-page");
  const runId = executePage.dataset.programRunId;
  const apiUrl = executePage.dataset.apiUrl;
  if (!runId) return;

  // リダイレクト先でのプログラムタイマー展開（fetch GET）
  try {
    const res = await fetch(apiUrl, {
      headers: { Accept: "application/json" },
      credentials: "same-origin",
    });
    if (!res.ok) {
      throw new Error(`レスポンスステータス: ${res.status}`);
    }
    const data = await res.json();
    // 右側画面タイマーの展開
    timerList.innerHTML = "";
    const timer_runs = data.runs_data.timer_runs;
    timer_runs.forEach((timer_run) => {
      const btn = document.createElement("button");
      btn.className = "oneTimer";
      btn.innerHTML = `<p>${timer_run.timer_name_snapshot}</p>`;
      timerList.appendChild(btn);
    });
    // 選択したプルダウンメニュー固定
    const programId = data.runs_data.program_run.program_id;
    const selectedOption = programSelect.querySelector(
      `option[value="${programId}"]`,
    );
    selectedOption.selected = true;
  } catch (error) {
    console.error(error.message);
  }
});

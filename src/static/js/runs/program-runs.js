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
const runId = config?.dataset.programRunId;

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
  if (!runId) return;
  const apiUrl = config?.dataset.apiDraftUrl;

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
      btn.id = timer_run.id;
      btn.dataset.status = timer_run.status;
      btn.dataset.elapsedSec = timer_run.elapsed_sec;
      btn.innerHTML = `<p>${timer_run.timer_name_snapshot}</p>`;
      timerList.appendChild(btn);
    });
    // 選択したプルダウンメニュー固定
    const programId = data.runs_data.program_run.program_id;
    const selectedOption = programSelect.querySelector(
      `option[value="${programId}"]`,
    );
    selectedOption.selected = true;
    // プルダウンメニューにprogram_run.statusを付与
    const programRunStatus = data.runs_data.program_run.status;
    selectedOption.dataset.programRunStatus = programRunStatus;
  } catch (error) {
    console.error(error.message);
  }
});

// プログラムstart, resume, pause, finished, interrupted
const btn = document.getElementById("startBtn");
btn.addEventListener("click", async (e) => {
  if (!runId) return;
  const startIcon = btn.querySelector("#startIcon");
  const pauseIcon = btn.querySelector("#pauseIcon");
  const selectedOption = programSelect.selectedOptions[0];
  startIcon.classList.toggle("hidden");
  pauseIcon.classList.toggle("hidden");
  /*
  【全体】
  1.ボタンのアイコンステータスを取得して、start, pauseで条件分岐する
  2.program_runs.statusを調べて、draftであれば、プログラム初期実行（start）を行い、pausedであれば、プログラム再開（resume）を行う（finished, interruptedの場合はどうするか？）
  3.それぞれのstatusでさらに条件分岐を行い、各statusにあうapiUrlを取得する
  【draft】
  1.order_indexが最も若く、timer_runs.statusがpendingのものを取得する
  2.取得したものからtimer_run.id, elapsed_secをPOSTする
  【resume】
  1.timer_run.statusがpausedのものを取得する
  2.取得したものからtimer_run.id, elapsed_secをPOSTする
  【finishedからの再実行】
  1.program_run_idをURLで送り、そのprogram_run_idに紐づくtimer_runs.statusを操作する
  2.order_indexが最も若い、timer_run.statusをrunningにして、それ以外のtimer_runs.statusをpendingにする
  【interrupted】
  1.timer_run.statusがinterruptedを取得する
  2.取得したものからtimer_run.id, elapsed_secをPOSTする
  */
  // 開始ボタン押下
  if (e.target.dataset.iconStatus === "start") {
    console.log("start送信");
    // プログラム初回実行（start）
    if (selectedOption.dataset.programRunStatus === "draft") {
      console.log("draftPOST");
      const apiUrl = config?.dataset.apiStartUrl;
      const timerStatus = timerList.querySelector(
        'button[data-status = "pending"]',
      );
      const timerRunId = timerStatus.id;
      const elapsedSec = timerStatus.dataset.elapsedSec;
      try {
        const res = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrf,
            "X-Requested-With": "XMLHttpRequest",
          },
          body: JSON.stringify({
            timer_run_id: timerRunId,
            elapsedSec: elapsedSec,
          }),
        });
        const data = await res.json();
      } catch (error) {
        console.error(error.message);
      }
    }
    // プログラム再開（resume）
    else if (selectedOption.dataset.programRunStatus === "resume") {
      console.log("resumePOST");
    }
    // プログラム終了後の再実行（finished）
    else if (selectedOption.dataset.programRunStatus === "finished") {
      console.log("finishedPOST");
    }
    // プログラム中断後の再実行（interrupted）
    else if (selectedOption.dataset.programRunStatus === "interrupted") {
      console.log("interruptedPOST");
    }

    // 一時停止ボタン押下
  } else if (e.target.dataset.iconStatus === "pause") {
    console.log("pause送信");
    if (selectedOption.dataset.programRunStatus === "running") {
      console.log("pausePOST");
      const apiUrl = config?.dataset.apiPauseUrl;
      const timerStatus = timerList.querySelector(
        'button[data-status = "running"]',
      );
      const timerRunId = timerStatus.id;
      const elapsedSec = timerStatus.dataset.elapsedSec;
      try {
        const res = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrf,
            "X-Requested-With": "XMLHttpRequest",
          },
          body: JSON.stringify({
            timer_run_id: timerRunId,
            elapsedSec: elapsedSec,
          }),
        });
        const data = await res.json();
      } catch (error) {
        console.error(error.message);
      }
    }
  }
});

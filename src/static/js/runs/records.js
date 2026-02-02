// メモモーダルの開閉
const modal = document.getElementById("modal");

// モーダルを閉じる処理
const closeBtn = document.getElementById("closeBtn");
const overlay = document.getElementById('modalOverlay')

closeBtn.addEventListener("click", () => {
    modal.hidden =true;
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
const timerList = document.getElementById("recordedTimerList");

timerList.addEventListener("click", (e) => {
    const timerEl = e.target.closest(".recordedTimer");
    if (!timerEl) return;

    const category = timerEl.dataset.category;

    const timerRunId = timerEl.dataset.timerRunId;
    openMemoModal(timerRunId);
});

// timerRunIDを受けてモーダルを開く関数を定義
function openMemoModal(timerRunId) {
    console.log("open modal for timer:", timerRunId); //この表示は確認用

    modal.hidden = false;
}
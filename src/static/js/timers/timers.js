// 1.定数
// stateを定義（フロント側で持つ状態）
// モーダルを除いた画面全体の状態
const state = {
    timers: [],
    categories: [],
    sounds: []
};
// モーダルの状態
const modalState = {
    mode: null,
    currentTimer: null,
};


// 2.DOM取得
// モーダルの制御に向けてDOMの取得
// モーダル全体の表示を分けるDOM
const createUpdateContent = document.getElementById('createUpdateContent');
const deleteContent = document.getElementById('deleteContent');

// 削除の前後の表示を分けるDOM
const beforeDelete = document.getElementById('beforeDelete');
const afterDelete = document.getElementById('afterDelete');

// タイマーの新規作成と編集での表示を分けるDOM
const timerModalTitle = document.getElementById('timerModalTitle');
const timerSendBtn = document.getElementById('timerSendBtn');

// タイマー編集モーダルで既存タイマーの値を表示するDOM
const timerNameInput = document.getElementById('timerNameInput');
const durationInput = document.getElementById('durationInput');
const categoryInput = document.getElementById('categoryInput');
const soundInput = document.getElementById('soundInput');

// 削除前モーダルで削除対象を確認するDOM
const deleteTimerName = document.getElementById('deleteTimerName');
const deleteTimerDuration = document.getElementById('deleteTimerDuration');
const deleteTimerCategory = document.getElementById('deleteTimerCategory');

// タイマーカードを振り分ける場所を表すDOM
const focusTimerList = document.getElementById("focusTimerList");
const otherTimerList = document.getElementById('otherTimerList');

// モーダルに関するDOM
const modal = document.getElementById("modal");
const closeBtn = document.getElementById("closeBtn");
const overlay = document.getElementById('modalOverlay');
const modalArea = document.getElementById("modalArea");

// 追加ボタンに関するDOM
const focusTimerAdd = document.getElementById("focusTimerAdd");
const otherTimerAdd = document.getElementById("otherTimerAdd");

// 削除ボタンに関するDOM
const timerDeleteBtn = document.getElementById("timerDeleteBtn");
const deletedConfirm = document.getElementById("deletedConfirm");

// エラーメッセージに関するDOM
const formError = document.getElementById("formError");
const deleteError = document.getElementById("deleteError");

// 3.ユーティリティ関数
// 変換関数
// バックエンドの秒表示をフロントの分表示に変える関数
function secToMin (sec) {
    return Math.floor(sec/60);
}
// フロントの分表示をバックの秒表示に変える関数
function minToSec (min) {
    return Number(min) * 60;
}

// crsftokenを取得する関数と取得処理
function getCookie(name){
  return document.cookie
    .split("; ")
    .find(row => row.startsWith(name + "="))
    ?.split("=")[1];
}
const csrftoken = getCookie("csrftoken");

if (!csrftoken) {
  console.warn("csrftokenが取得できません。CSRF設定を確認してください。");
}



// 4.描画系の関数
// タイマーカードの作成
// 1つのタイマーカードを作る関数
function createTimerCard(timer) {
    return `
    <div class="oneTimer" data-timer-id="${timer.timer_id}">
      <p class="timerName">${timer.timer_name}</p>
      <p class="duration">${secToMin(timer.duration_sec)}分</p>
      <button class="delete-btn" type="button">
        <iconify-icon icon="iconamoon:trash"></iconify-icon>
      </button>
    </div>
    `;
}

// タイマーカードを左右に振り分ける関数
function renderTimers() {
    // 左（集中）と右（その他）の入れ物を定義
    let leftHTML = "";
    let rightHTML = "";

    // stateのtimersを1つずつカテゴリを確認しながら上の変数に入れる
    state.timers.forEach(timer => {
        if (timer.category === "集中") {
            leftHTML += createTimerCard(timer);
        } else {
            rightHTML += createTimerCard(timer);
        }
    });

    if (leftHTML === "") {
        leftHTML = '<p class="empty">タイマーが登録されていません</p>';
    }
    if (rightHTML === "") {
        rightHTML = '<p class="empty">タイマーが登録されていません</p>';
    }

    focusTimerList.innerHTML = leftHTML;
    otherTimerList.innerHTML = rightHTML;

}

// タイマー作成・編集モーダルのカテゴリーの選択肢を入れる関数
function renderCategories() {
    let html = "";
    // 一連のoptionを作る
    state.categories.forEach(cat => {
        html += `<option value="${cat}">${cat}</option>`;
    });
    // 作ったoptionを#categoryInputに入れる
    categoryInput.innerHTML = html;
}

// タイマー作成・編集モーダルのサウンドの選択肢を入れる関数
function renderSounds() {
    let html = "";
    // 一連のoptionを作る
    state.sounds.forEach(sound => {
        html += `<option value="${sound.sound_id}">${sound.sound_name}</option>`;
    });
    // 作ったoptionを#soundInputに入れる
    soundInput.innerHTML = html;
}

// 空メッセージを削除する関数
function clearEmptyMessage(listEl){
    const empty = listEl.querySelector(".empty");
    if (empty) empty.remove();
}

// タイマー作成後にタイマーカードを追加する関数
function addTimerCard (timer) {
    const html = createTimerCard(timer);

    if(timer.category === "集中") {
        clearEmptyMessage(focusTimerList);
        focusTimerList.insertAdjacentHTML("beforeend", html);
    } else {
        clearEmptyMessage(otherTimerList);
        otherTimerList.insertAdjacentHTML("beforeend", html);
    }
}

// タイマー更新後にstateのタイマーを更新する関数
function replaceTimerInState(updated){
  const idx = state.timers.findIndex(t => t.timer_id === updated.timer_id);
  if(idx !== -1){
    state.timers[idx] = updated;
  }
}

// タイマー更新後にタイマーカードを再配置する関数
function replaceTimerCard(timer){
    // timer-idから該当のタイマーカードを取得
    const oldEl = document.querySelector(`.oneTimer[data-timer-id="${timer.timer_id}"]`);
    if(!oldEl) return;

    const oldWasFocus = oldEl.closest("#focusTimerList") !== null;

    // 古いタイマーカードを削除
    oldEl.remove();

    if (oldWasFocus) ensureEmptyMessage(focusTimerList);
    else ensureEmptyMessage(otherTimerList);

    // レスポンスを元に新しいタイマーカードを作成
    const html = createTimerCard(timer);

    // 新しいタイマーカードを再配置（カテゴリ変更にも対応）
    if(timer.category === "集中"){
        clearEmptyMessage(focusTimerList);
        focusTimerList.insertAdjacentHTML("beforeend", html);
    }else{
        clearEmptyMessage(otherTimerList);
        otherTimerList.insertAdjacentHTML("beforeend", html);
    }
}

// stateからタイマーを削除（timerIdに一致しないものを残す）する関数
function removeTimerFromState (timerId) {
    state.timers = state.timers.filter(t => t.timer_id !== timerId);
}

// DOMからタイマーカードを削除する関数
function removeTimerCard (timerId) {
    const el = document.querySelector(`.oneTimer[data-timer-id="${timerId}"]`);
    if (el) el.remove();
}

// タイマーカードを削除後に0件ならからメッセージを表示する関数
function ensureEmptyMessage(listEl) {
    const hasCard = listEl.querySelector(".oneTimer");
    const hasEmpty = listEl.querySelector(".empty");

    if(!hasCard && !hasEmpty) {
        listEl.innerHTML = '<p class="empty">タイマーが登録されていません</p>'
    }
}


// 5.モーダル系の関数
// モーダルを制御する関数を作る
function setModalMode (mode, payload = null) {
    // 最初にmodalStateに値を入れておく
    modalState.mode = mode;
    modalState.currentTimer = payload;
    // モーダル内の全ての表示をリセット
    createUpdateContent.hidden = true;
    deleteContent.hidden = true;
    beforeDelete.hidden = true;
    afterDelete.hidden = true;
    formError.hidden = true;
    deleteError.hidden = true;
    timerNameInput.value = "";
    durationInput.value = "";
    categoryInput.value = "";
    soundInput.value = "";
    deleteTimerName.textContent = "";
    deleteTimerDuration.textContent = "";
    deleteTimerCategory.textContent = "";
    formError.textContent = "";
    deleteError.textContent = "";

    if (mode === "create") {
        createUpdateContent.hidden = false
        timerModalTitle.textContent = "タイマー作成";
        timerSendBtn.textContent = "作成";
        categoryInput.value = payload?.category ?? "集中";
    }

    if (mode === "update") {
        createUpdateContent.hidden = false
        timerModalTitle.textContent = "タイマー編集";
        timerSendBtn.textContent = "更新";

        const t = modalState.currentTimer;
        timerNameInput.value = t.timer_name;
        durationInput.value = secToMin(t.duration_sec);
        categoryInput.value = t.category;
        soundInput.value = t.sound_id;
    }

    if (mode === "delete-confirm") {
        deleteContent.hidden = false;
        beforeDelete.hidden = false;

        const t = modalState.currentTimer;
        deleteTimerName.textContent = `タイマー名：${t.timer_name}`;
        deleteTimerDuration.textContent = `時間：${secToMin(t.duration_sec)}分`;
        deleteTimerCategory.textContent = `カテゴリー：${t.category}`;
    }

    if (mode === "delete-success") {
        deleteContent.hidden = false;
        afterDelete.hidden = false;
    }

    modal.hidden = false;
}

// タイマーカードのクリック場所によってモーダルのmodeを分ける関数
function handleTimerClick(e) {
    // タイマーカードのゴミ箱ボタンをクリックした時の処理
    const deleteBtn = e.target.closest(".delete-btn");
    if(deleteBtn) {
        e.stopPropagation();

        const timerEl = deleteBtn.closest(".oneTimer");
        const id = Number(timerEl.dataset.timerId);

        const timerObj = state.timers.find(t => t.timer_id === id);
        setModalMode("delete-confirm", timerObj);
        return;
    }

    // タイマーカードの編集をするとき（ゴミ箱ボタン以外をクリック）の処理
    const timerEl = e.target.closest(".oneTimer");
    if (!timerEl) return;

    const id = Number(timerEl.dataset.timerId);
    const timerObj = state.timers.find(t => t.timer_id === id);

    setModalMode("update", timerObj);

}


// 6.イベント登録
// バツボタンを押したらモーダルを閉じる処理
closeBtn.addEventListener("click", () => {
    modal.hidden =true;
});

// 背景を押したらモーダルを閉じる処理
overlay.addEventListener("click", () => {
    modal.hidden = true;
});

// 背景の範囲の中でも#modalArea上はイベントの伝播を止める（モーダルを閉じない）処理
modalArea.addEventListener("click", (e) => {
    e.stopPropagation();
});

// 集中のタイマーの1つを押したらモーダルを開く
focusTimerList.addEventListener("click", handleTimerClick);
otherTimerList.addEventListener("click", handleTimerClick);

// 集中のプラスボタンを押したらモーダルを開く
focusTimerAdd.addEventListener("click", () => {
    setModalMode("create", {category: "集中"});
});

// その他のプラスボタンを押したらモーダルを開く
otherTimerAdd.addEventListener("click", () => {
    setModalMode("create", {category: "休憩"})
});

// タイマー作成ボタンを押した時の処理
timerSendBtn.addEventListener("click", async () =>{
    // modeがcreateでない時は動かないようにする
    if (modalState.mode === "create") {
        // エラーを消す
        formError.textContent = "";
        formError.hidden = true;

        // 必須項目のチェック
        const name = timerNameInput.value.trim();
        const min = Number(durationInput.value);

        if (!name) {
            formError.textContent = "タイマー名を入力してください"
            formError.hidden = false;
            return;
        }
        if (!Number.isFinite(min) || min < 1) {
            formError.textContent = "時間（分）は1以上で入力してください";
            formError.hidden = false;
            return;
        }

        // 送信データの作成（分から秒へ）
        const sendData = {
            timer_name: name,
            duration_sec: minToSec(min),
            category: categoryInput.value,
            sound_id: Number(soundInput.value),
        };

        // 送信中の操作ガード
        timerSendBtn.textContent = "作成中..."
        timerSendBtn.disabled = true;

        try {
            const res = await fetch("/timers", {
                method: "POST",
                headers:{ 
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                credentials: "same-origin",
                body: JSON.stringify(sendData),
            });
            // resがokでない場合の処理
            if (!res.ok) {
                const err = await res.json();
                throw err;
            }

            // 成功時の処理
            const createdTimer = await res.json();
            // 下の1行はテスト用の関数
            // const createdTimer = mockCreateTimer(sendData);

            state.timers.push(createdTimer);
            addTimerCard(createdTimer);
            modal.hidden = true;

        } catch (err) {
            // 失敗メッセージの表示
            formError.textContent = err?.error ?? "作成に失敗しました。"
            formError.hidden = false;

        } finally {
            timerSendBtn.textContent = "作成"
            timerSendBtn.disabled = false;
        }
    }

    if (modalState.mode === "update") {
        const id = modalState.currentTimer.timer_id;

        const name = timerNameInput.value.trim();
        const min = Number(durationInput.value);

        if (!name) {
            formError.textContent = "タイマー名を入力してください"
            formError.hidden = false;
            return;
        }
        if (!Number.isFinite(min) || min < 1) {
            formError.textContent = "時間（分）は1以上で入力してください";
            formError.hidden = false;
            return;
        }

        // 送信データの作成（分から秒へ）
        const sendData = {
            timer_name: name,
            duration_sec: minToSec(min),
            category: categoryInput.value,
            sound_id: Number(soundInput.value),
        };

        timerSendBtn.textContent = "更新中...";
        timerSendBtn.disabled = true;

        try {
            const res = await fetch(`/timers/${id}`, {
                method: "POST",
                headers:{ 
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                credentials: "same-origin",
                body: JSON.stringify(sendData),
            });
            // resがokでない場合の処理
            if (!res.ok) {
                const err = await res.json();
                throw err;
            }

            // 成功時の処理
            const updatedTimer = await res.json();
            // 下の1行はテスト用の関数
            // const updatedTimer = await apiUpdateTimer(id, sendData);

            replaceTimerInState(updatedTimer);
            replaceTimerCard(updatedTimer);

            modal.hidden = true;

        } catch(err) {
            formError.textContent = err?.error ?? "更新に失敗しました。";
            formError.hidden = false;

        } finally {
            timerSendBtn.textContent = "更新";
            timerSendBtn.disabled = false;
        }
    }
});

// 削除ボタンを押した時の処理
timerDeleteBtn.addEventListener("click", async()=>{
    if(modalState.mode !== "delete-confirm") return;

    // エラーを消す
    deleteError.textContent = "";
    deleteError.hidden = true;
    // modalStateのcurrentTimerからタイマーIDを取得
    const id = modalState.currentTimer.timer_id;
    // 削除中のボタン表示変更とdisable
    timerDeleteBtn.textContent = "削除中...";
    timerDeleteBtn.disabled = true;

    try {
        const res = await fetch(`/timers/${id}/delete`, {
            method: "POST",
            headers:{ 
                "X-CSRFToken": csrftoken,
            },
            credentials: "same-origin",
        });
        // resがokでない場合の処理
        if (!res.ok) {
            let err = {};
            try {
                err = await res.json();
            } catch {
                err = {error: "サーバーエラー"}
            }
            throw err;
        }

        // 成功時の処理
        const result = await res.json();
        // 下の1行はテスト用の関数
        // const result = await apiDeleteTimer(id);

        if(result.deleted) {
            removeTimerFromState(id);
            removeTimerCard(id);
            ensureEmptyMessage(focusTimerList);
            ensureEmptyMessage(otherTimerList);
            setModalMode("delete-success");
            return;
        }

        // タイマー削除が失敗した場合
        const reason = result.reason ?? "unknown";
        if (reason === "in_use") {
            deleteError.textContent = "このタイマーは使用中のため削除できません。";
        } else {
            deleteError.textContent = "削除できませんでした。";
        }
        deleteError.hidden = false;

    } catch(err) {
        deleteError.textContent = err?.error ?? "削除に失敗しました。";
        deleteError.hidden = false;

    } finally {
        timerDeleteBtn.textContent = "削除";
        timerDeleteBtn.disabled = false;
    }
});

// afterDeleteの閉じるボタンを押した時の挙動
deletedConfirm.addEventListener("click", () => {
    modal.hidden = true;
});


// 仮のデータ
// async function getTimers(){
//     // 仮バックエンド（今だけ）
//     return {
//         timers: [
//             {
//                 timer_id: 1,
//                 timer_name: "Python",
//                 duration_sec: 1500,
//                 category: "集中",
//                 sound_id: 1
//             },
//             {
//                 timer_id: 2,
//                 timer_name: "休憩",
//                 duration_sec: 300,
//                 category: "休憩",
//                 sound_id: 2
//             },
//             {
//                 timer_id: 3,
//                 timer_name: "体操",
//                 duration_sec: 600,
//                 category: "リフレッシュ",
//                 sound_id: 4
//             },
//             {
//                 timer_id: 4,
//                 timer_name: "基本情報",
//                 duration_sec: 1800,
//                 category: "集中",
//                 sound_id: 3
//             },
//         ],
//         categories: ["集中","休憩","リフレッシュ"],
//         sounds: [
//             {sound_id:1,sound_name:"bell"},
//             {sound_id:2,sound_name:"digital"},
//             {sound_id:3,sound_name:"schoolchime"},
//             {sound_id:4,sound_name:"melody1"},
//         ]
//     };
// }

// // createテスト用の関数
// function mockCreateTimer(sendData){
//   const timer = {
//     timer_id: Date.now(), // 一意ならOK
//     timer_name: sendData.timer_name,
//     duration_sec: Number(sendData.duration_sec),
//     category: sendData.category,
//     sound_id: Number(sendData.sound_id),
//     updated_at: new Date().toISOString(),
//   };

//   // “サーバに保存された” ことにする
//   state.timers.push(timer);

//   return timer;
// }

// // updateテスト用の関数
// async function apiUpdateTimer(timerId, sendData){
//   // 仮バックエンド
//   return {
//     timer_id: timerId,
//     timer_name: sendData.timer_name,
//     duration_sec: Number(sendData.duration_sec),
//     category: sendData.category,
//     sound_id: Number(sendData.sound_id),
//     updated_at: new Date().toISOString(),
//   };
// }

// // deleteテスト用の関数
// async function apiDeleteTimer(timerId){
//   // ===== 仮バックエンド（今だけ） =====
//   if (timerId === 1) {
//     return { deleted: false, timer_id: timerId, reason: "in_use" };
//   }
//   return { deleted: true, timer_id: timerId };
// }


// バックエンドからの初期データ取得
async function getTimers(){
    const res = await fetch("/timers/data", {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "Accept": "application/json",
        }
    });

    if (!res.ok) {
        let err = {};
        try {
            err = await res.json();
        } catch {
            err = {
                error: "初期データ取得に失敗しました"
            };
        }
        throw err;
    }

    return await res.json();
}

// 初期ロード処理
async function init(){
    const data = await getTimers();
    // バックエンドから受け取ったデータをstateへ格納
    state.timers = data.timers;
    state.categories = data.categories;
    state.sounds = data.sounds;
    // 各表示を作る関数を実行する
    renderCategories();
    renderSounds();
    renderTimers();
}

document.addEventListener("DOMContentLoaded", init);
// 初期ロード処理ここまで
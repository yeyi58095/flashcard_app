"""Validate alias.txt and produce self-contained HTML and text study copies."""
import hashlib
import html
import json
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]


def parse_bank(path):
    cards = []
    unit = None
    question = None
    source = "原始名詞題庫"
    seen = set()
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# 來源："):
            source = line.removeprefix("# 來源：")
        elif line.startswith("#"):
            continue
        elif line.startswith("[") and line.endswith("]"):
            if question:
                raise ValueError(f"Unanswered question before line {number}")
            unit = line[1:-1]
            source = "原始名詞題庫"
        elif line.startswith("? "):
            if question:
                raise ValueError(f"Two questions before line {number}")
            question = line[2:]
        else:
            if not unit or not question or ": " not in line:
                raise ValueError(f"Invalid card at line {number}")
            term, answer = line.split(": ", 1)
            key = f"{unit}::{term}"
            if not term or not answer or key in seen:
                raise ValueError(f"Empty or duplicate card at line {number}")
            seen.add(key)
            cards.append(dict(id=key, unit=unit, term=term, question=question,
                              answer=answer, source=source, extended=term.startswith("HW-")))
            question = None
    if question:
        raise ValueError("Last question has no answer")
    return cards


HTML = r'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>航電離線複習｜452 題</title>
<style>
:root{color-scheme:light dark;font-family:system-ui,"Microsoft JhengHei",sans-serif;line-height:1.7;background:#101820;color:#edf3f8}
*{box-sizing:border-box}body{max-width:800px;margin:auto;padding:20px 16px 60px}h1{font-size:1.6rem;margin-bottom:0}h2{font-size:1.25rem;line-height:1.7;font-weight:650}p{overflow-wrap:anywhere}
.muted,small{color:#abc0d0}select,button{font:inherit;padding:12px;border-radius:10px;border:1px solid #456074;background:#1b2b39;color:#edf3f8}select{width:100%;margin:4px 0 14px}button{cursor:pointer;min-height:48px}.row{display:flex;gap:10px;flex-wrap:wrap}.row button{flex:1}#flip{width:100%;background:#087e8b;border-color:#24a5b3}article{padding:18px;background:#172532;border:1px solid #30495d;border-radius:16px;margin:20px 0}#answer{border-top:1px solid #456074;margin-top:20px;padding-top:14px;white-space:pre-wrap;overflow-wrap:anywhere}#answer p{margin:0 0 12px}.good{background:#155e48}.bad{background:#743744}progress{width:100%;accent-color:#39b9c9;height:10px}details{margin:20px 0}a{color:#68d8e6}.notice{padding:10px;background:#45391c;border-radius:8px}.hide{display:none!important}button:focus-visible,select:focus-visible{outline:3px solid #f1c86b;outline-offset:3px}
</style></head><body>
<h1>航電離線複習</h1><p class="muted">452 題 · 30 單元 · 300 題作業、架構與計算練習</p>
<p>本檔所有題目與答案都在檔案內；在可執行 JavaScript 的瀏覽器開啟後，不需網路。先回想或在紙上畫圖，再翻答案自評。</p>
<p id="storage-note" class="notice hide">這個瀏覽器無法儲存本機進度；本次仍可練習，關閉前請匯出錯題。</p>
<label for="unit">單元</label><select id="unit"><option value="">全部單元</option></select>
<label for="mode">練習範圍</label><select id="mode"><option value="all">全部題目</option><option value="extended">作業／申論／畫圖／計算</option><option value="wrong">歷史不熟的題目</option></select>
<div class="row"><button id="start">開始／重新隨機排列</button><button id="export">匯出歷史錯題</button></div>
<p id="status" class="muted" aria-live="polite"></p><progress id="progress" value="0" max="1"></progress>
<article><small id="meta"></small><h2 id="question"></h2><button id="flip">顯示答案與自評要點</button><div id="answer" class="hide"></div><div id="marks" class="row hide"><button id="known" class="good">我知道</button><button id="unknown" class="bad">還不熟</button></div></article>
<details><summary>四小時複習建議與使用說明</summary><p>先做 15–19 單元的 FBW 與自駕架構，再做 20、23、25 的冗餘、穩定與模型。接著練 26–30 的 INS／GPS，最後用 22 單元計算題與錯題收尾。時間不夠時優先作業題，不必一次做完所有題。</p><p>每個單元約 15 題。申論題以能否口述核心因果、畫出方塊及回授方向自評；計算題先列公式、單位與假設。原始 01–10 單元可用來補名詞。</p><p>切換單元或範圍會開始新一輪；歷史不熟題仍保留。歷史記錄在此瀏覽器本機，不與 Streamlit 或其他裝置同步。若手機的檔案預覽器不執行互動，請改以瀏覽器開啟，或使用一併提供的純文字題本。</p></details>
<script id="bank" type="application/json">__DATA__</script>
<script>
const bank=JSON.parse(document.getElementById('bank').textContent);
const byId=new Map(bank.map(c=>[c.id,c])), $=id=>document.getElementById(id), key='avionics-offline-__REVISION__';
const units=[...new Set(bank.map(c=>c.unit))];
for(const u of units){const o=document.createElement('option');o.value=u;o.textContent=u;$('unit').append(o)}
let state={unit:'',mode:'all',deck:[],index:0,known:0,revealed:false,wrong:[]};
try{const saved=JSON.parse(localStorage.getItem(key));if(saved&&Array.isArray(saved.deck)&&Array.isArray(saved.wrong)&&saved.deck.every(id=>byId.has(id))&&Number.isInteger(saved.index)&&saved.index>=0&&saved.index<=saved.deck.length)state={...state,...saved}}catch(e){$('storage-note').classList.remove('hide')}
const save=()=>{try{localStorage.setItem(key,JSON.stringify(state))}catch(e){$('storage-note').classList.remove('hide')}};
$('unit').value=state.unit;$('mode').value=state.mode;
function start(){state.unit=$('unit').value;state.mode=$('mode').value;state.deck=bank.filter(c=>(!state.unit||c.unit===state.unit)&&(state.mode!=='extended'||c.extended)&&(state.mode!=='wrong'||state.wrong.includes(c.id))).map(c=>c.id);for(let i=state.deck.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[state.deck[i],state.deck[j]]=[state.deck[j],state.deck[i]]}state.index=0;state.known=0;state.revealed=false;save();render()}
function render(){const total=state.deck.length,done=state.index>=total;$('progress').value=total?state.index/total:0;$('status').textContent=total?`已完成 ${state.index} / ${total} 題 · 本輪知道 ${state.known} 題 · 歷史不熟 ${state.wrong.length} 題`:'目前範圍沒有題目；可切換單元或練習範圍。';$('flip').classList.toggle('hide',done||state.revealed);$('answer').classList.toggle('hide',done||!state.revealed);$('marks').classList.toggle('hide',done||!state.revealed);if(done){$('meta').textContent='';$('question').textContent=total?`本輪完成！自評知道率 ${Math.round(100*state.known/total)}%`:'請選擇練習範圍';if(total)$('progress').value=1;return}const c=byId.get(state.deck[state.index]);$('meta').textContent=`${c.unit} · ${c.term} · 來源：${c.source}`;$('question').textContent=c.question;$('answer').replaceChildren();if(state.revealed){for(const part of c.answer.split(' || ')){const p=document.createElement('p');p.textContent=part;$('answer').append(p)}}}
function mark(known){if(!state.revealed||state.index>=state.deck.length)return;const id=state.deck[state.index];if(known)state.known++;else if(!state.wrong.includes(id))state.wrong.push(id);state.index++;state.revealed=false;save();render();$('question').scrollIntoView({block:'nearest'})}
$('start').onclick=start;$('unit').onchange=start;$('mode').onchange=start;
$('flip').onclick=()=>{state.revealed=true;save();render()};$('known').onclick=()=>mark(true);$('unknown').onclick=()=>mark(false);
$('export').onclick=()=>{const text=state.wrong.map(id=>byId.get(id)).filter(Boolean).map(c=>`[${c.unit}] ${c.term}\n題目：${c.question}\n答案：${c.answer.replaceAll(' || ','\n')}\n`).join('\n');const url=URL.createObjectURL(new Blob(['\ufeff'+(text||'目前沒有錯題。')],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='avionics-wrongs.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
if(state.deck.length)render();else start();
</script></body></html>'''


def build():
    cards = parse_bank(APP_DIR / "alias.txt")
    data = json.dumps(cards, ensure_ascii=False).replace("<", "\\u003c")
    revision = hashlib.sha256(data.encode()).hexdigest()[:12]
    (APP_DIR / "offline_review.html").write_text(
        HTML.replace("__DATA__", data).replace("__REVISION__", revision), encoding="utf-8")
    lines = ["航電完整複習題本", f"共 {len(cards)} 題，{len({c['unit'] for c in cards})} 個單元。",
             "先遮住答案回想；畫圖題請先畫出方塊與回授。數值題以題設簡化模型為準。", ""]
    last_unit = None
    for card in cards:
        if card["unit"] != last_unit:
            last_unit = card["unit"]
            lines.extend(["", "=" * 36, f"[{last_unit}]", f"來源：{card['source']}", "=" * 36])
        lines.extend([f"\n{card['term']}｜{card['question']}", "答案：",
                      card["answer"].replace(" || ", "\n"), ""])
    (APP_DIR / "review_guide.txt").write_text("\n".join(lines), encoding="utf-8-sig")
    print(f"Built offline HTML and text: {len(cards)} cards; {sum(c['extended'] for c in cards)} extended.")


if __name__ == "__main__":
    build()

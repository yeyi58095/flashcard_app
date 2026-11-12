import random
import hashlib
from datetime import datetime
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).resolve().parent
FLASHCARDS_PATH = APP_DIR / "alias.txt"
WRONGS_PATH = APP_DIR / "wrongs.txt"


def load_flashcards(path=FLASHCARDS_PATH):
    """Load cards grouped by the [unit] headings in alias.txt."""
    flashcards = {}
    current_unit = None

    try:
        with open(path, "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line or line.startswith(("#", "? ")):
                    continue
                if line.startswith("[") and line.endswith("]"):
                    current_unit = line[1:-1].strip()
                    flashcards.setdefault(current_unit, {})
                    continue
                if current_unit and ": " in line:
                    term, meaning = line.split(": ", 1)
                    if term.strip() and meaning.strip():
                        flashcards[current_unit][term.strip()] = meaning.strip()
    except (OSError, UnicodeError) as error:
        st.error(f"無法讀取題庫：{path}（{error}）")
        return {}

    return {unit: cards for unit, cards in flashcards.items() if cards}


def load_question_prompts(path=FLASHCARDS_PATH):
    """An optional '? ' line supplies the next card's contextual question."""
    prompts = {}
    unit = None
    pending = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            unit = line[1:-1].strip()
            pending = None
        elif line.startswith("? "):
            pending = line[2:].strip()
        elif unit and ": " in line:
            term = line.split(": ", 1)[0].strip()
            if pending:
                prompts[(unit, term)] = pending
            pending = None
    return prompts


def start_unit(unit, cards):
    deck = list(cards)
    random.shuffle(deck)
    st.session_state.quiz_unit = unit
    st.session_state.deck = deck
    st.session_state.card_index = 0
    st.session_state.show_answer = False
    st.session_state.correct_count = 0
    st.session_state.wrong_cards = []
    st.session_state.pop("save_error", None)


def save_wrong(unit, term, meaning):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(WRONGS_PATH, "a", encoding="utf-8") as file:
        file.write(f"{timestamp} | [{unit}] {term}: {meaning}\n")


def mark_card(correct):
    source_unit, term, meaning = st.session_state.deck[st.session_state.card_index]
    if correct:
        st.session_state.correct_count += 1
    else:
        st.session_state.wrong_cards.append((source_unit, term, meaning))
        try:
            save_wrong(source_unit, term, meaning)
        except OSError as error:
            st.session_state.save_error = str(error)

    st.session_state.card_index += 1
    st.session_state.show_answer = False


def run_quiz(unit, cards, prompts):
    if st.session_state.get("quiz_unit") != unit:
        start_unit(unit, cards)

    deck = st.session_state.deck
    index = st.session_state.card_index
    total = len(deck)
    if st.session_state.get("save_error"):
        st.warning(f"錯題仍保留在本次練習中，但無法寫入檔案：{st.session_state.save_error}")

    if index >= total:
        correct = st.session_state.correct_count
        accuracy = correct / total * 100 if total else 0
        st.progress(1.0)
        st.success("🎉 本次練習完成！")
        st.metric("自評答對率", f"{accuracy:.0f}%", f"{correct} / {total} 張")

        wrong_cards = st.session_state.wrong_cards
        if wrong_cards:
            st.write("這次標記為「還不熟」的詞：")
            for source_unit, term, meaning in wrong_cards:
                st.markdown(f"- **{term}**：{meaning}（{source_unit}）")
            if not st.session_state.get("save_error"):
                st.caption("錯題也已追加記錄到 wrongs.txt。")
            st.download_button("下載本次錯題", "\n".join(
                f"[{source_unit}] {term}: {meaning}"
                for source_unit, term, meaning in wrong_cards
            ), file_name="review.txt", mime="text/plain")
            if st.button("只重練本次不熟的卡", use_container_width=True):
                start_unit(unit, wrong_cards)
                st.rerun()
        else:
            st.info("這次沒有標記錯題。")

        if st.button("🔁 重練這個單元", use_container_width=True):
            start_unit(unit, cards)
            st.rerun()
        return

    source_unit, term, meaning = deck[index]
    st.progress(index / total)
    st.caption(f"第 {index + 1} / {total} 張 · {source_unit}")
    st.caption(f"詞彙索引：{term}")
    question = prompts.get((source_unit, term), f"在「{source_unit}」中，{term} 的全名或意義與主要用途是什麼？")
    st.markdown(f"### {question}")

    if not st.session_state.show_answer:
        if st.button("👀 顯示解釋", type="primary", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()
        st.caption("先依題目回想，再翻開答案。")
        return

    st.markdown(f"📖 **全名／解釋**：{meaning}")
    st.write("看完答案後，依照自己剛才是否答對來評估：")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 我知道", use_container_width=True):
            mark_card(correct=True)
            st.rerun()
    with col2:
        if st.button("❌ 還不熟", use_container_width=True):
            mark_card(correct=False)
            st.rerun()


def load_wrong_cards(flashcards):
    """Match saved mistakes to current answers; keep each unit/term once."""
    if not WRONGS_PATH.exists():
        return []
    saved = WRONGS_PATH.read_text(encoding="utf-8").splitlines()
    cards = {}
    for line in saved:
        _, separator, entry = line.partition(" | [")
        if not separator:
            continue
        unit, separator, entry = entry.partition("] ")
        term, separator2, _ = entry.partition(": ")
        if separator and separator2 and term in flashcards.get(unit, {}):
            cards[(unit, term)] = (unit, term, flashcards[unit][term])
    return list(cards.values())


def main():
    st.set_page_config(page_title="航電閃卡", page_icon="🛩️", layout="centered")
    st.title("🛩️ 航電名詞閃卡")
    st.write("選一個主題，先回想詞義，再翻開答案並自我評估。")

    flashcards = load_flashcards()
    if not flashcards:
        st.error("題庫是空的，或題庫格式無法讀取。請檢查 alias.txt。")
        return

    try:
        prompts = load_question_prompts()
        revision = hashlib.sha256(FLASHCARDS_PATH.read_bytes()).hexdigest()
    except (OSError, UnicodeError) as error:
        st.error(f"無法讀取題目：{error}")
        return
    if st.session_state.get("bank_revision") != revision:
        st.session_state.pop("quiz_unit", None)
        st.session_state.bank_revision = revision

    st.caption(f"題庫：{len(flashcards)} 個單元，共 {sum(map(len, flashcards.values()))} 張卡")
    mode = st.radio("練習方式", ["分單元練習", "全部混合練習", "歷史錯題複習"], horizontal=True)
    if mode == "分單元練習":
        selected_unit = st.selectbox("📂 練習單元", list(flashcards),
                                     format_func=lambda u: f"{u}（{len(flashcards[u])} 張）")
        cards = [(selected_unit, term, meaning) for term, meaning in flashcards[selected_unit].items()]
        quiz_key = selected_unit
    elif mode == "全部混合練習":
        cards = [(unit, term, meaning) for unit, terms in flashcards.items() for term, meaning in terms.items()]
        quiz_key = mode
    else:
        try:
            cards = load_wrong_cards(flashcards)
        except (OSError, UnicodeError) as error:
            st.error(f"無法讀取錯題紀錄：{error}")
            return
        quiz_key = mode
        if not cards:
            st.info("目前沒有歷史錯題。練習時標記「還不熟」即可加入。")
            return
    st.caption("切換練習方式或單元會開始新一輪；歷史錯題紀錄會保留。")
    if st.button("重新開始這組練習"):
        start_unit(quiz_key, cards)
    run_quiz(quiz_key, cards, prompts)


if __name__ == "__main__":
    main()

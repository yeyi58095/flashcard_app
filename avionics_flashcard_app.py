import random
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
                if not line or line.startswith("#"):
                    continue
                if line.startswith("[") and line.endswith("]"):
                    current_unit = line[1:-1].strip()
                    flashcards.setdefault(current_unit, {})
                    continue
                if current_unit and ": " in line:
                    term, meaning = line.split(": ", 1)
                    if term.strip() and meaning.strip():
                        flashcards[current_unit][term.strip()] = meaning.strip()
    except FileNotFoundError:
        st.error(f"找不到題庫檔案：{path.name}")
        return {}

    return {unit: cards for unit, cards in flashcards.items() if cards}


def start_unit(unit, cards):
    deck = list(cards.items())
    random.shuffle(deck)
    st.session_state.quiz_unit = unit
    st.session_state.deck = deck
    st.session_state.card_index = 0
    st.session_state.show_answer = False
    st.session_state.correct_count = 0
    st.session_state.wrong_cards = []


def save_wrong(unit, term, meaning):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(WRONGS_PATH, "a", encoding="utf-8") as file:
        file.write(f"{timestamp} | [{unit}] {term}: {meaning}\n")


def mark_card(correct):
    term, meaning = st.session_state.deck[st.session_state.card_index]
    if correct:
        st.session_state.correct_count += 1
    else:
        unit = st.session_state.quiz_unit
        st.session_state.wrong_cards.append((term, meaning))
        save_wrong(unit, term, meaning)

    st.session_state.card_index += 1
    st.session_state.show_answer = False


def run_quiz(unit, cards):
    if st.session_state.get("quiz_unit") != unit:
        start_unit(unit, cards)

    deck = st.session_state.deck
    index = st.session_state.card_index
    total = len(deck)

    if index >= total:
        correct = st.session_state.correct_count
        accuracy = correct / total * 100 if total else 0
        st.success("🎉 本單元練習完成！")
        st.metric("自評答對率", f"{accuracy:.0f}%", f"{correct} / {total} 張")

        wrong_cards = st.session_state.wrong_cards
        if wrong_cards:
            st.write("這次標記為「還不熟」的詞：")
            for term, meaning in wrong_cards:
                st.markdown(f"- **{term}**：{meaning}")
            st.caption("錯題也已追加記錄到 wrongs.txt。")
        else:
            st.info("這次沒有標記錯題。")

        if st.button("🔁 重練這個單元", use_container_width=True):
            start_unit(unit, cards)
            st.rerun()
        return

    term, meaning = deck[index]
    st.progress(index / total)
    st.caption(f"第 {index + 1} / {total} 張 · {unit}")
    st.markdown(f"### 🔤 {term}")

    if not st.session_state.show_answer:
        if st.button("👀 顯示解釋", type="primary", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()
        st.caption("先想想這個詞代表什麼，再翻開卡片。")
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


def main():
    st.set_page_config(page_title="航電閃卡", page_icon="🛩️", layout="centered")
    st.title("🛩️ 航電名詞閃卡")
    st.write("選一個主題，先回想詞義，再翻開答案並自我評估。")

    flashcards = load_flashcards()
    if not flashcards:
        st.error("題庫是空的，或題庫格式無法讀取。請檢查 alias.txt。")
        return

    units = list(flashcards)
    selected_unit = st.selectbox("📂 練習單元", units)
    run_quiz(selected_unit, flashcards[selected_unit])


if __name__ == "__main__":
    main()

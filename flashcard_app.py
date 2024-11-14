import streamlit as st
import random

# 顯示內容的顏色
def colored_text(text, color):
    return f'<span style="color:{color}">{text}</span>'

# 加載卡片資料
def load_flashcards(filename="flashcards.txt"):
    flashcards = {}
    learn_only_units = set()
    current_unit = None
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("[") and line.endswith("]"):
                    current_unit = line[1:-1]
                    if "(learn-only)" in current_unit:
                        current_unit = current_unit.replace(" (learn-only)", "")
                        learn_only_units.add(current_unit)
                    flashcards[current_unit] = {}
                elif current_unit and ": " in line:
                    parts = line.split(": ", 2)
                    if len(parts) == 2:
                        abbreviation, description = parts
                        flashcards[current_unit][abbreviation] = {
                            "full_name": abbreviation,
                            "description": description
                        }
                    elif len(parts) == 3:
                        abbreviation, full_name, description = parts
                        flashcards[current_unit][abbreviation] = {
                            "full_name": full_name,
                            "description": description
                        }
    except FileNotFoundError:
        st.error(f"文件 '{filename}' 未找到。請確認文件存在並重新運行。")
    return flashcards, learn_only_units

# 無範圍測驗模式
def unlimited_quiz_mode(flashcards, learn_only_units):
    all_flashcards = [(unit, abbreviation, info) for unit, unit_flashcards in flashcards.items()
                      if unit not in learn_only_units
                      for abbreviation, info in unit_flashcards.items()]
    random.shuffle(all_flashcards)
    total_questions = len(all_flashcards)
    correct_answers = 0
    incorrect_answers = []

    for unit, abbreviation, info in all_flashcards:
        user_answer = st.text_input(f"請輸入 '{abbreviation}' 的全名 (單元: {unit}):", key=f"{unit}-{abbreviation}")
        if user_answer:
            if user_answer.strip().lower() == info["full_name"].lower():
                st.markdown(colored_text("正確！", "green"), unsafe_allow_html=True)
                correct_answers += 1
            else:
                st.markdown(colored_text(f"錯誤！正確答案是：{info['full_name']}", "red"), unsafe_allow_html=True)
                incorrect_answers.append((abbreviation, info["full_name"]))
            st.write(f"用途: {info['description']}\n")

    # 顯示答錯的題目和答對率
    if st.button("完成測驗"):
        st.write("測驗結束！")
        if incorrect_answers:
            st.write("你答錯的題目：")
            for abbreviation, full_name in incorrect_answers:
                st.write(f"{abbreviation}: {full_name}")
        st.write(f"答對率: {correct_answers / total_questions * 100:.2f}%")

# 主程式
def main():
    st.title("Flashcards 無範圍測驗系統")
    flashcards, learn_only_units = load_flashcards()
    if not flashcards:
        st.error("無法載入卡片資料，請檢查文件內容。")
        return

    st.write("選擇無範圍測驗模式，系統將隨機顯示題目，請輸入答案。")
    if st.button("開始測驗"):
        unlimited_quiz_mode(flashcards, learn_only_units)

if __name__ == "__main__":
    main()

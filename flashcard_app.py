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

# 初始化測驗狀態
def initialize_quiz(flashcards, learn_only_units):
    if "quiz_data" not in st.session_state:
        all_flashcards = [(unit, abbreviation, info) for unit, unit_flashcards in flashcards.items()
                          if unit not in learn_only_units
                          for abbreviation, info in unit_flashcards.items()]
        random.shuffle(all_flashcards)
        st.session_state.quiz_data = {
            "all_flashcards": all_flashcards,
            "current_question": 0,
            "correct_answers": 0,
            "incorrect_answers": []
        }

# 回调函数，用于清空输入框并处理答案
def submit_answer():
    quiz_data = st.session_state.quiz_data
    current_question = quiz_data["current_question"]
    unit, abbreviation, info = quiz_data["all_flashcards"][current_question]
    user_answer = st.session_state[f"answer_{current_question}"]

    if user_answer.strip().lower() == info["full_name"].lower():
        st.session_state.result = colored_text("正確！", "green")
        quiz_data["correct_answers"] += 1
    else:
        st.session_state.result = colored_text(f"錯誤！正確答案是：{info['full_name']}", "red")
        quiz_data["incorrect_answers"].append((abbreviation, info["full_name"]))

    quiz_data["current_question"] += 1  # 增加当前问题的索引
    st.session_state[f"answer_{current_question}"] = ""  # 清空当前输入框内容

# 無範圍測驗模式
def unlimited_quiz_mode():
    quiz_data = st.session_state.quiz_data
    total_questions = len(quiz_data["all_flashcards"])

    if quiz_data["current_question"] < total_questions:
        unit, abbreviation, info = quiz_data["all_flashcards"][quiz_data["current_question"]]
        
        st.text_input(
            f"請輸入 '{abbreviation}' 的全名 (單元: {unit}):",
            key=f"answer_{quiz_data['current_question']}",
            on_change=submit_answer
        )

        if "result" in st.session_state:
            st.markdown(st.session_state.result, unsafe_allow_html=True)

    else:
        # 顯示答錯的題目和答對率
        st.write("測驗結束！")
        if quiz_data["incorrect_answers"]:
            st.write("你答錯的題目：")
            for abbreviation, full_name in quiz_data["incorrect_answers"]:
                st.write(f"{abbreviation}: {full_name}")
        st.write(f"答對率: {quiz_data['correct_answers'] / total_questions * 100:.2f}%")
        # 清空 session_state，允許重新開始
        if st.button("重新測驗"):
            del st.session_state.quiz_data
            del st.session_state.result

# 主程式
def main():
    st.title("Flashcards 無範圍測驗系統")
    flashcards, learn_only_units = load_flashcards()
    if not flashcards:
        st.error("無法載入卡片資料，請檢查文件內容。")
        return

    st.write("選擇無範圍測驗模式，系統將隨機顯示題目，請輸入答案。")
    
    if st.button("開始測驗"):
        initialize_quiz(flashcards, learn_only_units)
    if "quiz_data" in st.session_state:
        unlimited_quiz_mode()

if __name__ == "__main__":
    main()

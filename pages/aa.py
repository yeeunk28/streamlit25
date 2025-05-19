import streamlit as st
import random

st.title("속담 퀴즈 + 복습")

idioms = {
    "Break the ice": "긴장을 풀다, 분위기를 부드럽게 만들다",
    "Hit the books": "열심히 공부하다",
    "Piece of cake": "아주 쉬운 일",
    "Let the cat out of the bag": "비밀을 누설하다",
    "Costs an arm and a leg": "엄청 비싸다",
    "Once in a blue moon": "아주 드물게",
    "Under the weather": "몸이 아픈",
    "Bite the bullet": "이를 악물고 참다",
    "Burn the midnight oil": "밤늦게까지 공부하거나 일하다",
    "Kick the bucket": "죽다"
}

if "wrong_idioms" not in st.session_state:
    st.session_state.wrong_idioms = {}

def new_question():
    question = random.choice(list(idioms.items()))
    correct_answer = question[1]

    options = [correct_answer]
    all_meanings = list(idioms.values())
    all_meanings.remove(correct_answer)
    options += random.sample(all_meanings, min(3, len(all_meanings)))
    random.shuffle(options)

    st.session_state.current_question = question
    st.session_state.options = options
    st.session_state.answered = False
    st.session_state.selected_option = None

if "current_question" not in st.session_state:
    new_question()

tabs = st.tabs(["퀴즈", "틀린 속담 복습"])

with tabs[0]:
    st.header("속담 퀴즈")

    idiom, correct_meaning = st.session_state.current_question
    options = st.session_state.options

    selected = st.radio(f"'{idiom}'의 뜻은 무엇일까요?", options, index=options.index(st.session_state.selected_option) if st.session_state.selected_option in options else 0)
    st.session_state.selected_option = selected

    if not st.session_state.answered:
        if st.button("정답 확인"):
            st.session_state.answered = True
            if selected == correct_meaning:
                st.success("정답이에요! 🎉")
            else:
                st.error(f"틀렸어요... 정답은 '{correct_meaning}' 입니다.")
                st.session_state.wrong_idioms[idiom] = correct_meaning
    else:
        col1, col2 = st.columns(2)

        if col1.button("다음 문제"):
            new_question()

        if col2.button("게임 재시작"):
            st.session_state.wrong_idioms = {}
            new_question()

with tabs[1]:
    st.header("틀린 속담 복습")

    if st.session_state.wrong_idioms:
        for idiom, meaning in st.session_state.wrong_idioms.items():
            st.markdown(f"**{idiom}**: {meaning}")
        if st.button("틀린 속담 초기화"):
            st.session_state.wrong_idioms = {}
    else:
        st.write("아직 틀린 속담이 없습니다. 퀴즈를 풀어보세요!")

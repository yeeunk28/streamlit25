import streamlit as st
import random

st.title("📚 영어 속담 퀴즈 + 복습")

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

if "current_question" not in st.session_state:
    # 문제 하나 랜덤 선택
    st.session_state.current_question = random.choice(list(idioms.items()))
    st.session_state.answered = False  # 답변 여부
    st.session_state.selected_option = None

tabs = st.tabs(["퀴즈", "틀린 속담 복습"])

with tabs[0]:
    st.header("속담 퀴즈")

    idiom, correct_meaning = st.session_state.current_question

    options = list(idioms.values())
    random.shuffle(options)

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
        # 정답 확인 후 다음 문제 버튼 보여주기
        if st.button("다음 문제"):
            st.session_state.current_question = random.choice(list(idioms.items()))
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.experimental_rerun()

with tabs[1]:
    st.header("틀린 속담 복습")

    if st.session_state.wrong_idioms:
        for idiom, meaning in st.session_state.wrong_idioms.items():
            st.markdown(f"**{idiom}**: {meaning}")
        if st.button("틀린 속담 초기화"):
            st.session_state.wrong_idioms = {}
            st.experimental_rerun()
    else:
        st.write("아직 틀린 속담이 없습니다. 퀴즈를 풀어보세요!")

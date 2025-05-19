import streamlit as st
import random

st.title("📚 영어 속담 퀴즈 + 복습")

# 속담 데이터
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

# 틀린 문제를 저장할 세션 상태 초기화
if "wrong_idioms" not in st.session_state:
    st.session_state.wrong_idioms = {}

tabs = st.tabs(["퀴즈", "틀린 속담 복습"])

with tabs[0]:
    st.header("속담 퀴즈")

    quiz_idiom, quiz_meaning = random.choice(list(idioms.items()))
    options = list(idioms.values())
    random.shuffle(options)

    answer = st.radio(f"'{quiz_idiom}'의 뜻은 무엇일까요?", options)

    if st.button("정답 확인"):
        if answer == quiz_meaning:
            st.success("정답이에요! 🎉")
        else:
            st.error(f"틀렸어요... 정답은 '{quiz_meaning}' 입니다.")
            # 틀린 문제 세션 상태에 저장 (중복 저장 방지)
            st.session_state.wrong_idioms[quiz_idiom] = quiz_meaning

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

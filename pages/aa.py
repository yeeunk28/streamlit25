import streamlit as st
import random

st.title("📚 영어 속담 & 관용구 학습과 퀴즈")

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

# 속담 랜덤 출력
idiom, meaning = random.choice(list(idioms.items()))
st.markdown(f"### 오늘의 속담: **{idiom}**")
if st.checkbox("뜻 보기"):
    st.markdown(f"**뜻:** {meaning}")

# 퀴즈 시작
st.markdown("---")
st.header("속담 퀴즈")

quiz_idiom, quiz_meaning = random.choice(list(idioms.items()))
options = list(idioms.values())
random.shuffle(options)

answer = st.radio(
    f"'{quiz_idiom}'의 뜻은 무엇일까요?",
    options
)

if st.button("정답 확인"):
    if answer == quiz_meaning:
        st.success("정답이에요! 🎉")
    else:
        st.error(f"틀렸어요... 정답은 '{quiz_meaning}' 입니다.")

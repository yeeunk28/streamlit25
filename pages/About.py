import streamlit as st

st.write("This app is under construction.")

url="https://github.com/yeeunk28/streamlit25/raw/main/images/image01.png"
st.image(url, caption="Image link", width=300)  # width in pixels

import streamlit as st
from gtts import gTTS
import os

st.set_page_config(page_title="Easy English with Teacher [Your Name]", layout="wide")

st.title("🎓 Easy English - 중학생을 위한 영어 홈클래스")

menu = st.sidebar.selectbox("메뉴를 선택하세요", ["오늘의 표현", "단어 퀴즈", "문법 코너", "대화 연습"])

if menu == "오늘의 표현":
    st.subheader("📢 오늘의 표현")
    sentence = "How was your day?"
    st.markdown(f"**{sentence}**")
    
    tts = gTTS(sentence)
    tts.save("day.mp3")
    audio_file = open("day.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

elif menu == "단어 퀴즈":
    st.subheader("🧠 단어 퀴즈")
    # 예시 문제
    st.write("🍎 이 그림은 무엇일까요?")
    answer = st.radio("정답을 고르세요", ["apple", "banana", "grape"])
    if answer == "apple":
        st.success("정답입니다!")
    else:
        st.error("다시 생각해보세요!")

# 추가 기능은 이후 점차 확장 가능

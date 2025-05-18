import streamlit as st

st.write("This app is under construction.")

url="https://github.com/yeeunk28/streamlit25/raw/main/images/image01.png"
st.image(url, caption="Image link", width=300)  # width in pixels

import streamlit as st
import random

# ------------------- 설정 -------------------

WORD_LIST = ['apple', 'banana', 'school', 'friend', 'english', 'guitar', 'teacher', 'travel', 'morning', 'computer']
MAX_TRIES = 6

# ------------------- 세션 상태 초기화 -------------------

if 'word' not in st.session_state:
    st.session_state.word = random.choice(WORD_LIST)
    st.session_state.guessed = []
    st.session_state.tries_left = MAX_TRIES
    st.session_state.message = ""

# ------------------- 함수 정의 -------------------

def display_word(word, guessed):
    return ' '.join([letter if letter in guessed else '_' for letter in word])

def reset_game():
    st.session_state.word = random.choice(WORD_LIST)
    st.session_state.guessed = []
    st.session_state.tries_left = MAX_TRIES
    st.session_state.message = ""

# ------------------- UI 출력 -------------------

st.title("🎮 Hangman: 영어 단어 맞추기")
st.markdown("중학교 수준의 영어 단어를 맞춰보세요. 기회는 총 6번!")

st.write(f"단어: {display_word(st.session_state.word, st.session_state.guessed)}")
st.write(f"남은 기회: {st.session_state.tries_left}번")

# ------------------- 입력 처리 -------------------

guess = st.text_input("알파벳을 입력하세요 (a-z):", max_chars=1)

if st.button("제출"):
    if not guess.isalpha() or len(guess) != 1:
        st.warning("한 글자의 알파벳을 입력하세요.")
    elif guess in st.session_state.guessed:
        st.info("이미 입력한 알파벳이에요.")
    else:
        st.session_state.guessed.append(guess.lower())
        if guess.lower() not in st.session_state.word:
            st.session_state.tries_left -= 1
            st.session_state.message = f"❌ '{guess}'는 단어에 없어요!"
        else:
            st.session_state.message = f"✅ 잘했어요! '{guess}'는 단어에 있어요!"

# ------------------- 게임 상태 확인 -------------------

st.write(st.session_state.message)

if all(letter in st.session_state.guessed for letter in st.session_state.word):
    st.success(f"🎉 정답입니다! 단어는 '{st.session_state.word}' 였어요.")
    if st.button("🔁 다시 시작하기"):
        reset_game()

elif st.session_state.tries_left == 0:
    st.error(f"😢 실패! 정답은 '{st.session_state.word}' 였어요.")
    if st.button("🔁 다시 시작하기"):
        reset_game()


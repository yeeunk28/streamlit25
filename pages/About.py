import streamlit as st
import pandas as pd
import random
import os

# ------------------- 설정 -------------------
CSV_PATH = "data/word_frequency (1).csv"
MAX_TRIES = 6

# ------------------- 데이터 로드 -------------------
@st.cache_data
def load_words(csv_path):
    df = pd.read_csv(csv_path)
    if 'word' not in df.columns:
        st.error("❗ 'word'라는 이름의 컬럼이 CSV에 없습니다.")
        return []
    return df['word'].dropna().astype(str).tolist()

WORD_LIST = load_words(CSV_PATH)

if not WORD_LIST:
    st.stop()

# ------------------- 세션 상태 초기화 -------------------
if 'word' not in st.session_state:
    st.session_state.word = random.choice(WORD_LIST).lower()
    st.session_state.guessed = []
    st.session_state.tries_left = MAX_TRIES
    st.session_state.message = ""

# ------------------- 함수 정의 -------------------
def display_word(word, guessed):
    return ' '.join([letter if letter in guessed else '_' for letter in word])

def get_letter_positions(word, letter):
    return [str(i + 1) for i, l in enumerate(word) if l == letter]

def reset_game():
    st.session_state.word = random.choice(WORD_LIST).lower()
    st.session_state.guessed = []
    st.session_state.tries_left = MAX_TRIES
    st.session_state.message = ""

# ------------------- UI 출력 -------------------
st.title("🎮 Hangman: 단어 추측 게임")

st.write(f"단어: {display_word(st.session_state.word, st.session_state.guessed)}")
st.write(f"남은 기회: {st.session_state.tries_left}번")

# ------------------- 사용자 입력 -------------------
guess = st.text_input("알파벳을 입력하세요 (a-z):", max_chars=1)

if st.button("제출"):
    if not guess.isalpha() or len(guess) != 1:
        st.warning("한 글자의 알파벳을 입력하세요.")
    elif guess.lower() in st.session_state.guessed:
        st.info("이미 입력한 알파벳이에요.")
    else:
        st.session_state.guessed.append(guess.lower())
        if guess.lower() not in st.session_state.word:
            st.session_state.tries_left -= 1
            st.session_state.message = f"❌ '{guess}'는 단어에 없어요!"
        else:
            positions = get_letter_positions(st.session_state.word, guess.lower())
            st.session_state.message = f"✅ 잘했어요! '{guess}'는 단어에 있어요!\n📍 위치: {', '.join(positions)}번 글자"

st.write(st.session_state.message)

# ------------------- 게임 종료 조건 -------------------
if all(letter in st.session_state.guessed for letter in st.session_state.word):
    st.success(f"🎉 정답입니다! 단어는 '{st.session_state.word}' 였어요.")
    if st.button("🔁 다시 시작하기"):
        reset_game()

elif st.session_state.tries_left == 0:
    st.error(f"😢 실패! 정답은 '{st.session_state.word}' 였어요.")
    if st.button("🔁 다시 시작하기"):
        reset_game()

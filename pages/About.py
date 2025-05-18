import streamlit as st
import pandas as pd
import random
import os

# ----------------- 설정 -----------------
CSV_PATH = "data/word_frequency (1).csv"
MAX_TRIES = 6

# ----------------- 데이터 로드 -----------------
@st.cache_data
def load_words(csv_path):
    df = pd.read_csv(csv_path)

    # 첫 번째 컬럼 이름 가져오기
    first_col = df.columns[0]
    st.info(f"📄 단어는 CSV의 '{first_col}' 컬럼에서 불러왔어요.")

    return df[first_col].dropna().astype(str).tolist()

WORD_LIST = load_words(CSV_PATH)

if not WORD_LIST:
    st.error("❗ 단어 리스트를 불러오지 못했습니다.")
    st.stop()

# ----------------- 세션 상태 초기화 -----------------
if 'word' not in st.session_state:
    st.session_state.word = random.choice(WORD_LIST).lower()
    st.session_state.guessed = []
    st.session_state.tries_left = MAX_TRIES
    st.session_state.message = ""

# ----------------- 함수 정의 -----------------
def display_word(word, guessed):
    return ' '.join([letter if letter in guessed else '_' for letter in word])

def get_letter_positions(word, letter):
    return [str(i + 1) for i, l in enumerate(word) if l == letter]

def reset_game():
    st.session_state.word = random.choice(WORD_LIST).lower()
    st.session_state.guessed = []
    st.session_state.tries_left = MAX_TRIES
    st.session_state.message = ""

# ----------------- UI -----------------
st.title("🎮 영어 단어 Hangman 게임")
st.write("CSV 파일에서 단어를 불러와서 행맨 게임을 해보세요!")

st.write(f"단어: {display_word(st.session_state.word, st.session_state.guessed)}")
st.write(f"남은 시도: {st.session_state.tries_left}번")

# ----------------- 입력 -----------------
guess = st.text_input("알파벳을 입력하세요 (a-z):", max_chars=1)

if st.button("제출"):
    if not guess.isalpha() or len(guess) != 1:
        st.warning("❗ 알파벳 한 글자를 입력해주세요.")
    elif guess.lower() in st.session_state.guessed:
        st.info("이미 입력한 알파벳이에요.")
    else:
        st.session_state.guessed.append(guess.lower())
        if guess.lower() not in st.session_state.word:
            st.session_state.tries_left -= 1
            st.session_state.message = f"❌ '{guess}'는 단어에 없어요!"
        else:
            positions = get_letter_positions(st.session_state.word, guess.lower())
            st.session_state.message = f"✅ 잘했어요! '{guess}'는 {', '.join(positions)}번째 글자에 있어요."

st.write(st.session_state.message)

# ----------------- 게임 종료 -----------------
if all(letter in st.session_state.guessed for letter in st.session_state.word):
    st.success(f"🎉 정답입니다! 단어는 '{st.session_state.word}' 였어요.")
    if st.button("🔁 다시 시작하기"):
        reset_game()

elif st.session_state.tries_left == 0:
    st.error(f"😢 실패! 정답은 '{st.session_state.word}' 였어요.")
    if st.button("🔁 다시 시작하기"):
        reset_game()

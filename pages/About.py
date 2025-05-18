import streamlit as st
import random
import pandas as pd

CSV_PATH = "data/word_frequency (1).csv"
MAX_TRIES = 6

HANGMAN_PICS = [
    ''' +---+
  |   |
      |
      |
      |
      |
=========''', 
    ''' +---+
  |   |
  O   |
      |
      |
      |
=========''', 
    ''' +---+
  |   |
  O   |
  |   |
      |
      |
=========''', 
    ''' +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', 
    ''' +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========''', 
    ''' +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========''', 
    ''' +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
========='''
]

def load_words(csv_path):
    df = pd.read_csv(csv_path)
    first_col = df.columns[0]
    words = df[first_col].dropna().astype(str).tolist()
    words = [w.lower() for w in words if w.isalpha()]
    return words

def display_word(word, guessed):
    return ' '.join([letter if letter in guessed else '_' for letter in word])

def start_new_game(words):
    word = random.choice(words)
    return word, [], MAX_TRIES, ""

def main():
    st.title("🎮 Hangman Game & Word Review")

    words = load_words(CSV_PATH)

    # 세션 상태 초기화
    if 'word' not in st.session_state:
        st.session_state.word, st.session_state.guessed, st.session_state.tries_left, st.session_state.message = start_new_game(words)
    if 'wrong_words' not in st.session_state:
        st.session_state.wrong_words = []

    tabs = st.tabs(["Hangman Game", "Wrong Words Review"])

    with tabs[0]:
        # 행맨 게임 탭
        index = MAX_TRIES - st.session_state.tries_left
        index = max(0, min(index, len(HANGMAN_PICS) - 1))
        st.text(HANGMAN_PICS[index])

        st.write(f"Word: {display_word(st.session_state.word, st.session_state.guessed)}")
        st.write(f"Tries left: {st.session_state.tries_left}")
        st.write(f"Guessed letters: {', '.join(st.session_state.guessed)}")
        st.write(st.session_state.message)

        with st.form(key='guess_form'):
            letter = st.text_input("Guess a letter (a-z):", max_chars=1).lower()
            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if len(letter) != 1 or not letter.isalpha():
                st.session_state.message = "❗ Please enter a single alphabet letter."
            elif letter in st.session_state.guessed:
                st.session_state.message = f"You already guessed '{letter}'."
            else:
                st.session_state.guessed.append(letter)
                if letter in st.session_state.word:
                    positions = [str(i+1) for i, l in enumerate(st.session_state.word) if l == letter]
                    st.session_state.message = f"✅ Correct! Letter '{letter}' is at position(s): {', '.join(positions)}."
                else:
                    st.session_state.tries_left -= 1
                    if st.session_state.tries_left < 0:
                        st.session_state.tries_left = 0
                    st.session_state.message = f"❌ Wrong! Letter '{letter}' is not in the word."

            # 게임 종료 조건 체크
            if all(l in st.session_state.guessed for l in st.session_state.word):
                st.success(f"🎉 You won! The word was '{st.session_state.word}'.")
                # 틀린 단어 기록 초기화 (승리 후 다시 시작 시)
                st.session_state.wrong_words = []
            elif st.session_state.tries_left == 0:
                st.error(f"😢 Game Over! The word was '{st.session_state.word}'.")
                # 틀린 단어 리스트에 저장 (게임 끝난 단어)
                if st.session_state.word not in st.session_state.wrong_words:
                    st.session_state.wrong_words.append(st.session_state.word)

        if st.button("Restart Game"):
            st.session_state.word, st.session_state.guessed, st.session_state.tries_left, st.session_state.message = start_new_game(words)

    with tabs[1]:
        # 틀린 단어 복습 탭
        st.header("📚 Review Your Wrong Words")
        if st.session_state.wrong_words:
            for w in st.session_state.wrong_words:
                st.write(f"- **{w}**")
        else:
            st.write("You haven't missed any words yet! Keep playing the game to see wrong words here.")

if __name__ == "__main__":
    main()

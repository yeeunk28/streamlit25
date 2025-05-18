import streamlit as st
import random
import pandas as pd

# CSV 파일 경로 (data 폴더 안에 있다고 가정)
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
    # 영어 단어 소문자 변환 및 필터링 (알파벳만)
    words = [w.lower() for w in words if w.isalpha()]
    return words

def display_word(word, guessed):
    return ' '.join([letter if letter in guessed else '_' for letter in word])

def start_new_game(words):
    word = random.choice(words)
    return word, [], MAX_TRIES, ""

def main():
    st.title("🎮 Hangman Game with Streamlit")
    
    # 단어 리스트 불러오기 (한 번만)
    words = load_words(CSV_PATH)
    
    if 'word' not in st.session_state:
        st.session_state.word, st.session_state.guessed, st.session_state.tries_left, st.session_state.message = start_new_game(words)
    
    st.text(HANGMAN_PICS[MAX_TRIES - st.session_state.tries_left])
    st.write(f"Word: {display_word(st.session_state.word, st.session_state.guessed)}")
    st.write(f"Tries left: {st.session_state.tries_left}")
    st.write(f"Guessed letters: {', '.join(st.session_state.guessed)}")
    st.write(st.session_state.message)

    letter = st.text_input("Guess a letter (a-z):", max_chars=1).lower()

    if st.button("Submit"):
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
                st.session_state.message = f"❌ Wrong! Letter '{letter}' is not in the word."

        # 승리 조건
        if all(l in st.session_state.guessed for l in st.session_state.word):
            st.success(f"🎉 You won! The word was '{st.session_state.word}'.")
        # 패배 조건
        elif st.session_state.tries_left == 0:
            st.error(f"😢 Game Over! The word was '{st.session_state.word}'.")
    
    if st.button("Restart Game"):
        st.session_state.word, st.session_state.guessed, st.session_state.tries_left, st.session_state.message = start_new_game(words)

if __name__ == "__main__":
    main()

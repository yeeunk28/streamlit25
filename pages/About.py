import gradio as gr
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
    return df[first_col].dropna().astype(str).tolist()

WORD_LIST = load_words(CSV_PATH)

# 게임 상태 초기화 함수
def new_game():
    word = random.choice(WORD_LIST).lower()
    guessed = []
    tries_left = MAX_TRIES
    message = ""
    return word, guessed, tries_left, message

# 단어 화면에 표시할 때 밑줄과 맞춘 글자 보여주기
def display_word(word, guessed):
    return ' '.join([letter if letter in guessed else '_' for letter in word])

# 한 글자 입력해서 게임 진행하는 함수
def guess_letter(letter, word, guessed, tries_left, message):
    letter = letter.lower()
    if len(letter) != 1 or not letter.isalpha():
        message = "❗ Please enter a single alphabet letter."
        return word, guessed, tries_left, message, display_word(word, guessed), HANGMAN_PICS[MAX_TRIES - tries_left]
    if letter in guessed:
        message = f"You already guessed '{letter}'."
        return word, guessed, tries_left, message, display_word(word, guessed), HANGMAN_PICS[MAX_TRIES - tries_left]

    guessed.append(letter)
    if letter not in word:
        tries_left -= 1
        message = f"❌ '{letter}' is not in the word."
    else:
        positions = [str(i + 1) for i, l in enumerate(word) if l == letter]
        message = f"✅ Good job! '{letter}' is in position(s): {', '.join(positions)}."

    current_display = display_word(word, guessed)
    hangman_pic = HANGMAN_PICS[MAX_TRIES - tries_left]

    if all(l in guessed for l in word):
        message = f"🎉 Congratulations! The word was '{word}'."
    elif tries_left == 0:
        message = f"😢 Game Over! The word was '{word}'."

    return word, guessed, tries_left, message, current_display, hangman_pic

# 재시작 버튼 함수
def restart_game():
    return new_game() + ("", display_word(*new_game()[:2]), HANGMAN_PICS[0])

with gr.Blocks() as demo:
    word, guessed, tries_left, message = new_game()

    word_state = gr.State(word)
    guessed_state = gr.State(guessed)
    tries_state = gr.State(tries_left)
    message_state = gr.State(message)

    gr.Markdown("## 🎮 English Word Hangman Game (Gradio)")
    hangman_display = gr.Textbox(value=HANGMAN_PICS[0], interactive=False, lines=7)
    word_display = gr.Textbox(value=display_word(word, guessed), interactive=False)
    tries_display = gr.Text(f"Tries left: {tries_left}")
    message_display = gr.Textbox(value=message, interactive=False)

    letter_input = gr.Textbox(label="Enter a letter (a-z):", max_chars=1)
    submit_btn = gr.Button("Submit")
    restart_btn = gr.Button("Restart Game")

    def update_ui(letter, word, guessed, tries_left, message):
        return guess_letter(letter, word, guessed, tries_left, message)

    submit_btn.click(
        update_ui,
        inputs=[letter_input, word_state, guessed_state, tries_state, message_state],
        outputs=[word_state, guessed_state, tries_state, message_state, word_display, hangman_display]
    )

    restart_btn.click(
        restart_game,
        inputs=[],
        outputs=[word_state, guessed_state, tries_state, message_state, word_display, hangman_display]
    )

demo.launch()

import streamlit as st
import random
from gtts import gTTS
import tempfile

# 문장 리스트
sentences = [
    ["Leo", "and", "his", "friends", "discovered", "a", "path", "leading", "to", "the", "Whispering", "Woods", ",", "known", "for", "the", "trees", "that", "could", "talk"],
    ["The", "locals", "avoided", "it,", "saying", "it", "was", "bewitched", ",", "but", "the", "adventurous", "teens", "couldn’t", "resist", "exploring"],
    ["As", "they", "walked", "deeper", "into", "the", "woods", ",", "the", "trees", "started", "whispering"],
    ["Each", "tree", "told", "stories", "of", "ancient", "times", ",", "of", "battles", "fought", "and", "lovers", "separated"],
    ["The", "trees", "also", "warned", "them", "about", "the", "dangers", "of", "forgetting", "the", "past", "and", "the", "importance", "of", "nature"],
    ["Moved", "by", "these", "stories,", "the", "friends", "promised", "to", "protect", "the", "woods", "and", "share", "their", "knowledge"],
    ["They", "left", "the", "woods", "wiser,", "with", "a", "deeper", "respect", "for", "nature", "and", "its", "untold", "stories", ",", "ready", "to", "advocate", "for", "its", "preservation"]
]

# 세션 상태 초기화
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'selected_words' not in st.session_state:
    st.session_state.selected_words = []
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'show_options' not in st.session_state:
    st.session_state.show_options = False

# TTS 함수
def play_tts():
    current_sentence = ' '.join(sentences[st.session_state.current_index])
    tts = gTTS(current_sentence)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        audio_file = open(tmp_file.name, "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        audio_file.close()

# 퀴즈 시작
def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.current_index = 0
    st.session_state.selected_words = []
    st.session_state.show_options = False
    play_tts()

# 단어 선택
def select_word(word_with_index):
    word, index = word_with_index
    st.session_state.selected_words.append((word, index))

# 정답 제출
def submit_answer():
    correct_sentence = sentences[st.session_state.current_index]
    selected = [word for word, idx in st.session_state.selected_words]
    if selected == correct_sentence:
        st.success("Correct! 🎉")
        st.session_state.show_options = True
    else:
        st.error("Incorrect. Try again!")

# 선택 초기화
def clear_selection():
    st.session_state.selected_words = []

# 재시도
def retry():
    clear_selection()

# 다음 문제
def next_problem():
    if st.session_state.current_index < len(sentences) - 1:
        st.session_state.current_index += 1
        st.session_state.selected_words = []
        st.session_state.show_options = False
        play_tts()
    else:
        st.balloons()
        st.session_state.quiz_started = False

# UI
st.title("🗣️ Digital English Word Order Quiz")

if not st.session_state.quiz_started:
    st.button("🎬 Start Quiz", on_click=start_quiz)
else:
    correct_sentence = sentences[st.session_state.current_index]
    shuffled_words = list(enumerate(correct_sentence))
    random.shuffle(shuffled_words)

    st.markdown("### 🔠 Arrange the words in the correct order by clicking:")

    # 가로 정렬된 단어 버튼
    max_columns = 6
    for i in range(0, len(shuffled_words), max_columns):
        row = st.columns(max_columns)
        for j, (idx, word) in enumerate(shuffled_words[i:i + max_columns]):
            if (word, idx) not in st.session_state.selected_words:
                with row[j]:
                    if st.button(word, key=f"{word}_{idx}"):
                        select_word((word, idx))

    # 선택된 문장
    selected_display = ' '.join([word for word, idx in st.session_state.selected_words])
    st.markdown("### ✍️ Your Answer:")
    st.markdown(f"**{selected_display}**")

    st.button("✅ Submit", on_click=submit_answer)
    st.button("🗑️ Clear", on_click=clear_selection)

    if st.session_state.show_options:
        st.button("🔁 Retry", on_click=retry)
        st.button("➡️ Next", on_click=next_problem)

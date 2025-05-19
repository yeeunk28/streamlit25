# 발음 평가기 (Pronunciation Checker)
import gradio as gr
import speech_recognition as sr

recognizer = sr.Recognizer()
target_word = "environment"  # 예시 단어

def check_pronunciation(audio):
    try:
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            if text.lower().strip() == target_word.lower():
                return f"✅ Great! You said: {text}"
            else:
                return f"❌ You said: {text} (Try again: say '{target_word}')"
    except Exception as e:
        return f"⚠️ Error: {e}"

interface = gr.Interface(
    fn=check_pronunciation,
    inputs=gr.Audio(source="microphone", type="filepath"),
    outputs="text",
    title="🎤 Pronunciation Checker",
    description=f"Say the word: **{target_word}** and get instant feedback!"
)

interface.launch()

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="중학생 영어 회화 연습 GPT", page_icon="🗣️")

st.title("🗣️ 영어 회화 연습 챗봇 (OpenAI API 필요)")

# API 키 입력 받기
api_key = st.text_input("🔑 OpenAI API Key를 입력하세요:", type="password")

# 대화 주제 선택
topic = st.selectbox(
    "연습하고 싶은 주제를 선택하세요:",
    ["자기소개", "음식 주문", "학교 생활", "친구와 대화", "여행"]
)

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a kind and patient English teacher speaking to a Korean middle school student. Keep sentences simple and encouraging."}
    ]

# 사용자 입력 받기
user_input = st.text_input("📝 영어로 문장을 입력해보세요:")

# OpenAI 호출 및 답변 생성
if api_key and user_input:
    client = OpenAI(api_key=api_key)
    
    # 사용자의 메시지를 세션에 저장
    st.session_state.messages.append({"role": "user", "content": f"[Topic: {topic}] {user_input}"})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        assistant_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        st.markdown(f"**🤖 GPT:** {assistant_reply}")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

# 이전 대화 보기 (펼침)
if st.session_state.messages and len(st.session_state.messages) > 1:
    with st.expander("📜 지난 대화 기록 보기"):
        for msg in st.session_state.messages[1:]:
            speaker = "👤 You" if msg["role"] == "user" else "🤖 GPT"
            st.markdown(f"**{speaker}:** {msg['content']}")

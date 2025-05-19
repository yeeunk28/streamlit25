import streamlit as st
import openai

# 🎯 제목
st.title("💬 영어 연습 챗봇 for 중학생")
st.write("GPT와 함께 영어 회화를 연습해보세요!")

# 🔑 OpenAI API 키 입력
api_key = st.text_input("🔐 OpenAI API Key를 입력하세요:", type="password")

# 📚 대화 주제 선택
topic = st.selectbox(
    "🗂️ 연습하고 싶은 주제를 선택하세요",
    ["자기소개", "음식 주문", "학교 생활", "친구와 대화", "여행"]
)

# 💬 사용자 입력창
user_input = st.text_input("📝 영어로 말해보세요:")

# 🧠 세션 상태로 대화 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a kind English teacher speaking to a Korean middle school student. Keep the conversation simple and encouraging."}
    ]

# 🔁 GPT 응답 생성
if api_key and user_input:
    openai.api_key = api_key

    # 사용자 발화 추가
    st.session_state.messages.append({"role": "user", "content": f"{topic}: {user_input}"})

    # GPT 호출
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # 출력
        st.markdown(f"**🤖 GPT:** {reply}")
    except Exception as e:
        st.error(f"⚠️ 오류 발생: {str(e)}")

# 💬 대화 이력 출력
if st.session_state.messages:
    with st.expander("📜 지난 대화 보기"):
        for msg in st.session_state.messages[1:]:
            speaker = "👤 You" if msg["role"] == "user" else "🤖 GPT"
            st.markdown(f"**{speaker}:** {msg['content']}")


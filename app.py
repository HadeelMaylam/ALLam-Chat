import streamlit as st
import requests
from streamlit_chat import message

API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = st.secrets["GROQ_API_KEY"]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

st.title("علّام الغبي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=(msg["role"] == "user"), key=f"msg_{i}")

if user_input := st.chat_input("جربني"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=f"user_{len(st.session_state.messages)}")

    # تجهيز المحادثة كاملة مع آخر سؤال
    prompt = f"اجب على الاسئله التاليه: {user_input}"
    chat_history = st.session_state.messages.copy()
    chat_history[-1] = {"role": "user", "content": prompt}

    payload = {
        "model": "allam-2-7b",
        "messages": chat_history,
        "max_tokens": 100,
        "temperature": 0.6,
    }

    res = requests.post(API_URL, headers=headers, json=payload)
    bot_reply = res.json()["choices"][0]["message"]["content"] if res.ok else f"خطأ: {res.status_code}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    message(bot_reply, key=f"bot_{len(st.session_state.messages)}")

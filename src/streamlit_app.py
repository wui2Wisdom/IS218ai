import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

st.set_page_config(page_title="ChatGPT Clone", page_icon="💬", layout="centered")

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY not found. Create a .env file with your key.")
    st.stop()

client = OpenAI(api_key=api_key)

st.sidebar.title("Settings")
model = st.sidebar.selectbox(
    "Model",
    options=["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1", "gpt-3.5-turbo"],
    index=0,
)

if "system_message" not in st.session_state:
    st.session_state.system_message = "You are a helpful assistant."
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar.expander("⚙️ Configure System Message", expanded=False):
    sys_msg = st.text_area(
        "System message",
        value=st.session_state.system_message,
        height=120,
        help="Sets the assistant's behavior and role.",
    )
    if st.button("Save system message"):
        st.session_state.system_message = sys_msg
        st.success("Updated system message.")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.toast("Chat cleared.")

st.title("💬 ChatGPT Clone")
st.caption("Educational demo using OpenAI API + Streamlit")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    chat_messages = [{"role": "system", "content": st.session_state.system_message}]
    chat_messages.extend(st.session_state.messages)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                resp = client.chat.completions.create(
                    model=model,
                    messages=chat_messages,
                    temperature=0.7,
                )
                reply = resp.choices[0].message.content
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"OpenAI API error: {e}")

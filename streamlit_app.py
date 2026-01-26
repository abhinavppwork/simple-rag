import streamlit as st
import requests

st.set_page_config(page_title="AI Document Assistant", page_icon="🤖")

st.title("🤖 AI Document Assistant")
st.caption("Ask about Tesla, Nvidia, Google, Microsoft & SpaceX")

# ---- Sidebar ----
with st.sidebar:
    st.header("📂 Knowledge Base")
    st.markdown("• Tesla\n• Nvidia\n• Google\n• Microsoft\n• SpaceX")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

# ---- Init chat ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi 👋 Ask me anything about Tesla, Nvidia, Google, Microsoft, or SpaceX."}
    ]

# ---- Display messages ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Suggested questions (only at start) ----
if len(st.session_state.messages) == 1:
    st.markdown("### 💡 Try asking")
    cols = st.columns(2)
    suggestions = [
        "Who is the CEO of Tesla?",
        "Explain Nvidia’s role in AI",
        "Who is the CEO of Google?",
        "Tell me about Microsoft Azure",
        "What is SpaceX working on?"
    ]

    for i, q in enumerate(suggestions):
        if cols[i % 2].button(q):
            st.session_state.messages.append({"role": "user", "content": q})

# ---- Chat input ----
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

# ---- If last message is user, get answer ----
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/chat",
                    json={"question": st.session_state.messages[-1]["content"]},
                    timeout=120
                )
                answer = response.json().get("answer", "No response")
            except:
                answer = "❌ Could not connect to backend"

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

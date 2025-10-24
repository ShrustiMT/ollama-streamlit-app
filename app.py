'''# app.py
import streamlit as st
import requests

st.set_page_config(page_title="Ollama Chat", page_icon="🧠")

st.title("🧠 Chat with Ollama")

# Text input box for user query
query = st.text_input("Enter your question:", "")

if st.button("Ask"):
    if query.strip() == "":
        st.warning("Please enter a question!")
    else:
        with st.spinner("Ollama is thinking..."):
            try:
                # Send request to local Ollama API
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "granite3-moe:3b", "prompt": query},
                    stream=True,
                )
                answer = ""
                for line in response.iter_lines():
                    if line:
                        data = line.decode("utf-8")
                        if '"response":"' in data:
                            answer += data.split('"response":"')[1].split('"')[0]
                st.success(answer)
            except Exception as e:
                st.error(f"Error connecting to Ollama: {e}")
'''

# app.py
import streamlit as st
import requests
import json

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Ollama Chat", page_icon="🧠", layout="centered")

# ---- HEADER ----
st.markdown(
    """
    <div style="text-align:center">
        <h1 style="color:#4B8BBE;">🧠 Chat with Ollama</h1>
        <p style="font-size:16px; color:#333;">Ask any question and get answers powered by Ollama AI!</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---- INPUT CONTAINER ----
with st.container():
    st.subheader("Enter your question below:")
    query = st.text_input("", placeholder="Type your question here...", key="query")

    if st.button("💬 Ask Ollama"):
        if not query.strip():
            st.warning("⚠️ Please enter a question!")
        else:
            with st.spinner("Ollama is thinking..."):
                try:
                    # Send streaming request to Ollama API
                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={"model": "granite3-moe:3b", "prompt": query, "max_tokens": 500},
                        stream=True,
                        timeout=60
                    )

                    # Placeholder for incremental response display
                    answer_placeholder = st.empty()
                    full_answer = ""

                    # Iterate over streamed lines
                    for line in response.iter_lines():
                        if line:
                            try:
                                data_json = json.loads(line.decode("utf-8"))
                                # Ollama's streaming JSON contains 'response' key
                                if "response" in data_json:
                                    full_answer += data_json["response"]
                                    # Update Streamlit in real time
                                    answer_placeholder.markdown(f"**Answer:** {full_answer}")
                            except json.JSONDecodeError:
                                # Sometimes partial JSON chunks; ignore safely
                                continue

                    st.success("✅ Done!")

                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to Ollama: {e}")

# ---- FOOTER ----
st.markdown(
    """
    <hr style="border:1px solid #eee">
    <p style="font-size:12px; color:#888; text-align:center;">
        Powered by Ollama • Built with Streamlit
    </p>
    """,
    unsafe_allow_html=True
)

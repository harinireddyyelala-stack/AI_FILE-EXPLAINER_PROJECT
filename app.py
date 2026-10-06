import ollama
import streamlit as st

st.title("🤖 AI Configuration File Explainer")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:

    st.header("⚙️ Chat Settings")

    st.subheader("📁 Upload File")

    uploaded_file = st.file_uploader(
        "Upload Configuration File",
        type=["txt", "json", "yaml", "yml", "env", "xml"]
    )

    if uploaded_file:

        try:
            st.session_state.context = (
                uploaded_file.read().decode("utf-8")
            )

            st.success("File uploaded successfully 👍")

        except:
            st.error("Invalid file ❌")


    st.subheader("🗑️ Clear Chat")

    if st.button("Clear Chat"):

        st.session_state.messages = []

        st.success("Chat Cleared ☺️")

    st.subheader("🕘 Chat History")

    if st.session_state.messages:

        for msg in st.session_state.messages:

            if msg["role"] == "user":

                st.write("❓ " + msg["content"])

    else:

        st.info("No chat history yet.")

tab1, tab2, tab3 = st.tabs([
    "❓ Question&Answer",
    "🤖 Summary",
    "💬 Keypoints"
])

with tab1:

    st.header("❓ Question & Answer")


    # Previous messages

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])


    # Ask Question

    question = st.chat_input(
        "🙋‍♀️ Ask Any Question:"
        )

if question:

    # Save user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # AI response
    with st.spinner("🧠 Thinking...."):

        response = ollama.chat(

            model="llama3.2:3b",

            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an AI Configuration File Explainer.
                    Explain the configuration file in simple language.
                    """
                },

                {
                    "role": "user",
                    "content": f"""
Configuration File:

{st.session_state.context}

Question:

{question}
"""
                }
            ]
        )

    answer = response["message"]["content"]

    # Save AI answer
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # Refresh the page
    st.rerun()

with tab2:

    st.header("🤖 Summary")

    if st.session_state.context:

        if st.button("📝 Generate Summary"):

            with st.spinner("🧠 Generating Summary..."):

                response = ollama.chat(

                    model="llama3.2:3b",

                    messages=[

                        {
                            "role": "user",
                            "content":
                            f"""
Give a simple summary of this
configuration file in 9-10 lines:

{st.session_state.context}
"""
                        }

                    ]
                )


            st.write(
                response["message"]["content"]
            )

    else:

        st.info("📁 Please upload a file first.")
with tab3:

    st.header("💬 Key Points")

    col1, col2 = st.columns([3, 5])

    with col1:

        st.markdown(
            "<p style='font-size:20px; font-weight:600; "
            "white-space:nowrap;'>⚙️ No of Key Points</p>",
            unsafe_allow_html=True
        )

        num_points = st.slider(
            "Select number of key points",
            min_value=5,
            max_value=15,
            value=10
        )

    with col2:

        st.markdown(
            "<p style='font-size:18px; font-weight:600;'>"
            "💬 Key Points</p>",
            unsafe_allow_html=True
        )

        if st.session_state.context:

            if st.button("🔍 Generate Key Points"):

                with st.spinner(
                    "🧠 Finding Key Points..."
                ):

                    response = ollama.chat(

                        model="llama3.2:3b",

                        messages=[

                            {
                                "role": "user",
                                "content":
                                f"""
Analyze the following configuration file.

Give exactly {num_points}
important key points.

Configuration File:

{st.session_state.context}

Give the key points as a numbered list.
"""
                            }

                        ]
                    )


                st.write(
                    response["message"]["content"]
                )

        else:

            st.info(
                "📁 Please upload a file first."
            )
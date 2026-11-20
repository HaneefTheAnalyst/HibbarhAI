import streamlit as st

from agent import ask_agent

# Page configuration
st.set_page_config(
    page_title="WeatherAI",
    page_icon="🌤️",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }

    .stChatMessage {
        border-radius: 12px;
    }

    h1 {
        color: #60A5FA;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:

    st.title("🌤️ HibbarhAI")

    st.write(
        "Your intelligent AI-powered weather assistant."
    )

    st.divider()

    st.subheader("Example questions")

    examples = [
        "Find the capital of Nigeria and its current weather",
        "What is the capital of Japan and its weather?",
        "Find the capital of France and its current weather",
        "What is the weather like in London?"
    ]

    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.pending_question = example

    st.divider()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# Main interface
st.title("🌤️ HibbarhAI")

st.caption(
    "Discover city capitals and current weather conditions "
    "using artificial intelligence."
)

st.divider()


# Welcome message
if not st.session_state.messages:

    with st.chat_message("assistant"):
        st.write(
            "Hello! 👋 I'm your AI weather assistant. "
            "Ask me about a country's capital and its "
            "current weather."
        )


# Display conversation history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Handle sidebar example questions
question = st.session_state.pop(
    "pending_question", None
)

# Chat input
user_input = st.chat_input(
    "Ask about a city's weather..."
)

if user_input:
    question = user_input


# Process user question
if question:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Get agent response
    with st.chat_message("assistant"):

        with st.spinner("AI agent is thinking..."):

            try:
                response = ask_agent(question)

                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:

                error_message = (
                    f"Something went wrong: {str(e)}"
                )

                st.error(error_message)

    st.rerun()
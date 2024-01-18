import openai
import streamlit as st
import time

# Set the page config as the first command
st.set_page_config(page_title="CatGPT", page_icon=":speech_balloon:")

# Streamlit UI for API Key
with st.sidebar:
    openai_api_key = st.text_input("Enter OpenAI API Keyt to start the Chat", key="openai_api_key", type="password")

assistant_id = "asst_zvX44SSUo3ebPhGqQLsdsjCq"

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.title("Welcome to the Style Companion!")

# Add an image (replace 'path_to_image' with your image path or URL)
image_path = 'clothing-logo.jpg'  # Example: 'images/clothing.jpg' or 'http://example.com/image.jpg'
st.image(image_path, caption='Fashion and Apparel')

st.markdown("""
👗 **Your Fashion Assistant**

Looking for the perfect outfit or style advice? Our Style Companion is here to help with all your fashion needs.

**Features:**
- **Trend Insights:** Get the latest on what's in style.
- **Outfit Recommendations:** Personalized suggestions to suit your taste.
- **Size and Fit Guidance:** Find your perfect fit with ease.
- **Brand Information:** Explore a variety of fashion brands.

**How It Works:**
Just type your fashion query, and get instant, AI-powered advice. Discover new styles, make informed choices, and elevate your fashion game!

**Ready to Find Your Style?**
Chat with our Style Companion and transform your wardrobe today!
""")

# Set the API key if provided
if openai_api_key:
    openai.api_key = openai_api_key
else:
    st.error("Please enter your OpenAI API key in the sidebar to start the chat.")
    st.stop()

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id

if st.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-1106-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        openai.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        run = openai.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="You are a helpful assistance for clothing apparel store, where you have to answer questions related with clothing, brands, sizes etc."
        )

        while run.status != 'completed':
            time.sleep(1)
            run = openai.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = openai.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)
else:
    st.write("Click 'Start Chat' to begin.")

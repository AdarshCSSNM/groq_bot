import streamlit as st
from groq import Groq
from groq import APIError

# Get API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]

# Streamlit UI
st.title("Chat Assistant")

# Check if API key is set
if not api_key or api_key == "your_api_key_here":
    st.error("Please set a valid API key in the code.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)


# User input
user_input = st.text_area("Type your message:", height=150)

# Button to trigger the chat
if st.button("Send"):
    if user_input:
        try:
            # Display a placeholder for streaming response
            response_container = st.empty()
            full_response = ""

            # Make the API call with streaming
            completion = client.chat.completions.create(
                model="compound-beta",
                messages=[
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_completion_tokens=4096,
                top_p=1,
                stream=True,
                stop=None,
            )

            # Stream the response
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                response_container.write(full_response)

        except APIError as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a message before sending.")
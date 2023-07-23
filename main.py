import streamlit as st
from streamlit_chat import message
from agent import get_agent

st.set_page_config(page_title="MeChat - An LLM-powered Streamlit app")

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 MeChat App')
    st.markdown('''
        ## About
        This app is an LLM-powered chatbot built used to answer any questions from google search.

        💡 Note: OpenAI API and SERP API key is required!
        ''')
    api_key = st.text_input("Paste your OpenAI API Key below and press ENTER", "", type="password")
    serp_api_key = st.text_input("Paste your SERP API Key below and press ENTER", "", type="password")


# generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm MeChat, How may I help you?"]
# past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']


def initialize_object(serp,key):
    # Put your object initialization code here
    obj = get_agent(serp, key)
    return obj


if 'obj' not in st.session_state:
    if api_key and serp_api_key:
        st.session_state['api_key'] = api_key
        st.session_state['serp_api_key'] = serp_api_key
        st.session_state['obj'] = get_agent(serp_api_key, api_key)
    else:
        st.warning("Please enter the API keys to initialize the chatbot.")
        st.stop()

# Layout of input/response containers
input_container = st.container()
response_container = st.container()


# User input
# Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


# Applying the user input box
with input_container:
    user_input = get_text()


# Response output
def generate_response(prompt, api_key, serp_key):
    print("API", api_key)
    print("SERP", serp_key)
    agent = st.session_state.obj
    chatbot_response = agent.run(prompt)
    st.session_state.obj = agent
    return chatbot_response


# Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input, api_key, serp_api_key)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

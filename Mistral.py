import streamlit as st
from streamlit_player import st_player
from PIL import Image
import base64
import requests
import json


    
@st.cache_data
def Mistral_8x7B(token,prompt, temp, top_p,seed):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/8f4118ba-60a8-4e6b-8574-e38a4067a4a3"

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "text/event-stream",
        "content-type": "application/json",
    }

    payload = {
        "messages": [
            {
                "content": f"{prompt}",
                "role": "user"
            }
        ],
        "temperature": temp,
        "top_p": top_p,
        "max_tokens": 1024,
        "stream": True,
        "seed" : seed
    }

    try:
        response = requests.post(invoke_url, headers=headers, json=payload, stream=True)

        # List to store content values
        content_list = []

        # Get the total content length
        total_length = int(response.headers.get("content-length", 0))

        # Initialize progress bar
        progress_bar = st.progress(0)

        # Initialize progress counter
        progress_counter = 0

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                if decoded_line.startswith("data:"):
                    try:
                        json_data = json.loads(decoded_line[5:])
                        content = json_data["choices"][0]["delta"]["content"]
                        content_list.append(content)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")

                    # # Update progress
                    # if total_length > 0:
                    #     progress_counter += len(decoded_line)
                    #     progress_bar.progress(min(progress_counter / total_length, 1.0))

                    #     # Add a small delay to allow the progress bar to update smoothly
                    #     time.sleep(0.01)

    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None

    # Now content_list contains all the 'content' values from the JSON data
    response_text = "".join(content_list)
    return response_text



def Display_Mistral_7B(token):
    st.markdown("<h1 style=text-align:center;'>Mixtral 8x7B</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("Parameters Tuning (7B)")
        st.session_state.temperature_val = st.slider("Select Temperature", key="slider1", min_value=0.1, max_value=1.0, value=0.25, step=0.1, help="Less Temp = More precise\n,High temperature = Creative")
        if st.session_state.temperature_val > 0.9:
            st.session_state.temperature_val = 1.0
        st.write('Temperature:', st.session_state.temperature_val)

        st.session_state.top_p_val = st.slider("Select Top_P", key="slider2", min_value=0.1, max_value=1.0, value=0.1, step=0.1, help="nucleus sampling probability threshold")
        if st.session_state.top_p_val > 0.9:
            st.session_state.top_p_val = 1.0
        st.write('Top_P:', st.session_state.top_p_val)

        st.session_state.val2 = st.slider("Select Seed", key="slider3", min_value=1, max_value=1000, value=42, step=1)
        st.write('Seed:', st.session_state.val2)


    if "messages_Mistral" not in st.session_state:
        st.session_state["messages_Mistral"] = [{"role": "assistant", "content": "Ask me anything you want I can answer you !"}]

    for msg in st.session_state.messages_Mistral:
        with st.chat_message(msg.get("role")):
            st.write(msg.get("content"))
    
    
    prompt = st.chat_input("Ask me anything:", max_chars=8000)
    
    if prompt:
        st.session_state.messages_Mistral.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        result = Mistral_8x7B(token,prompt, st.session_state.temperature_val, st.session_state.top_p_val,st.session_state.val2)

        st.session_state.messages_Mistral.append({"role": "assistant", "content": result})
        with st.chat_message("assistant"):
            st.write(result)

import streamlit as st
from streamlit_player import st_player
from dotenv import load_dotenv
from PIL import Image
import os
import base64
import time
import requests
import json

load_dotenv()
NVIDIA_API_KEY = api_key = os.getenv("NVIDIA_API_KEY")

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.read()

        # Encode the bytes data to base64
        encoded = base64.b64encode(bytes_data).decode("utf-8")
        return encoded
    else:
        raise FileNotFoundError("No file uploaded")
    
@st.cache_data
def Kosmos2_text(prompt, temp, top_p):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/0bcd1a8c-451f-4b12-b7f0-64b4781190d1"

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
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
        "max_tokens": 512,
        "stream": True
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

                    # Update progress
                    if total_length > 0:
                        progress_counter += len(decoded_line)
                        progress_bar.progress(min(progress_counter / total_length, 1.0))

                        # Add a small delay to allow the progress bar to update smoothly
                        time.sleep(0.01)

    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None

    # Now content_list contains all the 'content' values from the JSON data
    response_text = "".join(content_list)
    return response_text

@st.cache_data
def Kosmos2_Vision(prompt, temp, top_p, image):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/8bf70738-59b9-4e5f-bc87-7ab4203be7a0"

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "accept": "text/event-stream",
        "content-type": "application/json",
    }

    payload = {
        "messages": [
            {
                "content": f"{prompt} <img src=\"data:image/png;base64,{image}\" />",
                "role": "user"
            },
            {
                "labels": {
                    "creativity": 6,
                    "helpfulness": 6,
                    "humor": 0,
                    "quality": 6
                },
                "role": "assistant"
            }
        ],
        "temperature": temp,
        "top_p": top_p,
        "max_tokens": 512,
        "stream": True
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
                        choices = json_data.get("choices", [])
                        for choice in choices:
                            delta = choice.get("delta", {})
                            content = delta.get("content", "")
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




def Display_Kosmos2():
    st.markdown("<h1 style=text-align:center;'>Kosmos2 Multimodel</h1>", unsafe_allow_html=True)
    is_image_uploaded = False
    uploaded_image = st.sidebar.file_uploader("Upload Images", [".jpeg", ".png", ".jpg"], help="Choose file for Kosmos2 Vision")

    if uploaded_image is not None:
        is_image_uploaded = True
        st.sidebar.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

    with st.sidebar:
        st.session_state.temperature_val = st.slider("Select Temperature", key="slider1", min_value=0.1, max_value=1.0, value=0.25, step=0.1, help="Less Temp = More precise\n,High temperature = Creative")
        if st.session_state.temperature_val > 0.9:
            st.session_state.temperature_val = 1.0
        st.write('Temperature:', st.session_state.temperature_val)

        st.session_state.top_p_val = st.slider("Select Top_p", key="slider2", min_value=0.1, max_value=1.0, value=0.25, step=0.1, help="neucleus samplinf threshold limit")
        if st.session_state.top_p_val > 0.9:
            st.session_state.top_p_val = 1.0
        st.write('Top_p:', st.session_state.top_p_val)

        
        st.subheader("Usage Manual")
        st.markdown("""<ul>
                        <li>Default model Kosmos2 - Text</l1>
                        <li>Image input changes model to Kosmos2 vision</l1>
                        <li>Once an image is selected then rest of the Chat goes according to That image, So if you wanna revert to text generation delete the image in sidebar yourself</l1>
                        <li>When you image contain any Harsh,nudity,violence or other content might give you error. So dont try it </l1>
                        <li>There is only 8000 char input allowed in a single prompt so write wisely</li>
                        <li>when your chat history is long it might get Stuck or takes more time to render page (will fix in future), If you encounter this start another session by refreshing page</li>
                        </ul>
                    
                    """,unsafe_allow_html=True)
        st.success("You are Good to go !")
            

    if "messages_kosmos2" not in st.session_state:
        st.session_state["messages_kosmos2"] = []

    for msg in st.session_state.messages_kosmos2:
        with st.chat_message(msg.get("role")):
            if msg.get("is_image_uploaded"):
                st.image(msg.get("image"),use_column_width=True)
                st.write(msg.get("content"))
            else:
                st.write(msg.get("content"))

    prompt = st.chat_input("Ask me anything or give me any picture", max_chars=8000)

    if prompt:
        if is_image_uploaded:
            st.session_state.messages_kosmos2.append({"role": "user", "content": prompt, "image": uploaded_image, "is_image_uploaded": True})
            is_image_uploaded = False  # Reset the flag after storing the image in history
        else:
            st.session_state.messages_kosmos2.append({"role": "user", "content": prompt, "is_image_uploaded": False})

        if st.session_state.messages_kosmos2[-1]["is_image_uploaded"]:
            with st.chat_message("user"):
                st.image(st.session_state.messages_kosmos2[-1]["image"], caption='Uploaded Image', use_column_width=True)
                st.write(prompt)

            pre_img = input_image_setup(uploaded_image)
            result = Kosmos2_Vision(prompt=prompt,image = pre_img,temp=st.session_state.temperature_val,top_p=st.session_state.top_p_val)
            uploaded_image = None

        else:
            with st.chat_message("user"):
                st.write(prompt)

            result = Kosmos2_text(prompt,st.session_state.temperature_val,st.session_state.top_p_val)

        st.session_state.messages_kosmos2.append({"role": "assistant", "content": result})

        with st.chat_message("assistant"):
            st.write(result)


# Run the app
if __name__ == "__main__":
    Display_Kosmos2()
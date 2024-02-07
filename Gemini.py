import streamlit as st
from streamlit_player import st_player
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()
GEMINI_API_KEY = api_key = os.getenv("GEMINI_API_KEY")


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

@st.cache_data
def Gemini(token,prompt):
    genai.configure(api_key =token)
    model = genai.GenerativeModel('gemini-pro') 
    response = model.generate_content(prompt)
    return response.text

    
    # return f"gemini pro {prompt}" ## complete function 1/2/2024
@st.cache_data
def Gemini_vision(token,prompt,image):
    st.markdown("<p style='text-align:center;'>Image will be used from here, Delete image when you are done ✅</p>",unsafe_allow_html=True)
    genai.configure(api_key =token)
    model = genai.GenerativeModel('gemini-pro-vision')
    safe = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
    response = model.generate_content([image[0],prompt],safety_settings=safe) 
    return response.text

def Display_Gemini(token):
    st.markdown("<h1 style=text-align:center;'>Google Gemini-pro</h1>", unsafe_allow_html=True)
    there_img = False
    uploaded_image = st.sidebar.file_uploader("Upload Images", [".jpeg", ".png", ".jpg"], help="Choose file for Gemini Vision Pro")

    if uploaded_image is not None:
        there_img = True
        st.sidebar.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

    with st.sidebar:
        st.session_state.val = st.slider("Select Temperature", key="slider1", min_value=0.1, max_value=1.0, value=0.25, step=0.1, help="Less Temp = More precise\n,High temperature = Creative")
        if st.session_state.val > 0.9:
            st.session_state.val = 1.0
        st.write('Temperature:', st.session_state.val)

        st.title("what is Gemini Pro ?")
        st_player("https://youtu.be/UIZAiXYceBI?si=a3DhLB2PKekI9FmD")
        
        st.subheader("Usage Manual")
        st.markdown("""<ul>
                        <li>Default model gemini pro - Text</l1>
                        <li>Image input changes model to Gemini-pro-vision</l1>
                        <li>Once an image is selected then rest of the Chat goes according to That image, So if you wanna revert to text generation delete the image in sidebar yourself</l1>
                        <li>Gemini API accepts 60RPM so if you encounter any error try after a min</l1>
                        <li>When you image contain any Harsh,nudity,violence or other content might give you error. So dont try it </l1>
                        <li>There is only 8000 char input allowed in a single prompt so write wisely</li>
                        <li>when your chat history is long it might get Stuck or takes more time to render page (will fix in future), If you encounter this start another session by refreshing page</li>
                        </ul>
                    
                    """,unsafe_allow_html=True)
        st.success("You are Good to go !")
        # st.markdown("<h3>Repository link :- <a href='https://github.com'>Multimodel Chatbot</a></h3>",unsafe_allow_html=True)
        # st.info("You can contribute to this repo !")
            


    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Ask me anything you want or give me image 📷 to explain"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg.get("role")):
            if msg.get("there_img"):
                st.image(msg.get("image"),use_column_width=True)
                st.write(msg.get("content"))
            else:
                st.write(msg.get("content"))

    prompt = st.chat_input("Ask me anything or give me any picture", max_chars=8000)

    if prompt:
        if there_img:
            st.session_state.messages.append({"role": "user", "content": prompt, "image": uploaded_image, "there_img": True})
            there_img = False  # Reset the flag after storing the image in history
        else:
            st.session_state.messages.append({"role": "user", "content": prompt, "there_img": False})

        if st.session_state.messages[-1]["there_img"]:
            with st.chat_message("user"):
                st.image(st.session_state.messages[-1]["image"], caption='Uploaded Image', use_column_width=True)
                st.write(prompt)
            pre_img = input_image_setup(uploaded_image)
            result = Gemini_vision(token=token,prompt=prompt,image = pre_img)
            uploaded_image = None

        else:
            with st.chat_message("user"):
                st.write(prompt)

            result = Gemini(token,prompt)

        st.session_state.messages.append({"role": "assistant", "content": result})

        with st.chat_message("assistant"):
            st.write(result)






import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
import os

from Gemini import Display_Gemini
from Neva import Display_NeVA_22B
# from Models.kosmos2 import Display_Kosmos2
from Palm2 import Display_Palm2
from Mistral import Display_Mistral_7B
from Llama2 import Display_Llama2

load_dotenv()
GEMINI_API_KEY = api_key = os.getenv("GEMINI_API_KEY")
NVIDIA_API_KEY = api_key = os.getenv("NVIDIA_API_KEY")

st.set_page_config(
        page_title="Generative LLMs",
)

# Define the sidebar
with st.sidebar:
    # Create the options menu
    selected = option_menu(menu_title="Generative AI",
                           options=["Gemini Pro", "NeVA-22B","Mistral 8x7B","Llama-2 70B","Palm-2"],
                           icons=["box", "box", "box","box","box"],
                           menu_icon="boxes",
                           default_index=0
                           )
    
if selected == "Gemini Pro":
    Display_Gemini(GEMINI_API_KEY)
elif selected == "NeVA-22B":
    Display_NeVA_22B(NVIDIA_API_KEY)
# elif selected == "Kosmos2":
#     Display_Kosmos2()
elif selected == "Palm-2":
    Display_Palm2(GEMINI_API_KEY)
elif selected == "Mistral 8x7B":
    Display_Mistral_7B(NVIDIA_API_KEY)
elif selected == "Llama-2 70B":
    Display_Llama2(NVIDIA_API_KEY)
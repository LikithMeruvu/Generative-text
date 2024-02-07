import streamlit as st
import google.generativeai as palm

@st.cache_data
def palm_2(token,prompt,temp,top_p):
    palm.configure(api_key=f"{token}")
    models = [m for m in palm.list_models() if "generateText" in m.supported_generation_methods]
    model = models[0].name

    completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=temp,
    top_p=top_p,
    # The maximum length of the response
    max_output_tokens=4096,
)

    return completion.result


def Display_Palm2(token):
    st.markdown("<h1 style=text-align:center;'>Google Palm-2</h1>", unsafe_allow_html=True)
    
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


    if "messages_palm" not in st.session_state:
        st.session_state["messages_palm"] = [{"role": "assistant", "content": "Ask me anything you want I can answer you !"}]

    for msg in st.session_state.messages_palm:
        with st.chat_message(msg.get("role")):
            st.write(msg.get("content"))
    
    
    prompt = st.chat_input("Ask me anything:", max_chars=8000)
    
    if prompt:
        st.session_state.messages_palm.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        result = palm_2(token,prompt, st.session_state.temperature_val, st.session_state.top_p_val)

        st.session_state.messages_palm.append({"role": "assistant", "content": result})
        with st.chat_message("assistant"):
            st.write(result)

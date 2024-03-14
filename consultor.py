import streamlit as st
from generator import generar_respuesta

st.set_page_config(page_title="Datec Wizard", page_icon="images/ISOTIPO.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# Crea tres columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.image('images/Logo_Sigi.png')

with col3:
    st.image('images/LOGO_DATEC.png')
    
st.title("Pregúntame algo de Datec")
#st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "En qué te puedo ayudar?"}
    ]

if prompt := st.chat_input("Escribe aquí"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Analizando..."):
            response = generar_respuesta(message["content"])
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history

# Crea tres columnas
col1, col2, col3, col4 = st.columns(4)
with col4:
    # Imagen
    st.image('images\Logo_D4G.png', use_column_width=True)
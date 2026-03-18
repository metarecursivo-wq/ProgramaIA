from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st 
from dotenv import load_dotenv

load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Programa IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Programa IA")
st.markdown("""
    Este es un programa IA creado por el usuario de github @metarecursivo-wq, cuyo objetivo es ayudar a los usuarios a resolver problemas de programación.
    El objetivo del programa es ayudar a los usuarios a resolver problemas de programación de manera eficiente y rápida.
    """)

with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"])
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

plantilla = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""
    Eres un experto en programación y desarrollo de software.
    Tu objetivo es ayudar a los usuarios a resolver problemas de programación de manera eficiente y rápida.
    Historial de conversación:
    {historial}

    Responde a la pregunta del usuario: {mensaje}
    """
)

if st.button("Otro problema"):
    st.session_state.mensajes = []
    st.rerun()

problema = st.chat_input("Introduce el problema de programación a resolver")

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if problema:
    st.session_state.mensajes.append({"role": "user", "content": problema})
    with st.chat_message("user"):
        st.markdown(problema)

    historial = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.mensajes[:-1]
    )

    prompt = plantilla.format(mensaje=problema, historial=historial)

    with st.chat_message("assistant"):
        with st.spinner("Resolviendo..."):
            respuesta = chat_model.invoke([HumanMessage(content=prompt)])
            st.markdown(respuesta.content)

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta.content})

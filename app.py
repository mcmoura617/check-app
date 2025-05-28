import streamlit as st

st.title("🎉 Meu Primeiro App com Streamlit")
st.write("Olá! Este é o início do seu app!")

nome = st.text_input("Qual é o seu nome?")
if nome:
    st.success(f"Bem-vindo(a), {nome}!")
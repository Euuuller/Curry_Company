import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'Home',
    page_icon = '🎲'  
)


image_path = 'Logo.png' 
image = Image.open(image_path)  
st.sidebar.image(image, width=300)

st.sidebar.markdown ( '# Curry Company' )
st.sidebar.markdown ( '## Fastest Delivery in Town' )
st.sidebar.markdown ( """___""") 

st.write ('# Curry Company Growth Dashboard')

st.markdown("**Growth Dashborad foi contruído para acompanhar as métricas de crecimento dos Entregadores e Restaurantes.**")

st.markdown(":orange[**Como utilizar esse Growth Dashboard?**]")
st.markdown ( """___""") 

st.markdown(":blue[**Visão Empresa**]: 🔰 ")
st.markdown('-- ***Visão Gerencial: Métricas gerais de comportamento.***')
st.markdown('-- ***Visão Tática: Indicadores semanais de crescimento.***')
st.markdown('-- ***Visão Geográfica: Insights de geolocalização.***')
st.markdown ( """___""") 

st.markdown(":blue[**Visão Entregador**]: 🔰 ")
st.markdown('-- ***Acompanhamento dos indicadores semanais de crescimento***')
st.markdown ( """___""") 

st.markdown(":blue[**Visão Restaurantes**]: 🔰 ")
st.markdown('-- ***Visão Gerencial: Métricas gerais de comportamento.***')
st.markdown('-- ***Visão Tática: Indicadores semanais de crescimento.***')
st.markdown('-- ***Visão Geográfica: Insights de geolocalização.***')
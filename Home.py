import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home 🏠", 
    page_icon=":🦈:", 
    layout="wide")

#image_path = "Logo.png"
image = Image.open('Logo.png')
st.sidebar.image(image, width=300)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""___""")
st.sidebar.markdown("## Selecione uma data limite")

st.write("Curry Company Growth Dashboard")

st.markdown(
    """
    Growrh Dashboard foi construido para acompanhar o crescimento dos Entregadores e Restaurantes.
    ### COmo utilizar esse Growth Dashboard?
    - A barra lateral esquerda contém os filtros para selecionar os dados que deseja visualizar.
        - Visão da Empresa:
            - VIsão Gerencial: Métricas Gerais de Comportamento.
            - Visão Tática: Indicadores semanais de crescimento.
            - Visão Geográfica: Indicadores de crescimento por região.
        - Visão Entregadores:
            - Acompanhamento dos indicadores semanais de crescimento.
        - Visão Restaurantes:
            - Indicadores semanais de crescimento dos restaurantes.
        
        ### Ask for Help
        - Time de Data Science da Comunidade DS
        - @euuuller
    """)
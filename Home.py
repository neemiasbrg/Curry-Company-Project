import streamlit as st
from PIL import Image
import base64

# Configuração da página com título, ícone e layout
st.set_page_config(
    page_title='Home',
    page_icon='map.png',
    layout='wide'
)

# Carrega e exibe a imagem do logo
image_path = 'logo.png'
image = Image.open(image_path)
st.image(image, width=120)  

# Barra lateral e conteúdo principal
st.sidebar.markdown('### Curry Company')
st.sidebar.markdown('# Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas Gerais de Comportamento
        - Visão Tática: Indicadores Semanais de Crescimento
        - Visão Geográfica: Insights de Geolocalização
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask for help
    - Time de Data Science no Discord
        - @comunidadeds
    """
)

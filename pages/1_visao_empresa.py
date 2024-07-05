#===================================================
#Importação das bibliotecas e funções
#===================================================

import pandas as pd
import re
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image
import folium
import datetime

st.set_page_config( page_title='Visão Empresa' , page_icon=r"C:\Users\Neemias G Braga\Music\node_modules\serve-index\public\icons\map.png" , layout='wide' )

#===================================================
#Funções
#===================================================
def country_maps (df1):
    columns = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    data_plot = (df_filtered[columns].groupby(['City', 'Road_traffic_density'])
                                     .median()
                                     .reset_index())
    
    # Criar o mapa usando folium
    map_ = folium.Map(location=[data_plot['Delivery_location_latitude'].mean(), data_plot['Delivery_location_longitude'].mean()], zoom_start=11)

    # Adicionar marcadores ao mapa
    for index, location_info in data_plot.iterrows():
        folium.Marker(
            location=[location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']],
            popup=f"{location_info['City']} - Traffic Density: {location_info['Road_traffic_density']}"
        ).add_to(map_)

    # Renderizar o mapa usando folium_static
    folium_static(map_, width=1024, height=600)

    return None

def order_share_by_week(df1):
        df_aux1 = df_filtered.groupby('week_of_year').size().reset_index(name='total_orders')
        df_aux2 = df_filtered.groupby('week_of_year')['Delivery_person_ID'].nunique().reset_index(name='unique_delivery_persons')
        df_aux = pd.merge(df_aux1, df_aux2, on='week_of_year')
        df_aux['avg_orders_per_delivery_person'] = df_aux['total_orders'] / df_aux['unique_delivery_persons']
        fig5 = px.line(df_aux, x='week_of_year', y='avg_orders_per_delivery_person', title='Média de pedidos por entregador por semana')
        
        return fig5

def order_by_week (df1):
        df_filtered['week_of_year'] = df_filtered['Order_Date'].dt.strftime("%U")
        df_aux = df_filtered.groupby('week_of_year').size().reset_index(name='qtde_entregas')
        fig4 = px.bar(df_aux, x='week_of_year', y='qtde_entregas', title='Quantidade de pedidos por semana')
        
        return fig4

def traffic_order_city (df1):
    df_aux = df_filtered.groupby(['City', 'Road_traffic_density']).size().reset_index(name='count')
    fig3 = px.bar(df_aux, x='City', y='count', color='Road_traffic_density', title='Pedidospor cidade e densidade de tráfego', barmode='group')
                    

    return fig3

def traffic_order_share(df1):
                    
    df_aux = df_filtered.groupby('Road_traffic_density').size().reset_index(name='count')
    fig2 = px.pie(df_aux, values='count', names='Road_traffic_density', title='Distribuição dos pedidos por tipo de tráfego')
                    
    return fig2


def order_by_metric (df1):
            
    df_aux = df_filtered.groupby('Order_Date').size().reset_index(name='qtde_entregas')
    fig1 = px.bar(df_aux, x='Order_Date', y='qtde_entregas', title='Quantidade de pedidos por dia')            
        
    return fig1
        

def clean_code (df1):
    """Esta função é responsável pela limpeza do dataframe

       Tipos de Limpezas:
    
       1. Remoção dos dados NaN
       2. Mudança do tipo da coluna de dados
       3. Remoção dos espaços das variáveis de texto
       4. Fotmatação da coluna de datas
       5. Limpeza da coluna tempo (remoção do texto da variáve numérica)

       Imput: Dataframe
       Output Dataframe
    
    """
    # Remover spaco da string
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

    # Excluir as linhas com a idade dos entregadores vazia
    # ( Conceitos de seleção condicional )
    # Use pd.isna() to check for NaN values more reliably
    linhas_vazias = ~pd.isna(df1['Delivery_person_Age'])
    df1 = df1.loc[linhas_vazias, :]

    # Conversao de texto/categoria/string para numeros inteiros
    # Use pd.to_numeric() with errors='coerce' to handle non-convertible values
    df1['Delivery_person_Age'] = pd.to_numeric(df1['Delivery_person_Age'], errors='coerce').astype('Int64') # Use Int64 to allow for nullable integers

    # Conversao de texto/categoria/strings para numeros decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # Conversao de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )
    # Removendo espaços vazios
    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )
    linhas_vazias = df1['City'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]
    linhas_vazias = df1['Weatherconditions'] != 'conditions NaN'
    df1 = df1.loc[linhas_vazias, :]
    linhas_vazias = df1['Road_traffic_density'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]
    linhas_vazias = df1['Festival'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]

    # Comando para remover o texto de números
    df1 = df1.reset_index( drop=True )
    # Apply re.findall() to each element in the Series
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: re.findall(r'\d+', x)[0] if re.findall(r'\d+', x) else None)
    # Convert the extracted numbers to integers
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype('Int64')

    return df1

#===================================================
#Carregar os dados
#===================================================

df = pd.read_csv('train.csv')

# Criar uma cópia do DataFrame original
df1 = df.copy()

#===================================================
#Limpeza dos dados
#===================================================

df1 = clean_code(df)

#===================================================
#Barra Lateral
#===================================================
st.header('Marketplace - Visão Empresa')

# Carregar e mostrar a imagem do logo
image_path = 'logo.png'
image = Image.open(image_path)
st.image(image, width=120)

st.sidebar.markdown('### Cury Company')
st.sidebar.markdown('# Fastest Delivery in Town')
st.sidebar.markdown( """---""" )

min_date = df1['Order_Date'].min()
max_date = df1['Order_Date'].max()

# Convert datetime to days since epoch
min_days = int((min_date - pd.Timestamp("1970-01-01")).days)
max_days = int((max_date - pd.Timestamp("1970-01-01")).days)

# Slider na barra lateral para seleção de data
data_slider_days = st.sidebar.slider(
    'Selecione uma data',
    min_value=min_days,
    max_value=max_days,
    value=max_days
)

# Convert days back to datetime
data_slider = pd.Timestamp("1970-01-01") + pd.Timedelta(days=data_slider_days)

st.header(data_slider.strftime('%d-%m-%Y'))
st.sidebar.markdown( """---""" )

traffic_options = st.sidebar.multiselect(
    'Quais as condições de trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default='Low'
)

st.sidebar.markdown( """---""" )

conditions_options = st.sidebar.multiselect(
    'Quais as condições climáticas?',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default='conditions Stormy'
)

st.sidebar.markdown( """---""" )


st.sidebar.markdown('### Powered by Comunidade DS')

# Filtrar dados com base na seleção do slider
df_filtered = df1[(df1['Order_Date'] < data_slider) &
                  (df1['Road_traffic_density'].isin(traffic_options)) &
                  (df1['Weatherconditions'].isin(conditions_options))]

#===================================================
#Layout no Streamlit
#===================================================
# Abas no Streamlit
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica']) 

with tab1:
    with st.container():
        #Order Metric
        fig1 = order_by_metric(df1)
        st.header('Order by Date')
        st.plotly_chart(fig1, use_container_width=True)
        
        with st.container():   
            col1, col2 = st.columns( 2 )

            with col1:
                st.header('Traffic Order Share')
                fig2 = traffic_order_share(df1)
                st.plotly_chart(fig2, use_container_width=True)
                
            with col2:
                st.header('Traffic Order City')
                fig3 = traffic_order_city(df1)
                st.plotly_chart(fig3, use_container_width=True)
                
with tab2:
    with st.container():
        st.header('Order by Week')
        fig4 = order_by_week(df1)
        st.plotly_chart(fig4, use_container_width=True)

    with st.container():
        st.header(' Order Share by Week')
        fig5 = order_share_by_week(df1)
        st.plotly_chart(fig5, use_container_width=True)

with tab3:
    st.header('Country Maps')
    country_maps(df1)

    
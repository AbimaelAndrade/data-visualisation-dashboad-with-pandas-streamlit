import streamlit as st
import pandas as pd
import plotly.express as px

# Definir os dados diretamente
data = pd.read_csv('data/houses_to_rent_v2.csv')  # Coloque o caminho do seu arquivo

# Função para filtrar os dados
def filter_data(data, 
                selected_cities=['São Paulo', 'Rio de Janeiro'], 
                selected_rooms=(2, 3), 
                selected_bathroom=(1, 2),
                selected_animal=['not acept'], 
                selected_price_range=(500, 5000)):
    filtered_data = data[
        (data['city'].isin(selected_cities)) &
        (data['rooms'].between(selected_rooms[0], selected_rooms[1])) &
        (data['bathroom'].between(selected_bathroom[0], selected_bathroom[1])) &
        (data['animal'].isin(selected_animal)) &
        (data['rent amount (R$)'].between(selected_price_range[0], selected_price_range[1]))
    ]

    return filtered_data

# Função para gerar gráfico de dispersão (Área vs. Aluguel)
def plot_scatter_area_rent(data):
    fig = px.scatter(
        data, 
        x='area', 
        y='rent amount (R$)', 
        color='city', 
        title='Relação entre Área e Valor do Aluguel',
        labels={'area': 'Área (m²)', 'rent amount (R$)': 'Valor do Aluguel (R$)'}
    )
    st.plotly_chart(fig)

# Função para gerar histograma de valores de aluguel
def plot_histogram_rent(data):
    fig = px.histogram(
        data, 
        x='rent amount (R$)', 
        nbins=20, 
        color='city', 
        title='Distribuição dos Valores de Aluguel',
        labels={'rent amount (R$)': 'Valor do Aluguel (R$)'}
    )
    st.plotly_chart(fig)

# Título do dashboard
st.title("Dashboard de Comparação de Preços de Aluguel")

# Divisão em abas para as análises
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Comparação de Preços por Filtros", 
    "Distribuição de Preços", 
    "Análise de Preços Totais", 
    "Gráfico de Dispersão", 
    "Histograma"
])

# Aba 1: Comparação de preços por filtros
with tab1:
    st.subheader("Filtros para Comparação de Preços")
    # setar valor
    filtered_data = filter_data(data)

    # Formulário para seleção de filtros
    with st.form(key='filters_form'):
        selected_cities = st.multiselect('Selecione as cidades', data['city'].unique(), default=data['city'].unique())
        selected_rooms = st.slider('Número de Quartos', int(data['rooms'].min()), int(data['rooms'].max()), (2, 3))
        selected_bathroom = st.slider('Número de Banheiros', int(data['bathroom'].min()), int(data['bathroom'].max()), (1, 2))
        selected_animal = st.multiselect('Aceita Animais', data['animal'].unique(), default="not acept")
        selected_price_range = st.slider('Faixa de Preço de Aluguel (R$)', 
                                         int(data['rent amount (R$)'].min()), 
                                         int(data['rent amount (R$)'].max()), 
                                         (500, 5000), step=100, format='%d')

        submit_button = st.form_submit_button(label='Aplicar Filtros')

    if submit_button:
        filtered_data = filter_data(data, selected_cities, selected_rooms, selected_bathroom, selected_animal, selected_price_range)
        
        st.subheader("Dados Filtrados")
        st.dataframe(filtered_data)

# Aba 2: Distribuição de Preços
with tab2:
    st.subheader("Distribuição de Preços de Aluguel entre Cidades")
    city_avg_rent = data.groupby('city')['rent amount (R$)'].mean().sort_values()
    fig = px.bar(
        city_avg_rent, 
        x=city_avg_rent.values, 
        y=city_avg_rent.index, 
        orientation='h', 
        color=city_avg_rent.values, 
        color_continuous_scale='Blues', 
        title='Distribuição de Preços Médios de Aluguel',
        labels={'x': 'Preço Médio de Aluguel (R$)', 'city': 'Cidade'})
    
    fig.update_layout(coloraxis_showscale=False, title_font_color="#cfcfcf")
    st.plotly_chart(fig)

# Aba 3: Análise de Preços Totais
with tab3:
    st.subheader("Análise de Preços Totais (incluindo taxas)")
    city_avg_total = data.groupby('city')['total (R$)'].mean().sort_values()
    fig = px.bar(city_avg_total, 
    x=city_avg_total.values, 
    y=city_avg_total.index, 
    orientation='h', 
    color=city_avg_total.values, 
    color_continuous_scale='Blues', 
    labels={'x': 'Preço Médio de Aluguel (R$)', 'city': 'Cidade'})
    
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig)

# Aba 4: Gráfico de Dispersão
with tab4:
    st.subheader("Gráfico de Dispersão: Área vs. Valor do Aluguel")
    plot_scatter_area_rent(filtered_data)

# Aba 5: Histograma
with tab5:
    st.subheader("Histograma: Distribuição dos Valores de Aluguel")
    plot_histogram_rent(filtered_data)
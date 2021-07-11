#region IMPORTING PACKAGES
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")
from PIL import Image
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
import plotly.io as pio
import app_functions as app
pd.options.display.float_format = "{:,.2f}".format
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
import pickle
#endregion importing packages

#region SIDEBAR
df_territory = app.load_df_territory()
uf = st.sidebar.selectbox(label='UF', options=df_territory.uf.unique())
options = app.filter_municipalities_by_uf(uf=uf, df=df_territory)
municipio = st.sidebar.selectbox(label='Município', options=options)
cod_municipio = app.get_cod_municipio(df=df_territory, uf=uf, municipio=municipio)
municipio_name = app.load_mun_name(cod_municipio=cod_municipio)
#endregion SIDEBAR

#region HEADER
st.markdown(f"<h1 style='text-align: right; color: black;'>PopApp</h1>", unsafe_allow_html=True)
st.markdown(f'## {municipio}')
#endregion HEADER


#region FIRST ROW
df_urbrur_growth = app.load_urbrur_data()
fig_urbrur_growth, ano_min, ano_max = app.plot_urbrur_growth(df=df_urbrur_growth, cod_municipio=cod_municipio)


col_a, col_b = st.beta_columns((1, 6))
urb_indicator = app.get_urbanization_index(df=df_urbrur_growth, cod_municipio=cod_municipio)
if 2000 not in df_urbrur_growth[df_urbrur_growth['Código'] == cod_municipio].Ano.unique():
    urb_index = app.plot_urbanization_index(urb_indicator=urb_indicator, height=184, font_size=50, color=px.colors.qualitative.Plotly[0])
    col_a.markdown(f"<p style='text-align: left; color: black; font-size:18px'><b>Taxa de Urbanização<b></p>", unsafe_allow_html=True)
    col_a.plotly_chart(urb_index, use_container_width=True)
else:
    col_a.markdown(f"<p style='text-align: left; color: black; font-size:18px; line-height: 2'><b>Taxa de Urbanização<b></p>", unsafe_allow_html=True)
    urb_index = app.plot_urbanization_index(urb_indicator=urb_indicator, height=53, font_size=30, color=px.colors.qualitative.Plotly[0])
    col_a.plotly_chart(urb_index, use_container_width=True)
    pop_growth_rate = app.get_pop_growth_rate(df=df_urbrur_growth, cod_municipio=cod_municipio)
    indicator_pop_rate = app.plot_urbanization_index(urb_indicator=pop_growth_rate, height=53, font_size=30, color=px.colors.qualitative.Plotly[0])
    col_a.markdown(f"<p style='text-align: left; color: black; font-size:18px; margin-top: 10px; margin-bottom: 10px'><b>Taxa de Crescimento<b></p>", unsafe_allow_html=True)
    col_a.plotly_chart(indicator_pop_rate, use_container_width=True)

if uf == 'PR':
    df_projection = app.load_projection_data()
    subplots = app.subplot_pop_growth(df_urbrur=df_urbrur_growth, df_projection=df_projection, cod_municipio=cod_municipio)
    col_b.plotly_chart(subplots, use_container_width=True)
else:
    col_b.plotly_chart(fig_urbrur_growth, use_container_width=True)
#endregion FIRST ROW


#region SECOND ROW
df_estrutura_etaria_f, df_estrutura_etaria_m = app.load_age_groups()
fig_age_groups, year = app.plot_pop_pyramid(df_estrutura_etaria_f=df_estrutura_etaria_f, df_estrutura_etaria_m=df_estrutura_etaria_m, cod_municipio=cod_municipio, year=2010)

c1, c2 = st.beta_columns(2)
c1.plotly_chart(fig_age_groups, use_container_width=True)

gdf1 = app.load_sector_geodataframe(uf=uf, cod_municipio=cod_municipio)
fig_map1 = app.plot_density_map(gdf=gdf1)
c2.plotly_chart(fig_map1, use_container_width=True)
#endregion SECOND ROW


#region COMMUTING DATA
import streamlit.components.v1 as components
df = pd.read_csv('data/pop/arranjos populacionais/tab01.csv', sep=';', decimal=',', thousands='.')
if cod_municipio in df['Código do município'].unique():
    fig_arranjo = app.plot_arranjo(cod_municipio=cod_municipio)
    st.plotly_chart(fig_arranjo, use_container_width=True)


    st.markdown(f"<p style='text-align: left; color: black; font-size:18px'><b>Mobilidade Pendular<b></p>", unsafe_allow_html=True)
    kepler_map = app.plot_commuting(cod_municipio=cod_municipio)
    htm = kepler_map._repr_html_()
    components.html(htm, height=400)
#endregion COMMUTING DATA
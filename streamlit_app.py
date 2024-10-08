# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Smoothie de Raquel:cup_with_straw:")
st.write(
    """Prueba primera!
    **Smoothie de Fresa,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

name_on_order = st.text_input("Nombre del Smoothie:")
st.write("El nombre de tu smoothie será:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table ("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data = my_dataframe, use_container_width=True)

ingredients_list = st.multiselect (
    'Choose up to 5 ingredients:'
    , my_dataframe
)

if ingredients_list:
   
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_with=True)
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
        values ('""" + ingredients_string + """','""" + name_on_order+ """')"""
     
    st.write (my_insert_stmt)

    time_to_insert = st.button ('Submit Order')
        
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
    st.stop()

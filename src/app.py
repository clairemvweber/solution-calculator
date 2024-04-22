import streamlit as st
import pandas as pd

from calculations import *
from util import *

st.set_page_config(layout='wide')

# Selectbox and Radio Constants
ACTIONS = ['Add', 'Edit', 'Remove']
CONCENTRATION_UNITS = ['mM', 'M', '%']
FORMULA_WEIGHT_UNITS = ['g/mol']
STATES = ['Liquid', 'Solid']
VOLUME_UNITS = ['mL', 'L']


st.write('# Solution Calculator')

ingredients_container = st.container(border=True)
ingredients_container.write('### Ingredients')


# Create an empty ingredients dataframe on first page load
if 'ingredients' not in st.session_state:
    ingredients = pd.DataFrame({
        'Ingredient': [], 'State': [],
        'Stock': [], 'Stock_Units': [],
        'Final_Concentration': [], 'Final_Concentration_Units': []
    })

    st.session_state.ingredients = ingredients

ingredients_container.dataframe(st.session_state.ingredients)


# Container for adding ingredients
with st.container(border=True):
    st.write('#### Update Ingredients List')
    st.radio('Select action', ACTIONS, key='action', horizontal=True)

    # Initialize current ingredient list for selectbox
    if 'curr_ingredients' in st.session_state:
        st.session_state['curr_ingredients'] = st.session_state.ingredients['Ingredient'].to_list()
    else:
        st.session_state['curr_ingredients'] = []

    # Conditional rendering of input options based on action
    if st.session_state.action == 'Remove':
        st.selectbox('Choose ingredient to remove', st.session_state['curr_ingredients'], key='ingredient')
    else:
        fields = st.columns([.2, .2, .2, .1, .2, .1])
        disable_stock = False
        disable_unit = False

        with fields[0]:
            if st.session_state['action'] == 'Add':
                st.text_input('Ingredient', key='ingredient')
            else:
                st.selectbox('Ingredient', st.session_state['curr_ingredients'], key='ingredient')

        with fields[1]:
            st.radio('State', STATES, key='state', horizontal=True)
        
        with fields[4]:
            st.number_input(
                'Final Concentration', key='final_conc',
                min_value=0.000, step=0.001, format='%.3f')
            
        with fields[5]:
            st.selectbox('Units', CONCENTRATION_UNITS, key='final_conc_unit')
        
        # Conditional rendering based on ingredient state of matter and units
        if st.session_state['state'] == 'Liquid':
            stock_label = 'Stock Concentration'
            unit_slice = CONCENTRATION_UNITS
        else:
            stock_label = 'Formula Weight'
            unit_slice = FORMULA_WEIGHT_UNITS
            disable_unit = True

            if st.session_state['final_conc_unit'] == '%':
                disable_stock = True

        with fields[2]:
            st.number_input(label=stock_label, key='stock', disabled=disable_stock, min_value=0.000, step=0.001, format='%.3f')

        with fields[3]:
            st.selectbox('Units', unit_slice, key='stock_unit', disabled=disable_unit)

    st.button('Update', on_click=update, kwargs=dict(session_state=st.session_state))


# Container to display recipe
with st.container(border=True):
    st.write('### Recipe')
    if 'recipe' in st.session_state:
        st.dataframe(st.session_state.recipe)


# Container for entering total volume and generating recipe
with st.container():
    final_volume_fields = st.columns([.2, .1, .7])

    with final_volume_fields[0]:
        st.number_input('Total Volume', key='total_volume', min_value=0.000, step=0.001, format='%.3f')

    with final_volume_fields[1]:
        st.selectbox('Units', VOLUME_UNITS, key='total_volume_units')

    st.button('Calculate', on_click=calculate_recipe, kwargs=dict(session_state=st.session_state), type='primary')
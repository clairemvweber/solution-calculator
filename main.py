import streamlit as st
import pandas as pd

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

# Functions for performing actions
def add_ingredient(row):
    # Don't allow dupes???
    st.session_state.ingredients = pd.concat([st.session_state.ingredients, row], ignore_index=True)


def get_ingredient_index():
    return st.session_state.ingredients.index[st.session_state.ingredients['Ingredient'] == st.session_state.ingredient].tolist()

def remove_ingredient():
    st.session_state.ingredients.drop(index=get_ingredient_index(), inplace=True)

# Function to reset ingredient inputs
def reset_inputs():
    st.session_state['ingredient'] = ''
    st.session_state['state'] = 'Liquid'
    st.session_state['stock'] = 0.000
    st.session_state['stock_units'] = CONCENTRATION_UNITS[0]
    st.session_state['final_conc'] = 0.000

    st.session_state.ingredients.reset_index(drop=True)
    st.session_state['action'] = 'Add'


# Function to update ingredients dataframe
def update():
    if st.session_state['action'] == 'Remove':
        remove_ingredient()
    else:
        row = pd.DataFrame({
            'Ingredient': [st.session_state.ingredient],
            'State': [st.session_state.state],
            'Stock': [st.session_state.stock],
            'Stock_Units': [st.session_state.stock_unit],
            'Final_Concentration': [st.session_state.final_conc],
            'Final_Concentration_Units': [st.session_state.final_conc_unit]
        })

        if st.session_state['action'] == 'Add':
            add_ingredient(row)
        else:
            remove_ingredient()
            add_ingredient(row)
    
    reset_inputs()

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

    st.button('Update', on_click=update)



# Conversions
def to_molar(c):
    return c / 1000

def to_mL(v):
    return v * 1000

def to_L(v):
    return v / 1000

def percent(p):
    return p / 100

# def to_grams(mg):
#     return mg * 1000

# Calculations
def dilution(c1, c2, v2):
    return c2 * v2 / c1

def solution(fw, c2, v2):
    return fw * c2 * v2


# Calculations
def calculate_ingredient(i):
    v1, v1_units = 1.0, 'mL'
    c1, c2, v2 = i.Stock, i.Final_Concentration, st.session_state.total_volume
    
    if i.Stock_Units == 'mM':
        c1 = to_molar(c1)

    if i.Stock_Units == '%':
        c1 = percent(c1)
            
    if i.Final_Concentration_Units == 'mM':
        c2 = to_molar(c2)
    
    if i.Final_Concentration_Units == '%':
        c2 = percent(c2)

    if st.session_state.total_volume_units == 'mL':
        v2 = to_L(v2)


    if i.State == 'Liquid':
        v1 = to_mL(dilution(c1, c2, v2))
    else:
        v1_units = 'g'

        if i.Final_Concentration_Units == '%':
            c1 = 1000

        v1 = solution(c1, c2, v2)
    
    return pd.DataFrame({'Ingredient': [i.Ingredient], 'Amount': [v1], 'Amount_Units': [v1_units]})

def calculate_recipe():
    recipe = pd.DataFrame({'Ingredient': [], 'Amount': [], 'Amount_Units': []})

    for ingredient in st.session_state.ingredients.itertuples():
        recipe = pd.concat([recipe, calculate_ingredient(ingredient)], ignore_index=True)

    st.session_state.recipe = recipe


# def reset_total_volume():
#     st.session_state['total_volume'] = 0.000

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

    st.button('Calculate', on_click=calculate_recipe, type='primary')
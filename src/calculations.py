import pandas as pd

# Conversions
def to_molar(c):
    return c / 1000

def to_mL(v):
    return v * 1000

def to_L(v):
    return v / 1000

def percent(p):
    return p / 100


# Calculation formulas
def dilution(c1, c2, v2):
    return c2 * v2 / c1

def solution(fw, c2, v2):
    return fw * c2 * v2


# Calculation functions
def calculate_ingredient(i, session_state):
    v1, v1_units = 1.0, 'mL'
    c1, c2, v2 = i.Stock, i.Final_Concentration, session_state.total_volume
    
    if i.Stock_Units == 'mM':
        c1 = to_molar(c1)

    if i.Stock_Units == '%':
        c1 = percent(c1)
            
    if i.Final_Concentration_Units == 'mM':
        c2 = to_molar(c2)
    
    if i.Final_Concentration_Units == '%':
        c2 = percent(c2)

    if session_state.total_volume_units == 'mL':
        v2 = to_L(v2)


    if i.State == 'Liquid':
        v1 = to_mL(dilution(c1, c2, v2))
    else:
        v1_units = 'g'

        if i.Final_Concentration_Units == '%':
            c1 = 1000

        v1 = solution(c1, c2, v2)
    
    return pd.DataFrame({'Ingredient': [i.Ingredient], 'Amount': [v1], 'Amount_Units': [v1_units]})


def calculate_recipe(session_state):
    recipe = pd.DataFrame({'Ingredient': [], 'Amount': [], 'Amount_Units': []})

    for ingredient in session_state.ingredients.itertuples():
        recipe = pd.concat([recipe, calculate_ingredient(ingredient, session_state)], ignore_index=True)

    session_state.recipe = recipe
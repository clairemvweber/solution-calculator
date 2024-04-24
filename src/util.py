import pandas as pd

# Actions
def add_ingredient(row, session_state):
    # Don't allow dupes???
    session_state.ingredients = pd.concat([session_state.ingredients, row], ignore_index=True)

def get_ingredient_index(session_state):
    return session_state.ingredients.index[session_state.ingredients['Ingredient'] == session_state.ingredient].tolist()

def remove_ingredient(session_state):
    session_state.ingredients.drop(index=get_ingredient_index(session_state), inplace=True)

# Function to reset ingredient inputs
def reset_inputs(session_state):
    session_state['ingredient'] = ''
    session_state['state'] = 'Liquid'
    session_state['stock'] = 0.000
    session_state['stock_units'] = 'mM'
    session_state['final_conc'] = 0.000

    session_state.ingredients.reset_index(drop=True)
    session_state['action'] = 'Add'

def update(session_state):
    if session_state['action'] == 'Remove':
        remove_ingredient(session_state)
    else:
        row = pd.DataFrame({
            'Ingredient': [session_state.ingredient],
            'State': [session_state.state],
            'Stock': [session_state.stock],
            'Stock_Units': [session_state.stock_unit],
            'Final_Concentration': [session_state.final_conc],
            'Final_Concentration_Units': [session_state.final_conc_unit]
        })

        if session_state['action'] == 'Add':
            add_ingredient(row, session_state)
        else:
            remove_ingredient(session_state)
            add_ingredient(row, session_state)
    
    reset_inputs(session_state)

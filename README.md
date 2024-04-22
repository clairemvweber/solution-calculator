# Solution Calculator
---
Solution Calculator is used to create a recipe for chemical solutions given ingredients, their stock concentration/formula weight, the desired concentration of the ingredients, and the total volume of the solution. This app aims to reduce calculation time and errors for scientists and technicians in their workflow.
<br>

Try the Solution Calculator [here](https://the-ultimate-solution-calculator.streamlit.app/)

---

### Built With
- [Streamlit](https://docs.streamlit.io/)
- [Pandas](https://pandas.pydata.org/docs/)

---

### Getting Started

#### Prerequisites
In addition to Python, Streamlit must be installed.

```
pip install streamlit
```

Note: installing Streamlit will install Pandas if Pandas is not already installed.

#### Installation
Clone the repo:

```
git clone https://github.com/cmvweber1123/solution-calculator.git
```

#### Running
To run locally, from the project directory run the following code in the command line:
```
streamlit run src/app.py
```

The app should open in a new browser page. However if it does not, check the command line for the Local URL and enter that URL into the browser's address bar.

---
### Roadmap
- [X] Add "Edit" and "Remove" actions for ingredients
- [X] Conditional rendering of "Update Ingredient List" based on action and selected options
- [ ] Add tests
- [ ] Add live demo to README
- [ ] Automatically populate fields with existing values when editing ingredients
- [ ] Add icons and update app visuals
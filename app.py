# %%
# Import dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, State

# %%
# read in data
data = pd.read_csv("/Users/tilliedavies/Downloads/A4_student/gdp_pcap.csv")

# %%
# create a year column using pd.melt
melted = pd.melt(data, id_vars='country', var_name='year', value_name='GDP Per Capita')
# convert column to an integer so it can be used in the graph
melted['year'] = melted['year'].astype(int)
# fix values that have "k" instead of thousand 
melted['GDP Per Capita'] = melted['GDP Per Capita'].replace({"k":"*1e3"}, regex=True).map(pd.eval).astype(int)

# %%
# create graph using plotly express, px.line() produces a line graph
fig = px.line(melted, 
              x='year',
              y='GDP Per Capita', 
              color='country',
              title = 'GDP Per Capita Over Time')

# %%
# load the CSS stylesheet
# %%
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# %%
app = Dash(__name__, external_stylesheets=stylesheets)

# %%
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Tilda Davies Assignment 5', className="app-header--title") # creating the title of the page 
        ]
    ),
    html.Div(
        children=html.Div([
            html.H1('Description'),
            html.Div('''
                     The following data comes largely from the World Bank.
                      It reaches all the way back to the year 1800. 
                     It also includes estimates of GDP per capita in the future, based on historical trends. 
                     Using the dropdown and slider below, you can look at the countries and time range you've specified.
            ''')
        ])
    ),
    html.Div(children=[
        html.H2(children = 'Select Countries'),
        # add dropdown to app, options for the dropdown are every unique value from the country column of our dataset
        dcc.Dropdown(
            melted.country.unique(), 
            id='country_dropdown',
            placeholder = 'select a country',  
            multi=True,
            value = 'USA'
            )
        # adjust style so that this and the slider can be next to each other
    ], style={'display': 'inline-block', 'width': '50%'}),
    html.Div([   
        html.H2(children = 'Select Year Range'),
        # add range slider for year selection, specifying min and max as well as a tooltip 
        dcc.RangeSlider(
            id='year_slider',
            min=melted['year'].min(),
            max = melted['year'].max(),
            value=[melted['year'].min(), melted['year'].max()],
            marks={year: {'label': str(year), 'style': {'writingMode': 'vertical-rl'}} 
                     for year in range(melted['year'].min(), melted['year'].max() + 1, 10)},
            step=1, 
            tooltip={'always_visible': True}
    )
    ], style={'display': 'inline-block', 'width': '50%'}),
    html.Div(
    # add graph that was built earlier
        dcc.Graph(
            id='graph', 
            figure=fig,
            style = {'marginTop': '50px'}))
])

@app.callback(
    Output('graph','figure'),
    Input('country_dropdown','value'),
    Input('year_slider','value'))

def update_graph(selected_country, selected_year): 
    if not isinstance(selected_country, list): # without this, we get a value error --> ensuring the data from the dropdown is a string
        # so that we can compare columns of different lengths
        selected_country = [selected_country]

    # need to ensure all inputs are within the available options from the data...without this we get an error
    dff = melted[(melted['year'] >= selected_year[0]) & (melted['year'] <= selected_year[1]) &
                   (melted['country'].isin(selected_country))]

    fig = px.line(dff, # creating my line graph
                    x = 'year', 
                    y = 'GDP Per Capita', 
                    color = 'country',
                    title = 'GDP Per Capita Over Time',
                    )

    return fig

# deploy app within Jupyter Notebook
if __name__ == '__main__':
    app.run_server(debug=True, port=8056)



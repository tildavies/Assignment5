# %%
# Import dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State

# %%
# read in data
data = pd.read_csv("gdp_pcap.csv")

# %%
# create a year column using pd.melt
melted = pd.melt(data, id_vars=['country'], var_name='year', value_name='value')
# fix values that have "k" instead of thousand 
melted['value'] = melted['value'].replace({"k":"*1e3"}, regex=True).map(pd.eval).astype(int)
# convert column to an integer so it can be used in the graph
melted['value'] = melted['value'].astype(int)

# %%
# create graph using plotly express, px.line() produces a line graph
graph = px.line(melted, x='year',y='value', color='country')
# use update_layout() function to add a title and change the axis labels
graph.update_layout(
    title= 'GPD Per Capita over Time',
    xaxis_title='Year',
    yaxis_title='GDP Per Capita'
)

# %%
# Load the CSS stylesheet
stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] 

# initialize app
app = Dash(__name__, external_stylesheets=stylesheet)
server=app.server

app.layout = html.Div([
    # use dcc.Markdown to add the title and three sentence summary to top of app
    dcc.Markdown('''
    # Global GDP Per Capita Over Time
    _The following data comes largely from the World Bank. It reaches all the way back to the year 1800. It also includes estimates of GDP per capita in the future, based on historical trends. Using the dropdown and slider below, you can look at the countries and time range you've specified._              
                 '''),
    html.Div([
        # add dropdown to app, options for the dropdown are every unique value from the country column of our dataset
        dcc.Dropdown(id='country_dropdown', options=data.country.unique(), multi=True)
        # adjust style so that this and the slider can be next to each other
    ], style={'display': 'inline-block', 'width': '48%'}),
    html.Div([   
        # add range slider for year selection, specifying min and max as well as a tooltip 
        dcc.RangeSlider( id='year_slider',
            min=1800,
            max=2100,
            step=1,
            marks = {1800:"1800",1850:"1850",1900:"1900",1950:"1950",2000:"2000",2050:"2050",2100:"2100"},
            tooltip={"always_visible": True})
    ], style={'display': 'inline-block', 'width': '48%'}),
    # add graph that was built earlier
    dcc.Graph(id='graph', figure=graph)
])

@app.callback(
    Output('graph','figure'),
    [Input('year_slider','value'),
    Input('country_dropdown','value')]
)

def update_graph(selected_country, selected_years):
    filtered_df = melted[(melted['country'].isin(selected_country)) & 
                       (melted['year'] >= selected_years[0]) & 
                       (melted['year'] <= selected_years[1])]
    
    fig = px.line(filtered_df, x='year', y='value', color='country', title='GDP x Year')
    
    return fig


# deploy app within Jupyter Notebook
if __name__ == '__main__':
    app.run_server(debug=True, port=8055)



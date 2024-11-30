# Import required libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the airline data into a pandas DataFrame
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
    encoding="ISO-8859-1",
    dtype={'Div1Airport': str, 'Div1TailNum': str, 
           'Div2Airport': str, 'Div2TailNum': str}
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(
        'Total number of flights to the destination state split by reporting airline (Afifa Puspitasari)', 
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': '40px'}
    ),
    html.Div([
        "Input Year: ",
        dcc.Input(
            id='input-year',
            value='2010',
            type='number',
            style={'height': '50px', 'font-size': '35px'}
        ),
    ], style={'font-size': '40px'}),
    html.Br(), html.Br(),
    html.Div(dcc.Graph(id='bar-plot')),
])

# Add a callback decorator
@app.callback(
    Output(component_id='bar-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value')
)
def get_graph(entered_year):
    """Generate a bar plot based on the entered year."""
    # Filter data for the selected year
    df = airline_data[airline_data['Year'] == int(entered_year)]
    
    # Aggregate the data
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()
    
    # Create the bar chart
    fig = px.bar(
        bar_data, 
        x="DestState", 
        y="Flights", 
        title='Total number of flights to the destination state split by reporting airline'
    )
    
    # Update layout for better readability
    fig.update_layout(
        title='Flights to Destination State',
        xaxis_title='Destination State',
        yaxis_title='Number of Flights'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas DataFrame
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding="ISO-8859-1",
    dtype={
        'Div1Airport': str, 'Div1TailNum': str,
        'Div2Airport': str, 'Div2TailNum': str
    }
)

# Create a Dash application
app = dash.Dash(__name__)
#Change the title to the dashboard from "Flight Delay Time Statistics" to "Flight Details Statistics Dashboard" using HTML H1 component and font-size as 35.
# Build Dash app layout
app.layout = html.Div(children=[
    html.H1(
        'Flight Details Statistics Dashboard (Afifa Puspitasari)',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': '35px'}
    ),
    html.Div([
        "Input Year: ",
        dcc.Input(
            id='input-year',
            value='2010',
            type='number',
            style={'height': '35px', 'font-size': '30px'}
        )
    ], style={'font-size': '30px'}),
    html.Br(),
    html.Br(),
    # Segment 1
    html.Div([
        html.Div(dcc.Graph(id='carrier-plot')),
        html.Div(dcc.Graph(id='weather-plot'))
    ], style={'display': 'flex'}),
    # Segment 2
    html.Div([
        html.Div(dcc.Graph(id='nas-plot')),
        html.Div(dcc.Graph(id='security-plot'))
    ], style={'display': 'flex'}),
    # Segment 3
    html.Div(dcc.Graph(id='late-plot'), style={'width': '65%'})
])

def compute_info(airline_data, entered_year):
    """
    Compute averages for delays by category.

    Args:
        airline_data: Input airline data as a DataFrame.
        entered_year: The year for which data is required.

    Returns:
        Tuple containing data for carrier, weather, NAS, security, and late aircraft delays.
    """
    # Filter data for the selected year
    df = airline_data[airline_data['Year'] == int(entered_year)]
    
    # Compute average delays for each category
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late

# Callback decorator
@app.callback(
    [
        Output('carrier-plot', 'figure'),
        Output('weather-plot', 'figure'),
        Output('nas-plot', 'figure'),
        Output('security-plot', 'figure'),
        Output('late-plot', 'figure')
    ],
    Input('input-year', 'value')
)
def get_graph(entered_year):
    """
    Generate figures for the input year.

    Args:
        entered_year: Year entered by the user.

    Returns:
        List of Plotly figures for each delay category.
    """
    # Compute averages for the selected year
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)

    # Line plot for carrier delay
    carrier_fig = px.line(
        avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline',
        title='Average Carrier Delay Time (minutes) by Airline'
    )
    # Line plot for weather delay
    weather_fig = px.line(
        avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
        title='Average Weather Delay Time (minutes) by Airline'
    )
    # Line plot for NAS delay
    nas_fig = px.line(
        avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline',
        title='Average NAS Delay Time (minutes) by Airline'
    )
    # Line plot for security delay
    sec_fig = px.line(
        avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline',
        title='Average Security Delay Time (minutes) by Airline'
    )
    # Line plot for late aircraft delay
    late_fig = px.line(
        avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
        title='Average Late Aircraft Delay Time (minutes) by Airline'
    )

    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

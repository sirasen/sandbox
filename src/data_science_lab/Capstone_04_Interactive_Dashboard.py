# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("./spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

options = [{'label': 'All Sites', 'value': 'ALL'}]
options.extend([{"label": _, "value": _} for _ in spacex_df['Launch Site'].unique()])

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),

        html.Div(
            dcc.Dropdown(
                id='site-dropdown',
                options=options,
                value='ALL',
                placeholder="Select Site",
                searchable=True,
            )
        ),

        html.Br(),

        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
        ),

        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ]
)

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        return px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches By Site')
    else:
        return px.pie(
            spacex_df[spacex_df['Launch Site'] == entered_site],
            values='Flight Number',
            names='class',
            title='Total Success Launches for site {0}'.format(entered_site))

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value'),
    ]
)
def get_scatter_plot(entered_site, selected_payload_range):
    if entered_site == 'ALL':
        return px.scatter(
            spacex_df,
            x='Payload Mass (kg)',
            y='class',
            color="Booster Version Category",
            title='Correlation between Payload and Success for all Sites',
            range_x = selected_payload_range,
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        return px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color="Booster Version Category",
            title='Correlation between Payload and Success for site {0}'.format(entered_site),
            range_x = selected_payload_range,
        )


# Run the app
if __name__ == '__main__':
    app.run_server()
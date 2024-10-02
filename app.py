from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px


def load_data():
    data = {
        'country': ['USA', 'Canada', 'Germany', 'Rwanda', 'Burundi'],
        'Year': [2020, 2021, 2022, 2023, 2024],
        'Life Expectancy': [78.5, 80.0, 79.4, 66.0, 61.5], 
        'Infant Mortality': [5.9, 4.5, 3.5, 30.0, 40.0],   
        'Access to Healthcare': [60, 70, 88, 90, 85],      
        'Diabetes': [10.5, 9.8, 9.0, 6.5, 5.0],           
        'Heart Disease': [6.5, 6.0, 5.8, 4.0, 3.5],        
        'Vaccination': [85, 98, 80, 95, 96]   

    }
    return pd.DataFrame(data)

app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css'])
df = load_data()

app.layout = html.Div([
    
    html.Div([
        html.H1("Global Health Metric Dashboard", className="text-center mb-4"),

        
        html.Div([

            
            html.Div([
                html.Label("Select Countries", className="form-label"),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{'label': country, 'value': country} for country in df['country'].unique()],
                    value=['Rwanda','Burundi','USA'],
                    multi=True, 
                    className="form-select"
                )
            ], className="col-md-6 mb-3"),

            
            html.Div([
                html.Label("Select Indicator", className="form-label"),
                dcc.Dropdown(
                    id="indicator-dropdown",
                    options=[
                        {'label': 'Life Expectancy', 'value': 'Life Expectancy'},
                        {'label': 'Infant Mortality', 'value': 'Infant Mortality'},
                        {'label': 'Access to Healthcare', 'value': 'Access to Healthcare'},
                        {'label': 'Diabetes Prevalence', 'value': 'Diabetes'},
                        {'label': 'Heart Disease Prevalence', 'value': 'Heart Disease'},
                        {'label': 'Vaccination Rates', 'value': 'Vaccination'},
                    ],
                    value='Life Expectancy',
                    className="form-select"
                )
            ], className="col-md-6 mb-3"),

            
            html.Div([
                html.Label("Select Year Range", className="form-label"),
                dcc.RangeSlider(
                    id='year-slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=[df['Year'].min(), df['Year'].max()],
                    className="form-range"
                )
            ], className="col-md-12 mb-4"),

        ], className="card card-body mb-4"),

        
        html.Div([
            dcc.Graph(id="health-graph", className="mb-4")
        ], className="card card-body"),

       
        html.Div([
            html.Button("Download Graph Data", id='download-button', className="btn btn-primary mb-3"),
            dcc.Download(id='download-graph')
        ], className="text-center"),

    ], className="container mt-4")
])

@app.callback(
    Output('health-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('indicator-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_graph(selected_country, selected_indicator, selected_year):
    
    filtered_df = df[
        (df['country'].isin(selected_country)) &
        (df['Year'] >= selected_year[0]) &
        (df['Year'] <= selected_year[1])
    ]

  
    max_value = filtered_df[selected_indicator].max()

    if selected_indicator == 'Life Expectancy' or selected_indicator == 'Infant Mortality':
        fig = px.bar(
            filtered_df,
            x='Year',
            y=selected_indicator,      
            color='country',
            title=f'{selected_indicator} Over Time'
        )
    elif selected_indicator in ['Access to Healthcare', 'Diabetes', 'Heart Disease', 'Vaccination']:
        fig = px.bar(
            filtered_df,
            x='Year',
            y=selected_indicator,
            color='country',
            title=f'{selected_indicator} Over Time'
        )
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=selected_indicator,
        shapes=[  
            {
                'type': 'line',
                'x0': 2022,  
                'y0': 0,
                'x1': 2022,
                'y1': max_value,
                'line': {'color': 'Red', 'width': 2}
            }
        ],
        annotations=[ 
            {
                'x': 2022,  
                'y': max_value,
                'xref': 'x',
                'yref': 'y',
                'text': 'Policy Change',
                'showarrow': True,
                'arrowhead': 2,
                'ax': 0,
                'ay': -40
            }
        ]
    )

    return fig

@app.callback(
    Output('download-graph','data'),
    Input('download-button','n_clicks'),
    prevent_initial_call=True,

)  

def func(n_clicks):
    return dcc.send_data_frame(df.to_csv,'mydf.csv')

if __name__ == '__main__':
    app.run(debug=True)

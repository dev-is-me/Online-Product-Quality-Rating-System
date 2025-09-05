from dash import dcc, html

# Define styles
header_style = {
    'text-align': 'center',
    'color': 'white'
}

subheader_style = {
    'text-align': 'center',
    'color': 'white'
}

graph_style = {
    'text-align': 'center',
    'padding': '20px',
    'border': '1px solid #ccc',
    'border-radius': '10px',
    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
    'background-color': '#f9f9f9',
    'transition': 'all 0.3s ease'
}

button_style = {
    'background-color': '#007bff',
    'color': 'white',
    'border': 'none',
    'padding': '10px 20px',
    'text-align': 'center',
    'text-decoration': 'none',
    'display': 'inline-block',
    'font-size': '16px',
    'margin': '4px 2px',
    'cursor': 'pointer',
    'border-radius': '12px',
    'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    'transition': 'all 0.3s ease'
}

# Define the layout for the home page
home_layout = html.Div([
    html.Div([
        html.H1("i-PQRS", style=header_style),
    ], style={'background-color': '#0047AB', 'padding': '10px'}),

    html.Div([
        dcc.Graph(id='gauge1', style={'margin': 'auto'}),
        html.H2("Overall PQRS Score ", style={'text-align': 'center', 'margin-top': '10px'})
    ], style=graph_style),

    html.Div([
        html.H2("Section Wise: i-PQRS", style=subheader_style),
    ], style={'background-color': '#0047AB', 'padding': '10px', 'margin-bottom': '10px'}),

    html.Div([
        html.Div([
            dcc.Link(html.Button("Go to Product Defects", style=button_style), href='/page-1'),
            dcc.Graph(id='gauge2', style={'margin-top': '20px'}),
            html.H2("Product-PQRS Score", style={'text-align': 'center', 'margin-top': '10px'})
        ], style=graph_style),

        html.Div([
            dcc.Link(html.Button("Go to Primary Packing Defects", style=button_style), href='/page-2'),
            dcc.Graph(id='gauge3', style={'margin-top': '20px'}),
            html.H2("Primary packing-PQRS Score", style={'text-align': 'center', 'margin-top': '10px'})
        ], style=graph_style),

        html.Div([
            dcc.Link(html.Button("Go to Secondary Packing Defects", style=button_style), href='/page-3'),
            dcc.Graph(id='gauge4', style={'margin-top': '20px'}),
            html.H2("Secondary Packing-PQRS Score", style={'text-align': 'center', 'margin-top': '10px'})
        ], style=graph_style)
    ], style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)', 'gap': '20px'})
])


# import dash
# app = dash.Dash(__name__)
# app.layout = home_layout

# if __name__ == '__main__':
#     app.run_server(debug=True)

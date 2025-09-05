import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from read_write import update_excel
from get_score import get_score
from get_score import recalculate_excel
from gauge import create_gauge
from home_layout import home_layout
from Read_plcdata import plcdata
import product
import primary
import secondary

# Initialize the Dash app with suppress_callback_exceptions=True
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Directory for CSV files
from directory import directory,directory_Calc


# Define the main layout of the app
main_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Interval(
        id='interval-component',
        interval=900*1000,  # Update every 15 minutes (900,000 milliseconds)
        n_intervals=0
    )
])

# Callback to control page navigation
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page-1':
        return product.page_1_layout
    elif pathname == '/page-2':
        return primary.page_2_layout
    elif pathname == '/page-3':
        return secondary.page_3_layout
    else:
        return home_layout

# Include the main layout in the app
app.layout = main_layout

# Common callback to update all gauges on the home page
@app.callback(
    [Output('gauge1', 'figure'),
     Output('gauge2', 'figure'),
     Output('gauge3', 'figure'),
     Output('gauge4', 'figure')],
    [Input('interval-component', 'n_intervals')]
)

def update_gauges(n):
    
    update_excel(directory,directory_Calc)
    plcdata(directory_Calc)

    recalculate_excel(f"{directory_Calc}/Calc_Worksheet.xlsx")
    key='Product'
    Product_Score= get_score(directory_Calc,key)
    key='Primary'
    Primary_Score= get_score(directory_Calc,key)
    key='Secondary'
    Secondary_Score= get_score(directory_Calc,key)

    #Score=(Product_Score+Primary_Score+Secondary_Score)/3
    Score=(Product_Score/100*Primary_Score/100*Secondary_Score/100)*100

    fig1 = create_gauge(Score)
    fig2 = create_gauge(Product_Score)
    fig3 = create_gauge(Primary_Score)
    fig4 = create_gauge(Secondary_Score)
    
    return fig1, fig2, fig3, fig4

# Import callbacks and layouts from other files
product.register_callbacks(app)
primary.register_callbacks(app)
secondary.register_callbacks(app)
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)  # use_reloader=True allows for continuous running



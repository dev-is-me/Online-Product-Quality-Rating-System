import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Path to the Excel file
from directory import directory_Calc
excel_path = f"{directory_Calc}/Calc_Worksheet.xlsx"

# Function to read defect data from Sheet 3
def read_defect_data():
    df = pd.read_excel(excel_path, sheet_name='Sheet3')
    product_df = df[df.iloc[:, 0] == 'Product']  # Filter rows where the first column (key) is 'Product'
    defects = product_df.iloc[:, 1].tolist()     # Get the second column as the list of defects
    percentages = product_df.iloc[:, 2].tolist() # Get the third column as the list of percentages
    lag_percentages = product_df.iloc[:, 3].tolist()
    lead_percentages = product_df.iloc[:, 4].tolist()
    percentages = [round(p, 2) for p in percentages]
    lag_percentages = [round(p, 2) for p in lag_percentages]
    lead_percentages = [round(p, 2) for p in lead_percentages]
    return defects, percentages, lag_percentages, lead_percentages

# Function to read indicator data from Sheet 4
def read_indicator_data():
    df = pd.read_excel(excel_path, sheet_name='Sheet4')
    keys = df.iloc[:, 0].tolist()
    indicators = df.iloc[:, 1].tolist()
    current_values = df.iloc[:, 2].tolist()
    range_A = df.iloc[:, 4].tolist()
    range_B = df.iloc[:, 7].tolist()
    set_value = df.iloc[:, 5].tolist()
    contribution = df.iloc[:, 10].tolist()
    contribution = [round(c, 3) for c in contribution]
    current_values = [round(c, 3) for c in current_values]
    uoms = df.iloc[:, 11].tolist()
    return keys, indicators, current_values, range_A, range_B, set_value, contribution, uoms

# Get initial data for tables
defects, percentages, lag_percentages, lead_percentages = read_defect_data()
keys, indicators, current_values, range_A, range_B, set_value, contribution, uoms = read_indicator_data()

# Create a DataFrame for indicator data for easier manipulation
indicator_df = pd.DataFrame({
    'Key': keys,
    'Indicator': indicators,
    'Current Value': current_values,
    'Range A': range_A,
    'Range B': range_B,
    'UOM': uoms,
    'Set_Value': set_value,
    'Contribution %': contribution
})

# Define the layout for Product page
page_1_layout = html.Div([
    html.H1("Leading Defect Indicators", style={'text-align': 'center', 'background-color': '#0047AB', 'color': 'white', 'padding': '10px'}),
    
    html.Div([
        # Table 1: Defects
        html.Div([
            html.H2("Defects", style={'text-align': 'center'}),
            dash_table.DataTable(
                id='table1',
                columns=[{'name': 'Defect', 'id': 'defect'}, 
                         {'name': 'Percentage Contribution', 'id': 'percentage'}, 
                         {'name': 'Lag Percentage', 'id': 'lag_percentage'}, 
                         {'name': 'Lead Percentage', 'id': 'lead_percentage'}],
                data=[{'defect': defect, 'percentage': percentage, 'lag_percentage': lag_percentage, 'lead_percentage': lead_percentage} 
                      for defect, percentage, lag_percentage, lead_percentage in zip(defects, percentages, lag_percentages, lead_percentages)],
                row_selectable='single',  # Allow single row selection
                selected_rows=[0],  # Default selection
                style_table={'width': '90%', 'margin': 'auto'},
                style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
                style_cell={'text-align': 'center'}
            ),
            dcc.Interval(
                id='interval-table1',
                interval=5*1000,  # Update every 5 seconds
                n_intervals=0
            )
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # Table 2: Indicators
        html.Div([
            html.H2("Indicators", style={'text-align': 'center'}),
            dash_table.DataTable(
                id='table2',
                columns=[{'name': 'Indicator', 'id': 'Indicator'},
                         {'name': 'Current Value', 'id': 'Current Value'},
                         {'name': 'Range A', 'id': 'Range A'},
                         {'name': 'Range B', 'id': 'Range B'},
                         {'name': 'UOM', 'id': 'UOM'},
                         {'name': 'Set_Value', 'id': 'Set_Value'},
                         {'name': 'Contribution %', 'id': 'Contribution %'}],
                data=[],  # Empty data initially
                style_table={'width': '90%', 'margin': 'auto'},
                style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
                style_cell={'text-align': 'center'}
            ),
            dcc.Interval(
                id='interval-table2',
                interval=5*1000,  # Update every 5 seconds
                n_intervals=0
            )
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'text-align': 'center'})
])

# Function to register callbacks
def register_callbacks(app):
    # Combined callback to update Table 1 (Defects) and Table 2 (Indicators)
    @app.callback(
        [Output('table1', 'data'),
         Output('table2', 'data')],
        [Input('interval-table1', 'n_intervals'),
         Input('interval-table2', 'n_intervals'),
         Input('table1', 'selected_rows')]
    )
    def update_tables(n1, n2, selected_rows):
        # Update Table 1
        defects, percentages, lag_percentages, lead_percentages = read_defect_data()
        table1_data = [{'defect': defect, 'percentage': percentage, 'lag_percentage': lag_percentage, 'lead_percentage': lead_percentage} 
                       for defect, percentage, lag_percentage, lead_percentage in zip(defects, percentages, lag_percentages, lead_percentages)]
        
        # Update Table 2 based on selected row in Table 1
        keys, indicators, current_values, range_A, range_B, set_value, contribution, uoms = read_indicator_data()

        if selected_rows is not None and len(selected_rows) > 0:
            selected_defect = defects[selected_rows[0]]
        else:
            selected_defect = defects[0]
        
        filtered_df = indicator_df[indicator_df['Key'] == selected_defect]
        table2_data = filtered_df[['Indicator', 'Current Value', 'Range A', 'Range B', 'UOM', 'Set_Value', 'Contribution %']].to_dict('records')
        
        return table1_data, table2_data

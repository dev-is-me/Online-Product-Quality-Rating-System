# import pandas as pd
# from dash import dcc, html, dash_table
# from dash.dependencies import Input, Output

# # Path to the Excel file
# from directory import directory_Calc
# excel_path = f"{directory_Calc}/Calc_Worksheet.xlsx"

# # Function to read defect data from Sheet 3
# def read_defect_data():
#     df = pd.read_excel(excel_path, sheet_name='Sheet3')
#     primary_df = df[df.iloc[:, 0] == 'Primary']  # Filter rows where the first column (key) is 'Primary'
#     defects = primary_df.iloc[:, 1].tolist()     # Get the second column as the list of defects
#     percentages = primary_df.iloc[:, 2].tolist() # Get the third column as the list of percentages
#     percentages = [round(p, 2) for p in percentages]
#     return defects, percentages

# # Function to read indicator data from Sheet 5
# def read_indicator_data():
#     df = pd.read_excel(excel_path, sheet_name='Sheet5')
#     keys = df.iloc[:, 0].tolist()
#     machines = df.iloc[:, 1].tolist()
#     indicators = df.iloc[:, 2].tolist()
#     current_values = df.iloc[:, 3].tolist()
#     ranges = df.iloc[:, 4].tolist()
#     uoms = df.iloc[:, 5].tolist()
#     set_value = df.iloc[:, 6].tolist()
#     contribution = df.iloc[:, 10].tolist()
#     contribution = [round(c, 2) for c in contribution]
#     return keys, machines, indicators, current_values, ranges, uoms, set_value, contribution

# # Get initial data for tables
# defects, percentages = read_defect_data()
# keys, machines, indicators, current_values, ranges, uoms, set_value, contribution = read_indicator_data()

# # Create a DataFrame for indicator data for easier manipulation
# indicator_df = pd.DataFrame({
#     'Key': keys,
#     'Machine': machines,
#     'Indicator': indicators,
#     'Current Value': current_values,
#     'Range': ranges,
#     'UOM': uoms,
#     'Set_Value': set_value,
#     'Contribution %': contribution
# })

# # Define the layout for Primary page
# page_2_layout = html.Div([
#     html.H1("Leading Defect Indicators", style={'text-align': 'center', 'background-color': '#0047AB', 'color': 'white', 'padding': '10px'}),

#     html.Div([
#         # Left half: Table 1 and Table 2
#         html.Div([
#             # Table 1: Defects
#             html.Div([
#                 html.H2("Defects", style={'text-align': 'center'}),
#                 dash_table.DataTable(
#                     id='primary-table1',  # Updated ID
#                     columns=[{'name': 'Defect', 'id': 'defect'}, {'name': 'Percentage Contribution', 'id': 'percentage'}],
#                     data=[{'defect': defect, 'percentage': percentage} for defect, percentage in zip(defects, percentages)],
#                     row_selectable='single',  # Allow single row selection
#                     selected_rows=[0],  # Default selection
#                     style_table={'width': '90%', 'margin': 'auto'},
#                     style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
#                     style_cell={'text-align': 'center', 'padding': '5px'},
#                     style_data={'whiteSpace': 'normal', 'height': 'auto'},
#                     css=[{
#                         'selector': '.dash-table-container',
#                         'rule': 'font-family: Arial, sans-serif; font-size: 14px;'
#                     }]
#                 ),
#                 dcc.Interval(
#                     id='primary-interval-table1',  # Updated ID
#                     interval=5*1000,  # Update every 5 seconds
#                     n_intervals=0
#                 )
#             ], style={'margin-bottom': '20px'}),
            
#             # Table 2: Machine Selector
#             html.Div([
#                 html.H2("Machines", style={'text-align': 'center'}),
#                 dash_table.DataTable(
#                     id='primary-table2',  # Updated ID
#                     columns=[{'name': 'Machine', 'id': 'Machine'}],
#                     data=[{'Machine': f'Packing Machine {i}'} for i in range(1, 7)],
#                     row_selectable='single',  # Allow single row selection
#                     selected_rows=[0],  # Default selection
#                     style_table={'width': '90%', 'margin': 'auto'},
#                     style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
#                     style_cell={'text-align': 'center', 'padding': '5px'},
#                     style_data={'whiteSpace': 'normal', 'height': 'auto'},
#                     css=[{
#                         'selector': '.dash-table-container',
#                         'rule': 'font-family: Arial, sans-serif; font-size: 14px;'
#                     }]
#                 ),
#                 dcc.Interval(
#                     id='primary-interval-table2',  # Updated ID
#                     interval=5*1000,  # Update every 5 seconds
#                     n_intervals=0
#                 )
#             ], style={'margin-bottom': '20px'})
#         ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
#         # Right half: Table 3
#         html.Div([
#             html.H2("Indicators", style={'text-align': 'center'}),
#             dash_table.DataTable(
#                 id='primary-table3',  # Updated ID
#                 columns=[{'name': 'Indicator', 'id': 'Indicator'},
#                          {'name': 'Current Value', 'id': 'Current Value'},
#                          {'name': 'Range', 'id': 'Range'},
#                          {'name': 'UOM', 'id': 'UOM'},
#                          {'name': 'Set_Value', 'id': 'Set_Value'},
#                          {'name': 'Contribution %', 'id': 'Contribution %'}],
#                 data=[],  # Empty data initially
#                 style_table={'width': '90%', 'margin': 'auto'},
#                 style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
#                 style_cell={'text-align': 'center', 'padding': '5px'},
#                 style_data={'whiteSpace': 'normal', 'height': 'auto'},
#                 css=[{
#                     'selector': '.dash-table-container',
#                     'rule': 'font-family: Arial, sans-serif; font-size: 14px;'
#                 }]
#             ),
#             dcc.Interval(
#                 id='primary-interval-table3',  # Updated ID
#                 interval=5*1000,  # Update every 5 seconds
#                 n_intervals=0
#             )
#         ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'})
#     ], style={'display': 'flex', 'justify-content': 'space-between', 'padding': '20px'})
# ])

# # Function to register callbacks
# def register_callbacks(app):
#     @app.callback(
#         [Output('primary-table1', 'data'),  # Updated ID
#          Output('primary-table2', 'data'),  # Updated ID
#          Output('primary-table3', 'data')],  # Updated ID
#         [Input('primary-interval-table1', 'n_intervals'),  # Updated ID
#          Input('primary-interval-table2', 'n_intervals'),  # Updated ID
#          Input('primary-interval-table3', 'n_intervals'),  # Updated ID
#          Input('primary-table1', 'selected_rows'),  # Updated ID
#          Input('primary-table2', 'selected_rows')]  # Updated ID
#     )
#     def update_tables(n1, n2, n3, selected_defect_rows, selected_machine_rows):
#         # Update Table 1
#         defects, percentages = read_defect_data()
#         table1_data = [{'defect': defect, 'percentage': percentage} for defect, percentage in zip(defects, percentages)]

#         # Update Table 2 (no change in data for this table, hence static data)
#         table2_data = [{'Machine': f'Packing Machine {i}'} for i in range(1, 7)]

#         # Update Table 3 based on selected row in Table 1 and Table 2
#         keys, machines, indicators, current_values, ranges, uoms, set_value, contribution = read_indicator_data()
#         indicator_df = pd.DataFrame({
#             'Key': keys,
#             'Machine': machines,
#             'Indicator': indicators,
#             'Current Value': current_values,
#             'Range': ranges,
#             'UOM': uoms,
#             'Set_Value': set_value,
#             'Contribution %': contribution
#         })

#         selected_defect = defects[selected_defect_rows[0]] if selected_defect_rows else defects[0]
#         selected_machine = f'Packing Machine {selected_machine_rows[0] + 1}' if selected_machine_rows else 'Packing Machine 1'

#         filtered_df = indicator_df[(indicator_df['Key'] == selected_defect) & (indicator_df['Machine'] == selected_machine)]

#         table3_data = filtered_df[['Indicator', 'Current Value', 'Range', 'UOM', 'Set_Value', 'Contribution %']].to_dict('records')

#         return table1_data, table2_data, table3_data


import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Path to the Excel file
from directory import directory_Calc
excel_path = f"{directory_Calc}/Calc_Worksheet.xlsx"

# Function to read defect data from Sheet 3
def read_defect_data():
    df = pd.read_excel(excel_path, sheet_name='Sheet3')
    product_df = df[df.iloc[:, 0] == 'Primary']  # Filter rows where the first column (key) is 'Product'
    defects = product_df.iloc[:, 1].tolist()     # Get the second column as the list of defects
    percentages = product_df.iloc[:, 2].tolist() # Get the third column as the list of percentages
    lag_percentages = product_df.iloc[:, 3].tolist()
    lead_percentages = product_df.iloc[:, 4].tolist()
    percentages = [round(p, 2) for p in percentages]
    lag_percentages = [round(p, 2) for p in lag_percentages]
    lead_percentages = [round(p, 2) for p in lead_percentages]
    return defects, percentages, lag_percentages, lead_percentages

# Function to read indicator data from Sheet 5
def read_indicator_data():
    df = pd.read_excel(excel_path, sheet_name='Sheet5')
    keys = df.iloc[:, 0].tolist()
    machines= df.iloc[:, 1].tolist()
    indicators = df.iloc[:, 2].tolist()
    current_values = df.iloc[:, 3].tolist()
    range_A = df.iloc[:, 5].tolist()
    range_B = df.iloc[:, 8].tolist()
    set_value = df.iloc[:, 6].tolist()
    contribution = df.iloc[:, 11].tolist()
    contribution = [round(c, 3) for c in contribution]
    uoms = df.iloc[:, 12].tolist()
    return keys,machines, indicators, current_values, range_A, range_B, set_value, contribution, uoms

# Get initial data for tables
defects, percentages, lag_percentages, lead_percentages = read_defect_data()
keys,machines, indicators, current_values, range_A, range_B, set_value, contribution, uoms = read_indicator_data()



# Create a DataFrame for indicator data for easier manipulation
indicator_df = pd.DataFrame({
    'Key': keys,
    'Indicator': indicators,
    'Current Value': current_values,
    'Range A': range_A,
    'Range B': range_B,
    'UOM': uoms,
    'Set_Value': set_value,
    'Contribution %': contribution,
    'Machine' : machines

})

# Define the layout for Primary page
page_2_layout = html.Div([
    html.H1("Leading Defect Indicators", style={'text-align': 'center', 'background-color': '#0047AB', 'color': 'white', 'padding': '10px'}),

    html.Div([
        # Left half: Table 1 and Table 2
        html.Div([
            # Table 1: Defects
            html.Div([
                html.H2("Defects", style={'text-align': 'center'}),
                dash_table.DataTable(
                    id='primary-table1',  # Updated ID
                    columns=[{'name': 'Defect', 'id': 'defect'}, 
                             {'name': 'Percentage Contribution', 'id': 'percentage'},
                             {'name': 'Lag Percentage', 'id': 'lag_percentage'},
                             {'name': 'Lead Percentage', 'id': 'lead_percentage'}],
                    data=[{'defect': defect, 'percentage': percentage, 'lag_percentage': lag, 'lead_percentage': lead} for defect, percentage, lag, lead in zip(defects, percentages, lag_percentages, lead_percentages)],
                    row_selectable='single',  # Allow single row selection
                    selected_rows=[0],  # Default selection
                    style_table={'width': '90%', 'margin': 'auto'},
                    style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
                    style_cell={'text-align': 'center', 'padding': '5px'},
                    style_data={'whiteSpace': 'normal', 'height': 'auto'},
                    css=[{
                        'selector': '.dash-table-container',
                        'rule': 'font-family: Arial, sans-serif; font-size: 14px;'
                    }]
                ),
                dcc.Interval(
                    id='primary-interval-table1',  # Updated ID
                    interval=5*1000,  # Update every 5 seconds
                    n_intervals=0
                )
            ], style={'margin-bottom': '20px'}),
            
            # Table 2: Machine Selector
            html.Div([
                html.H2("Machines", style={'text-align': 'center'}),
                dash_table.DataTable(
                    id='primary-table2',  # Updated ID
                    columns=[{'name': 'Machine', 'id': 'Machine'}],
                    data=[{'Machine': f'Packing Machine {i}'} for i in range(1, 7)],
                    row_selectable='single',  # Allow single row selection
                    selected_rows=[0],  # Default selection
                    style_table={'width': '90%', 'margin': 'auto'},
                    style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
                    style_cell={'text-align': 'center', 'padding': '5px'},
                    style_data={'whiteSpace': 'normal', 'height': 'auto'},
                    css=[{
                        'selector': '.dash-table-container',
                        'rule': 'font-family: Arial, sans-serif; font-size: 14px;'
                    }]
                ),
                dcc.Interval(
                    id='primary-interval-table2',  # Updated ID
                    interval=5*1000,  # Update every 5 seconds
                    n_intervals=0
                )
            ], style={'margin-bottom': '20px'})
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # Right half: Table 3
        html.Div([
            html.H2("Indicators", style={'text-align': 'center'}),
            dash_table.DataTable(
                id='primary-table3',  # Updated ID
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
                style_cell={'text-align': 'center', 'padding': '5px'},
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                css=[{
                    'selector': '.dash-table-container',
                    'rule': 'font-family: Arial, sans-serif; font-size: 14px;'
                }]
            ),
            dcc.Interval(
                id='primary-interval-table3',  # Updated ID
                interval=5*1000,  # Update every 5 seconds
                n_intervals=0
            )
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'padding': '20px'})
])

# Function to register callbacks
def register_callbacks(app):
    @app.callback(
        [Output('primary-table1', 'data'),  # Updated ID
         Output('primary-table2', 'data'),  # Updated ID
         Output('primary-table3', 'data')],  # Updated ID
        [Input('primary-interval-table1', 'n_intervals'),  # Updated ID
         Input('primary-interval-table2', 'n_intervals'),  # Updated ID
         Input('primary-interval-table3', 'n_intervals'),  # Updated ID
         Input('primary-table1', 'selected_rows'),  # Updated ID
         Input('primary-table2', 'selected_rows')]  # Updated ID
    )
    def update_tables(n1, n2, n3, selected_defect_rows, selected_machine_rows):
        # Ensure there's data in defects and machines
        defects, percentages, lag_percentages, lead_percentages = read_defect_data()
        machines = [{'Machine': f'Packing Machine {i}'} for i in range(1, 7)]
        
        # Handle default selections
        selected_defect = defects[selected_defect_rows[0]] if selected_defect_rows else defects[0]
        selected_machine = f'Packing Machine {selected_machine_rows[0] + 1}' if selected_machine_rows else 'Packing Machine 1'
        
        # Update Table 1
        table1_data = [{'defect': defect, 'percentage': percentage, 'lag_percentage': lag, 'lead_percentage': lead}
                       for defect, percentage, lag, lead in zip(defects, percentages, lag_percentages, lead_percentages)]
        
        # Update Table 2
        table2_data = machines
        
        # Update Table 3 based on selected defect and machine
        filtered_df = indicator_df[(indicator_df['Key'] == selected_defect) & (indicator_df['Machine'] == selected_machine)]
        table3_data = filtered_df[['Indicator', 'Current Value', 'Range A', 'Range B', 'UOM', 'Set_Value', 'Contribution %']].to_dict('records')
        
        return table1_data, table2_data, table3_data






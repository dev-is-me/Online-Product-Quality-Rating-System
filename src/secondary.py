# import pandas as pd
# from dash import dcc, html, dash_table
# from dash.dependencies import Input, Output

# # Path to the Excel file
# from directory import directory_Calc
# excel_path = f"{directory_Calc}/Calc_Worksheet.xlsx"

# # Function to read defect data from Sheet 3
# def read_defect_data():
#     df = pd.read_excel(excel_path, sheet_name='Sheet3')
#     secondary_df = df[df.iloc[:, 0] == 'Secondary']  # Filter rows where the first column (key) is 'Secondary'
#     defects = secondary_df.iloc[:, 1].tolist()     # Get the second column as the list of defects
#     percentages = secondary_df.iloc[:, 2].tolist() # Get the third column as the list of percentages
#     percentages = [round(p, 2) for p in percentages]
#     return defects, percentages

# # Function to read indicator data from Sheet 6
# def read_indicator_data():
#     df = pd.read_excel(excel_path, sheet_name='Sheet6')
#     keys = df.iloc[:, 0].tolist()
#     machines = df.iloc[:, 1].tolist()
#     indicators = df.iloc[:, 2].tolist()
#     current_values = df.iloc[:, 3].tolist()
#     ranges = df.iloc[:, 4].tolist()
#     uoms = df.iloc[:, 5].tolist()
#     set_value = df.iloc[:, 6].tolist()
#     contribution = df.iloc[:, 10].tolist()
#     contribution = [round(c, 3) for c in contribution]
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

# # Define the layout for Secondary page
# page_3_layout = html.Div([
#     html.H1("Leading Defect Indicators", style={'text-align': 'center', 'background-color': '#0047AB', 'color': 'white', 'padding': '10px'}),

#     html.Div([
#         # Left side: Table 1 and Table 2 stacked vertically
#         html.Div([
#             # Table 1: Defects
#             html.Div([
#                 html.H2("Defects", style={'text-align': 'center'}),
#                 dash_table.DataTable(
#                     id='secondary-table1',
#                     columns=[{'name': 'Defect', 'id': 'defect'}, {'name': 'Percentage Contribution', 'id': 'percentage'}],
#                     data=[{'defect': defect, 'percentage': percentage} for defect, percentage in zip(defects, percentages)],
#                     row_selectable='single',  # Allow single row selection
#                     selected_rows=[0],  # Default selection
#                     style_table={'width': '90%', 'margin': 'auto'},
#                     style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
#                     style_cell={'text-align': 'center'}
#                 ),
#                 dcc.Interval(
#                     id='secondary-interval-table1',
#                     interval=5*1000,  # Update every 5 seconds
#                     n_intervals=0
#                 )
#             ], style={'width': '100%', 'padding': '10px'}),
            
#             # Table 2: Indicators
#             html.Div([
#                 html.H2("Indicators", style={'text-align': 'center'}),
#                 dash_table.DataTable(
#                     id='secondary-table2',
#                     columns=[{'name': 'Machine', 'id': 'Machine'},  # Updated column
#                              {'name': 'Indicator', 'id': 'Indicator'},
#                              {'name': 'Current Value', 'id': 'Current Value'},
#                              {'name': 'Range', 'id': 'Range'},
#                              {'name': 'UOM', 'id': 'UOM'},
#                              {'name': 'Set_Value', 'id': 'Set_Value'},
#                              {'name': 'Contribution %', 'id': 'Contribution %'}],
#                     data=[],  # Empty data initially
#                     row_selectable='single',  # Allow single row selection
#                     selected_rows=[0],  # Default selection
#                     style_table={'width': '90%', 'margin': 'auto'},
#                     style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
#                     style_cell={'text-align': 'center'}
#                 ),
#                 dcc.Interval(
#                     id='secondary-interval-table2',
#                     interval=5*1000,  # Update every 5 seconds
#                     n_intervals=0
#                 )
#             ], style={'width': '100%', 'padding': '10px'})
#         ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
#         # Right side: Table 3
#         html.Div([
#             html.H2("Selected Data", style={'text-align': 'center'}),
#             dash_table.DataTable(
#                 id='secondary-table3',
#                 columns=[{'name': col, 'id': col} for col in indicator_df.columns],
#                 data=[],  # Empty data initially
#                 style_table={'width': '90%', 'margin': 'auto'},
#                 style_header={'backgroundColor': '#0047AB', 'color': 'white', 'text-align': 'center'},
#                 style_cell={'text-align': 'center'}
#             ),
#             dcc.Interval(
#                 id='secondary-interval-table3',
#                 interval=5*1000,  # Update every 5 seconds
#                 n_intervals=0
#             )
#         ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'})
#     ], style={'text-align': 'center', 'display': 'flex', 'justify-content': 'space-around'})
# ])

# # Function to register callbacks
# def register_callbacks(app):
#     @app.callback(
#         [Output('secondary-table1', 'data'),
#          Output('secondary-table2', 'data'),
#          Output('secondary-table3', 'data')],
#         [Input('secondary-interval-table1', 'n_intervals'),
#          Input('secondary-interval-table2', 'n_intervals'),
#          Input('secondary-interval-table3', 'n_intervals'),
#          Input('secondary-table1', 'selected_rows'),
#          Input('secondary-table2', 'selected_rows')]
#     )
#     def update_tables(n1, n2, n3, selected_rows1, selected_rows2):
#         # Update Table 1
#         defects, percentages = read_defect_data()
#         table1_data = [{'defect': defect, 'percentage': percentage} for defect, percentage in zip(defects, percentages)]

#         # Update Table 2 based on selected row in Table 1
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

#         if selected_rows1 is not None and len(selected_rows1) > 0:
#             selected_defect = defects[selected_rows1[0]]
#         else:
#             selected_defect = defects[0]

#         filtered_df = indicator_df[indicator_df['Key'] == selected_defect]
#         table2_data = filtered_df[['Machine', 'Indicator', 'Current Value', 'Range', 'UOM', 'Set_Value', 'Contribution %']].to_dict('records')

#         # Update Table 3 based on selected row in Table 2
#         if selected_rows2 is not None and len(selected_rows2) > 0:
#             selected_machine = filtered_df['Machine'].iloc[selected_rows2[0]]
#         else:
#             selected_machine = filtered_df['Machine'].iloc[0]

#         final_filtered_df = filtered_df[filtered_df['Machine'] == selected_machine]
#         table3_data = final_filtered_df.to_dict('records')

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
    secondary_df = df[df.iloc[:, 0] == 'Secondary']  # Filter rows where the first column (key) is 'Secondary'
    defects = secondary_df.iloc[:, 1].tolist()       # Get the second column as the list of defects
    percentages = secondary_df.iloc[:, 2].tolist()   # Get the third column as the list of percentages
    lag_percentages = secondary_df.iloc[:, 3].tolist()
    lead_percentages = secondary_df.iloc[:, 4].tolist()
    percentages = [round(p, 2) for p in percentages]
    lag_percentages = [round(p, 2) for p in lag_percentages]
    lead_percentages = [round(p, 2) for p in lead_percentages]
    return defects, percentages, lag_percentages, lead_percentages


# Function to read indicator data from Sheet 6
def read_indicator_data():
    df = pd.read_excel(excel_path, sheet_name='Sheet6')
    keys = df.iloc[:, 0].tolist()
    lines = df.iloc[:, 1].tolist()
    indicators = df.iloc[:, 2].tolist()
    current_values = df.iloc[:, 3].tolist()
    range_A = df.iloc[:, 5].tolist()
    range_B = df.iloc[:, 8].tolist()
    uoms = df.iloc[:, 12].tolist()
    set_value = df.iloc[:, 6].tolist()
    contribution = df.iloc[:, 11].tolist()
    contribution = [round(c, 2) for c in contribution]
    return keys, lines, indicators, current_values, range_A,range_B, uoms, set_value, contribution

# Get initial data for tables
defects, percentages, lag_percentages, lead_percentages = read_defect_data()
keys, lines, indicators, current_values, range_A,range_B, uoms, set_value, contribution = read_indicator_data()

# Create a DataFrame for indicator data for easier manipulation
indicator_df = pd.DataFrame({
    'Key': keys,
    'Line': lines,
    'Indicator': indicators,
    'Current Value': current_values,
    'Range A': range_A,
    'Range B': range_B,
    'UOM': uoms,
    'Set_Value': set_value,
    'Contribution %': contribution
})

page_3_layout = html.Div([
    html.H1("Leading Defect Indicators", style={'text-align': 'center', 'background-color': '#0047AB', 'color': 'white', 'padding': '10px'}),

    html.Div([
        # Left half: Table 1 and Table 2
        html.Div([
            # Table 1: Defects
            html.Div([
                html.H2("Defects", style={'text-align': 'center'}),
                dash_table.DataTable(
                    id='secondary-table1',  # Updated ID
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
                    id='secondary-interval-table1',  # Updated ID
                    interval=5*1000,  # Update every 5 seconds
                    n_intervals=0
                )
            ], style={'margin-bottom': '20px'}),
            
            # Table 2: Line Selector
            html.Div([
                html.H2("Lines", style={'text-align': 'center'}),
                dash_table.DataTable(
                    id='secondary-table2',
                    columns=[{'name': 'Line', 'id': 'Line'}],
                    data=[{'Line': f'Line {i}'} for i in range(1, 7)],
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
                    id='secondary-interval-table2',
                    interval=5*1000,  # Update every 5 seconds
                    n_intervals=0
                )
            ], style={'margin-bottom': '20px'})
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # Right half: Table 3
        html.Div([
            html.H2("Indicators", style={'text-align': 'center'}),
            dash_table.DataTable(
                id='secondary-table3',  # Updated ID
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
                id='secondary-interval-table3',  # Updated ID
                interval=5*1000,  # Update every 5 seconds
                n_intervals=0
            )
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'padding': '20px'})
])

# Function to register callbacks
def register_callbacks(app):
    @app.callback(
        [Output('secondary-table1', 'data'),
         Output('secondary-table2', 'data'),
         Output('secondary-table3', 'data')],
        [Input('secondary-interval-table1', 'n_intervals'),
         Input('secondary-interval-table2', 'n_intervals'),
         Input('secondary-interval-table3', 'n_intervals'),
         Input('secondary-table1', 'selected_rows'),
         Input('secondary-table2', 'selected_rows')]
    )
    def update_tables(n1, n2, n3, selected_defect_rows, selected_line_rows):
        # Ensure there's data in defects and lines
        defects, percentages, lag_percentages, lead_percentages = read_defect_data()
        lines = [{'Line': f'Line {i}'} for i in range(1, 7)]
        
        # Handle default selections
        selected_defect = defects[selected_defect_rows[0]] if selected_defect_rows else defects[0]
        selected_line = f'Line {selected_line_rows[0] + 1}' if selected_line_rows else 'Line 1'
        
        # Update Table 1
        table1_data = [{'defect': defect, 'percentage': percentage, 'lag_percentage': lag, 'lead_percentage': lead}
                       for defect, percentage, lag, lead in zip(defects, percentages, lag_percentages, lead_percentages)]
        
        # Update Table 2
        table2_data = lines
        
        # Update Table 3 based on selected defect and line
        filtered_df = indicator_df[(indicator_df['Key'] == selected_defect) & (indicator_df['Line'] == selected_line)]
        table3_data = filtered_df[['Indicator', 'Current Value', 'Range A', 'Range B', 'UOM', 'Set_Value', 'Contribution %']].to_dict('records')
        
        return table1_data, table2_data, table3_data




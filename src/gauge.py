# import plotly.graph_objects as go

# # Common function to create gauge figures
# def create_gauge(Score):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number+delta",
#         value=Score,
#         number={'suffix': ' %'},
#         gauge={
#             'axis': {'range': [0, 100]},
#             'bar': {'color': "black", 'thickness': 0.1},
#             'steps': [
#                 {'range': [0, 33.33], 'color': "red"},
#                 {'range': [33.33, 66.67], 'color': "yellow"},
#                 {'range': [66.67, 100], 'color': "green"}
#             ],
#             'threshold': {
#                 'line': {'color': "black", 'width': 4},
#                 'thickness': 0.75,
#                 'value': Score
#             }
#         }
#     ))

#     fig.update_layout(
#        font=dict(size=18)
#     )
    
#     return fig

# # create_gauge(100)


import plotly.graph_objects as go
from datetime import datetime

# Common function to create gauge figures
def create_gauge(Score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=Score,
        number={'suffix': ' %'},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black", 'thickness': 0.1},
            'steps': [
                {'range': [0, 33.33], 'color': "red"},
                {'range': [33.33, 66.67], 'color': "yellow"},
                {'range': [66.67, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': Score
            }
        }
    ))

    fig.update_layout(
       font=dict(size=18),
       annotations=[
           dict(
               x=0.5,
               y=-0.2,
               xref='paper',
               yref='paper',
               showarrow=False,
               text=f"Last Updated: {datetime.now().strftime('%H:%M:%S, %d %b %Y')}",
               font=dict(size=14)
           )
       ]
    )
    
    return fig


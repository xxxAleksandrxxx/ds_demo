from dash import Dash, dcc, html, Input, Output, callback
# import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

# import os

# my_dir = os.getcwd()
# print(my_dir)
# print()
# my_files = os.listdir(my_dir)
# print(my_files)
# print(os.getcwd())
# print()
# print()
# with open(my_files[0], 'r') as f:
#     print(f.readline())

# # url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
file = 'data.csv'
# file = 'test.txt'
# with open(file) as f:
#     print(f.readline())

df = pd.read_csv(file)


color ='#503D36'
font_size = 24
my_font = 'Arial'

app = Dash(__name__)
app.layout = html.Div([
    html.H1(
        'Automobile Sales Statistics Dashboard',
        style={
            'textAlign':'center',
            'color':'#503D36',
            'font-size':24,
            'font-family':my_font
        }
    ),
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label':'Yearly Statistics', 'value':'Yearly Statistics'},
            {'label':'Recession Period Statistics', 'value':'Recession Period Statistics'}
        ],
        placeholder='Select a report type',
        style={
            'width':'80%',
            'font-size':20,
            'font-family':my_font,
            'text-align-last':'center',
        }
    ),
    dcc.Dropdown(
        id='select-year',
        options=[
            {'label':i, 'value':i} for i in range(1980, 2024)
        ],
        placeholder='Select a year',
        disabled=False,
        style={
            'width':'80%',
            'font-size':20,
            'text-align-last':'center',
            'font-family':my_font
        }
    ),
    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={
                'display':'flex',
                'font-family':my_font
            }
        )
    ])
])


@app.callback(
    [
        Output(component_id='select-year', component_property='disabled'),
        Output(component_id='select-year', component_property='value')
    ],
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return [False, 0]
    else:
        return [True, 0]


@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'),
        Input(component_id='select-year', component_property='value'),
    ]
)
def update_output_container(selected_stat, selected_year=1980): #=1980):
    if selected_stat == 'Recession Period Statistics':
        recession_data = df[df['Recession'] == 1]

        # chart 1
        df_as = recession_data.groupby(['Year'])['Automobile_Sales'].mean().reset_index()
        fig_1 = px.line(
            data_frame=df_as,
            x='Year',
            y='Automobile_Sales',
            title='Automobile sales over Recession Period'
        )
        fig_1.update_layout(yaxis_title='Automobile Sales')
        R_chart_1 = dcc.Graph(
            figure=fig_1, 
            config={"displayModeBar":False}
        )

        # chart 2
        df_at = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig_2 = px.bar(
            data_frame=df_at,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title='Automobile sales over Recession Period by car types'
        )
        fig_2.update_layout(
            xaxis_title=None, #'Vehicle Type',
            yaxis_title='Automobile Sales'
        )
        R_chart_2 = dcc.Graph(
            figure=fig_2,
            config={"displayModeBar":False}
        )

        # chart 3
        df_ve = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig_3 = px.pie(
            data_frame = df_ve,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title='Total expenditure share by vehicle type'
        )
        R_chart_3 = dcc.Graph(
            figure=fig_3,
            config={"displayModeBar":False}
        )

        # chart 4
        df_uvs = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].sum().reset_index()
        fig_4 = px.bar(
            data_frame=df_uvs,
            x='Vehicle_Type',
            y='Automobile_Sales',
            color='unemployment_rate',
            title='Effect of unemployment rate on vehicle type and sales'
        )
        fig_4.update_layout(
            xaxis_title=None,
            yaxis_title='Automobile Sales',
            coloraxis_colorbar={'title':'Rate'}
        )
        R_chart_4 = dcc.Graph(
            figure=fig_4,
            config={"displayModeBar":False}
        )
        # end
        return [
            html.Div(className='chart-item', children=[
                html.Div(children=R_chart_1),
                html.Div(children=R_chart_3)
            ]),
            html.Div(className='chart-item', children=[
                html.Div(children=R_chart_2),
                html.Div(children=R_chart_4)
            ])
        ]
    
        # return html.Div([R_chart_1])
    elif selected_year and selected_stat == 'Yearly Statistics':
        yearly_data = df[df['Year'] == selected_year]

        # chart 1
        df_ys = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        df_ys
        fig_21 = px.line(
            data_frame=df_ys,
            x='Year',
            y='Automobile_Sales',
            title='Yearly Automobile sales'
        )
        fig_21.update_layout(
            yaxis_title='Automobile Sales'
        )        
        Y_chart_1 = dcc.Graph(
            figure=fig_21,
            config={'displayModeBar':False}
        )

        # chart 2
        df_ms = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        fig_22 = px.line(
            data_frame=df_ms,
            x='Month',
            y='Automobile_Sales',
            title='Total Monthly Automobile sales',
        )
        fig_22.update_traces(line_color='palevioletred')
        fig_22.update_layout(
            yaxis_title='Automobile Sales'
        )
        Y_chart_2 = dcc.Graph(
            figure=fig_22,
            config={'displayModeBar':False}
        )
        
        # chart 3
        df_vs = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig_23 = px.bar(
            data_frame=df_vs,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title='Average number of vehicles sold during the given year'
        )
        fig_23.update_layout(
            xaxis_title=None,
            yaxis_title='Automobile Sales'
        )
        Y_chart_3 = dcc.Graph(
            figure=fig_23,
            config={'displayModeBar':False}
        )

        # chart 4
        df_ve = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig_24 = px.pie(
            data_frame=df_ve,
            names='Vehicle_Type',
            values='Advertising_Expenditure',
            title='Total Advertisement Expenditure for each vehicle'
        )
        Y_chart_4 = dcc.Graph(
            figure=fig_24,
            config={'displayModeBar':False}
        )

    return[
        html.Div(className='chart-item', children=[
            html.Div(children=Y_chart_1),
            html.Div(children=Y_chart_3)
        ]),
        html.Div(className='chart-item', children=[
            html.Div(children=Y_chart_2),
            html.Div(children=Y_chart_4)
        ])
    ]


if __name__ == '__main__':
    app.run(debug=False)
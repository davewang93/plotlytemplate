#dashboard framework for 2 x * grid
#template for different plot types - heatmap, line, bar, ohlc, scatter
#template for different filters - dropdown, filter
#template for crossfilter
#template for css

from numpy.core.fromnumeric import _trace_dispatcher
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

app = dash.Dash()


df1 = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig1 = px.bar(df1, x="Fruit", y="Amount", color="City", barmode="group", title="Graph1", )

fruit_list = []

for fruit in df1['Fruit'].unique():
    fruit_list.append({'label':fruit,'value':fruit})

default1 = [x['value'] for x in fruit_list]


df2 = px.data.medals_wide(indexed=True)

fig2 = px.imshow(df2, title='Heatmap Sample')

medals_list = [{'label': x, 'value': x}
                 for x in df2.columns]

default2 = df2.columns.tolist()


df3 = px.data.stocks()

fig3 = px.line(df3, x='date', y='GOOG', title='Line Sample')

startdate = min(df3['date'])

enddate = max(df3['date'])

fig3.update_xaxes(rangeslider_visible=True)

fig3.update_layout(
    plot_bgcolor='#70D3FF',
    paper_bgcolor='#70D3FF',
    font_color = 'white')


df4 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig4 = go.Figure(data=[go.Candlestick(
    x=df4['Date'],
    open=df4['AAPL.Open'], high=df4['AAPL.High'],
    low=df4['AAPL.Low'], close=df4['AAPL.Close'],
    increasing_line_color= 'red', decreasing_line_color= 'green'
)])

fig4.update_layout(
    title='OHLC Candle Sample',
    plot_bgcolor='#70D3FF',
    paper_bgcolor='#70D3FF',
    font_color = 'white')

app.layout = html.Div([ #big block\

    html.H1(children='DASHBOARD TEMPLATE'),


    html.Div([ #small block upper most

    dcc.Graph(
        id='graph1',
        figure=fig1
    ),

    dcc.Dropdown(id='fruit-picker', options=fruit_list, value = default1, multi=True, )
    ]
    , style={
        'width': '45%',
        'display': 'inline-block', 
        'padding':'1.5rem',
        'margin-left':'2.25rem',
        }),


    html.Div([ #small block upper most

    dcc.Graph(
        id="graph2",
        figure = fig2),

    dcc.Dropdown(id='medal-picker', options=medals_list, value = default2, multi=True, )
    ]
    ,style={
        'width': '45%', 
        'display': 'inline-block',
        'padding':'1.5rem',
        }),


    html.Div([ #small block upper most

    dcc.Graph(
        id='graph3',
        figure=fig3
    ),

    ]
    ,style={
        'width': '45%', 
        'display': 'inline-block',
        'padding':'1.5rem',
        'margin-left':'2.25rem',
        }),

    html.Div([ #small block upper most

    dcc.Graph(
        id='graph4',
        figure=fig4
    )
    ]
    ,style={
        'width': '45%', 
        'display': 'inline-block',
        'padding':'1.5rem',
        }),
],
# this styles the outermost Div:
style={'border':'2px red dotted'})

@app.callback(Output('graph1', 'figure'),
              [Input('fruit-picker', 'value')])

def update_figure(selected_fruit):
    #funcdf = df1[df1['Fruit'] == selected_fruit] - in ploty tut but it doesnt work in this case and i don't get it
    funcdf1 = df1[df1['Fruit'].isin(selected_fruit)]
    fig1 = px.bar(funcdf1,x="Fruit", y="Amount", color="City", barmode="group",title='Bar Sample' )

    fig1.update_layout(
        plot_bgcolor='#70D3FF',
        paper_bgcolor='#70D3FF',
        font_color = 'white')
    
    return fig1


@app.callback(Output('graph2', 'figure'),
              [Input('medal-picker', 'value')])

def update_figure(selected_medal):
    #funcdf = df1[df1['Fruit'] == selected_fruit] - in ploty tut but it doesnt work in this case and i don't get it
    fig2 = px.imshow(df2[selected_medal],title='Heatmap Sample')

    fig2.update_layout(
        plot_bgcolor='#70D3FF',
        paper_bgcolor='#70D3FF',
        font_color = 'white')

    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)
  
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


a = pd.read_pickle("WorkFreqYear.pkl")
b = a.groupby("Year")
df = a[["Year","Count","Alpha term"]]
df = df.sort_values(['Year', 'Count'], ascending=[True, False])
df['Count'] = df['Count'].astype(int)
df = pd.DataFrame(df.groupby(by=["Year", "Alpha term"])['Count'].sum())
df.reset_index(inplace=True)

def display_table(year):

    filtered_data = a[a.Year == year]

    fig = go.Figure(
        go.Table(
            header=dict(
                values=filtered_data.columns,
                align="left"
            ),
            cells=dict(
                values=[filtered_data[x].tolist() for x in filtered_data],
                align='left'
            )
        )
    )
    return fig

# create the Dash app
app = dash.Dash()
server = app.server

app.layout = html.Div(
    dcc.Tabs([
        dcc.Tab(label='Static', children=[
            html.H1(children='Significant Tokens from Inclusion Criteria'),
            dcc.Dropdown(id='BM-dropdown',
                         options=[{'label': x, 'value': x}
                                  for x in df.Year.unique()],
                         value='1999',
                         multi=False, clearable=False),
            dcc.Graph(id='bar-chart')
        ]),
        dcc.Tab(label='Animated', children=[
            html.H1(children='Significant Tokens from Inclusion Criteria'),
            dcc.Interval(
                id='graph-update',
                interval=1 * 1000
            ),
            dcc.Graph(id='bar-chart2')
        ]),
        dcc.Tab(label='Data', children=[
            html.H1(children='Significant Tokens from Inclusion Criteria'),
            dcc.Dropdown(id='BM-dropdown1',
                         options=[{'label': x, 'value': x}
                                  for x in df.Year.unique()],
                         value='1999',
                         multi=False, clearable=True),
            dcc.Graph(id='bar-chart1')
        ])
    ])

)


# set up the callback function
@app.callback(
    Output(component_id="bar-chart", component_property="figure"),
    [Input(component_id="BM-dropdown", component_property="value")],
)
def display_BM_composition(selected_BM):
    filtered_BM = df[df.Year == selected_BM]

    barchart = px.bar(
        data_frame=filtered_BM,
        x="Alpha term",
        y="Count",
        color="Alpha term",
        opacity=0.9,
        barmode='group',
        text='Count')

    return barchart


# set up the callback function
@app.callback(
    Output(component_id="bar-chart2", component_property="figure"),
    [Input(component_id="graph-update", component_property="interval")],
)
def display_BM_composition1(selected_BM):
    filtered_BM = df[df.Year == selected_BM]

    barchart = px.bar(df, x="Alpha term", y="Count", color="Alpha term",text='Count',
                      animation_frame="Year", range_y=[0, 550])
    barchart.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000

    return barchart


# set up the callback function
@app.callback(
    Output(component_id="bar-chart1", component_property="figure"),
    [Input(component_id="BM-dropdown1", component_property="value")],
)
def display_filtered_table(year):
    fig = display_table(year)
    return fig


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(host="0.0.0.0", port=8050, debug=True)
    #app.run_server(debug=True, use_reloader=False)
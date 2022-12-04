import pathlib
import matplotlib.pyplot as plt
from dash import Dash, html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.colors as colors
import pandas as pd
from shotchart_module import shot_chart,shot_chart_plotly,convert_seaborn_to_img


app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.SOLAR])
# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


# *********************************************************************************************************

shotperf = pd.read_csv('./data/player_performance_pressure.csv')
shotperf['AST_TO_SUM'] = shotperf['AST_SUM'] + shotperf['TO_SUM']
shotdata = pd.read_csv('./data/shotchart_data.csv')
axes_choices = shotperf.columns[1:]
# *********************************************************************************************************

alert = dbc.Alert("Please choose players from dropdown to avoid further disappointment!", color="danger",
                  dismissable=True),  # use dismissable or duration=5000 for alert to close in x milliseconds

# *********************************************************************************************************

nav_bar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink('Shooting performance of players',href='/',id='shot-perf-nav',active='exact')),
        dbc.NavItem(dbc.NavLink('Shooting trends',href='/will-to-shoot',id='will-to-shoot-nav',active='exact')),
        dbc.NavItem(dbc.NavLink('Assist and turnover trends',href='/ast-to-trends',id='ast-to-trends-nav',active='exact')),
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem('2 point field goals',href='/2-point-field-goal-performance-under-pressure',\
                                     id='pres-perf-2p-nav'),
                dbc.DropdownMenuItem('3 point field goals',href='/3-point-field-goal-performance-under-pressure',\
                                     id='pres-perf-3p-nav'),
                dbc.DropdownMenuItem('Free-throws',href='/free-throw-performance-under-pressure',\
                                     id='pres-perf-ft-nav')
            ],
            label='Performance under different pressure situations',
            nav=True
        ),
        dbc.NavItem(dbc.NavLink('Shot charts',href='/shot-charts',id='shot-charts-nav',active='exact')),
        dbc.NavItem(dbc.NavLink('Custom',href='/custom-scatter-plot',id='custom-nav',active='exact'))
    ],
    pills=True,
    justified=True
)

# *********************************************************************************************************

image_card_shot_perform = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players", className="card-title"),
                html.H6("Choose NBA players:", className="card-text"),
                html.Div(id="the_alert_nba", children=[]),
                dcc.Dropdown(id='player_chosen',
                             options=[{'label': d, "value": d} for d in shotperf["PLAYER_NAME"].unique()],
                             value=["LeBron James", "Kevin Durant", "Kobe Bryant",'Stephen Curry'], \
                             multi=True,
                             style={"color": "#000000"}),
                html.Hr(),
                dbc.Button(
                    "All players", id="all-players-bottom-target"
                )
            ]
        ),
    ],
    color="light",
)

graph_card_shot_perform = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players' shot performance in the first half of the 2015-2016 season",\
                        className="card-title",
                        style={"text-align": "center"}),

                dcc.Graph(id='nba_scatter_shot_perf', figure={}),
            ]
        ),
    ],
    color="light",
)

image_card_will_to_shoot = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players", className="card-title"),
                html.H6("Choose NBA players:", className="card-text"),
                html.Div(id="the_alert_nba", children=[]),
                dcc.Dropdown(id='player_chosen_wts',
                             options=[{'label': d, "value": d} for d in shotperf["PLAYER_NAME"].unique()],
                             value=["LeBron James", "Kevin Durant", "Kobe Bryant",'Stephen Curry'], \
                             multi=True,
                             style={"color": "#000000"}),
                html.Hr(),
                dbc.Button(
                    "All players", id="all-players-bottom-target_wts"
                )
            ]
        ),
    ],
    color="light",
)

graph_card_will_to_shoot = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players' willingness to shoot under pressure in the first half of the 2015-2016 season",\
                        className="card-title",
                        style={"text-align": "center"}),

                dcc.Graph(id='nba_scatter_will_to_shoot', figure={}),
            ]
        ),
    ],
    color="light",
)

image_card_ast_to_trend = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players", className="card-title"),
                html.H6("Choose NBA players:", className="card-text"),
                html.Div(id="the_alert_nba", children=[]),
                dcc.Dropdown(id='player_chosen_ast_to_trend',
                             options=[{'label': d, "value": d} for d in shotperf["PLAYER_NAME"].unique()],
                             value=["LeBron James", "Kevin Durant", "Kobe Bryant",'Stephen Curry'], \
                             multi=True,
                             style={"color": "#000000"}),
                html.Hr(),
                dbc.Button(
                    "All players", id="all-players-bottom-target_ast_to_trend"
                )
            ]
        ),
    ],
    color="light",
)

graph_card_ast_to_trend = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players' assist and turnover trends in the first half of the 2015-2016 season",\
                        className="card-title",
                        style={"text-align": "center"}),

                dcc.Graph(id='nba_scatter_ast_to_trend', figure={}),
            ]
        ),
    ],
    color="light",
)

image_card_pres_2 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players", className="card-title"),
                html.H6("Choose NBA players:", className="card-text"),
                html.Div(id="the_alert_nba", children=[]),
                dcc.Dropdown(id='player_chosen_pres_2',
                             options=[{'label': d, "value": d} for d in shotperf["PLAYER_NAME"].unique()],
                             value=["LeBron James", "Kevin Durant", "Kobe Bryant",'Stephen Curry'], \
                             multi=True,
                             style={"color": "#000000"}),
                html.Hr(),
                dbc.Button(
                    "All players", id="all-players-bottom-target_pres_2"
                )
            ]
        ),
    ],
    color="light",
)

graph_card_pres_2 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players' 2 point shot performances under pressure in the first half of the 2015-2016 season",\
                        className="card-title",
                        style={"text-align": "center"}),

                dcc.Graph(id='nba_scatter_pres_2', figure={}),
            ]
        ),
    ],
    color="light",
)


image_card_pres_3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players", className="card-title"),
                html.H6("Choose NBA players:", className="card-text"),
                html.Div(id="the_alert_nba", children=[]),
                dcc.Dropdown(id='player_chosen_pres_3',
                             options=[{'label': d, "value": d} for d in shotperf["PLAYER_NAME"].unique()],
                             value=["LeBron James", "Kevin Durant", "Kobe Bryant",'Stephen Curry'], \
                             multi=True,
                             style={"color": "#000000"}),
                html.Hr(),
                dbc.Button(
                    "All players", id="all-players-bottom-target_pres_3"
                )
            ]
        ),
    ],
    color="light",
)

graph_card_pres_3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players' 3 point shot performances under pressure in the first half of the 2015-2016 season",\
                        className="card-title",
                        style={"text-align": "center"}),

                dcc.Graph(id='nba_scatter_pres_3', figure={}),
            ]
        ),
    ],
    color="light",
)


image_card_pres_ft = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players", className="card-title"),
                html.H6("Choose NBA players:", className="card-text"),
                html.Div(id="the_alert_nba", children=[]),
                dcc.Dropdown(id='player_chosen_pres_ft',
                             options=[{'label': d, "value": d} for d in shotperf["PLAYER_NAME"].unique()],
                             value=["LeBron James", "Kevin Durant", "Kobe Bryant",'Stephen Curry'], \
                             multi=True,
                             style={"color": "#000000"}),
                html.Hr(),
                dbc.Button(
                    "All players", id="all-players-bottom-target_pres_ft"
                )
            ]
        ),
    ],
    color="light",
)

graph_card_pres_ft = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players' free-throw performances under pressure in the first half of the 2015-2016 season",\
                        className="card-title",
                        style={"text-align": "center"}),

                dcc.Graph(id='nba_scatter_pres_ft', figure={}),
            ]
        ),
    ],
    color="light",
)


image_card_shotchart = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players", className="card-title"),
                html.H6("Choose an NBA player:", className="card-text"),
                html.Div(id="the_alert_nba"),
                dcc.Dropdown(id='player_chosen_shotchart',
                             options=[{'label': d, "value": d} for d in shotperf["PLAYER_NAME"].unique()],
                             value="LeBron James", \
                             style={"color": "#000000"}),
                html.Hr(),
            ]
        ),
    ],
    color="light",
)

graph_card_shotchart = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players' shotcharts under pressure in the first half of the 2015-2016 season",\
                        className="card-title",
                        style={"text-align": "center"}),
                html.H5(id="nba_sc_pres_title"),
                dcc.Graph(id='nba_shotchart_sc_pres', figure={}),
                html.Hr(),
                html.H5(id="nba_sc_no_pres_title"),
                dcc.Graph(id='nba_shotchart_sc_no_pres', figure={}),
                html.Hr(),
                html.H5(id="nba_kde_pres_title"),
                html.Img(id='nba_shotchart_kde_pres',children=[]),
                html.Hr(),
                html.H5(id="nba_kde_no_pres_title"),
                html.Img(id='nba_shotchart_kde_no_pres', children=[]),
            ]
        ),
    ],
    color="light",
)
image_card_custom_axes = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Choose what the axes of the grapgh should be",className="card-title"),
                dbc.Row(
                    [
                        dbc.Col(html.H6("x axis:", className="card-text"),width=3),
                        dbc.Col(html.H6("y axis:", className="card-text"), width=3),
                        dbc.Col(html.H6("color:", className="card-text"), width=3),
                        dbc.Col(html.H6("size:", className="card-text"), width=3),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Dropdown(id="custom_x_axis",
                                     options=[{'label' : d, 'value' : d} for d in axes_choices],
                                     value="PERFORMANCE_2P",
                                     style={"color": "#000000"}), width=3),
                        dbc.Col(dcc.Dropdown(id="custom_y_axis",
                                     options=[{'label': d, 'value': d} for d in axes_choices],
                                     value="PERFORMANCE_3P",
                                     style={"color": "#000000"}), width=3),
                        dbc.Col(dcc.Dropdown(id="custom_color_axis",
                                     options=[{'label' : d, 'value' : d} for d in axes_choices],
                                     value="PERFORMANCE_FT",
                                     style={"color": "#000000"}), width=3),
                        dbc.Col(dcc.Dropdown(id="custom_size_axis",
                                     options=[{'label' : d, 'value' : d} for d in axes_choices],
                                     value="SHOTS_SUM",
                                     style={"color": "#000000"}), width=3),
                    ], justify="around"
                )
            ]
        )
    ], color="light", class_name="mb-3"
)



image_card_custom = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("NBA players", className="card-title"),
                html.H6("Choose NBA players:", className="card-text"),
                #html.Div(id="the_alert_nba", children=[]),
                dcc.Dropdown(id='player_chosen_custom',
                             options=[{'label': d, "value": d} for d in shotperf["PLAYER_NAME"].unique()],
                             value=["LeBron James", "Kevin Durant", "Kobe Bryant",'Stephen Curry'], \
                             multi=True,
                             style={"color": "#000000"}),
                html.Hr(),
                dbc.Button(
                    "All players", id="all-players-bottom-target_custom"
                )
            ]
        ),
    ],
    color="light",
)

graph_card_custom = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Assemble a scatterplot with the axes of your choice!",\
                        className="card-title",
                        style={"text-align": "center"}),

                dcc.Graph(id='nba_scatter_custom', figure={}),
            ]
        ),
    ],
    color="light",
)



content = html.Div(id='page_content',children=[],style={'padding':'2rem'})

# *********************************************************************************************************
app.layout = html.Div([
    dcc.Location(id='url'),
    nav_bar,
    content
    #dbc.Row([dbc.Col(image_card_shot_perform, width=4), dbc.Col(graph_card_shot_perform, width=8)], justify="around")
])


# *********************************************************************************************************

@app.callback(
    Output('page_content', 'children'),
    [Input('url','pathname')]
)
def render_page_content(pathname):
    if pathname=='/':
        return [dbc.Row([dbc.Col(image_card_shot_perform, width=4), dbc.Col(graph_card_shot_perform, width=8)], justify="around")]
    elif pathname=='/will-to-shoot':
        return [dbc.Row([dbc.Col(image_card_will_to_shoot, width=4), dbc.Col(graph_card_will_to_shoot, width=8)], justify="around")]
    elif pathname == '/ast-to-trends':
        return [dbc.Row([dbc.Col(image_card_ast_to_trend, width=4), dbc.Col(graph_card_ast_to_trend, width=8)], justify="around")]
    elif pathname == '/2-point-field-goal-performance-under-pressure':
        return [dbc.Row([dbc.Col(image_card_pres_2, width=4), dbc.Col(graph_card_pres_2, width=8)], justify="around")]
    elif pathname == '/3-point-field-goal-performance-under-pressure':
        return [dbc.Row([dbc.Col(image_card_pres_3, width=4), dbc.Col(graph_card_pres_3, width=8)], justify="around")]
    elif pathname == '/free-throw-performance-under-pressure':
        return [dbc.Row([dbc.Col(image_card_pres_ft, width=4), dbc.Col(graph_card_pres_ft, width=8)], justify="around")]
    elif pathname == '/shot-charts':
        return [dbc.Row([dbc.Col(image_card_shotchart, width=4), dbc.Col(graph_card_shotchart, width=8)], justify="around")]
    elif pathname == '/custom-scatter-plot':
        return [dbc.Row([image_card_custom_axes]), \
                dbc.Row([dbc.Col(image_card_custom,width=4),dbc.Col(graph_card_custom, width=8)], justify="around")]
    else:
        return dbc.Card(
            [
                html.H1('404: Not found', className='text-danger'),
                html.Hr(),
                html.P(f'The pathname {pathname} was not recognised...')
            ]
        )

@app.callback(
    [Output("nba_scatter_shot_perf", "figure"),
     Output("the_alert_nba", "children")],
    Input("player_chosen", "value")
)
def update_graph_card_nba(players):
    if len(players) == 0:
        return no_update, alert
    else:
        df_filtered = shotperf[shotperf["PLAYER_NAME"].isin(players)]

        fig = px.scatter(df_filtered, x='PERFORMANCE_2P', y='PERFORMANCE_3P', size='SHOTS_SUM', \
                         color='PERFORMANCE_FT',color_continuous_scale=colors.sequential.Bluered,\
                         color_continuous_midpoint=0, text='PLAYER_NAME', \
                         labels={'PERFORMANCE_2P': 'Player\'s 2 point shooting performance', \
                                 'PERFORMANCE_3P': 'Player\'s 3 point shooting performance',\
                                 'PERFORMANCE_FT': 'Player\'s free-throw shooting performance'})
        fig.add_hline(y=0, line_color='black')
        fig.add_vline(x=0, line_color='black')
        fig.update_layout(font=dict(size=10))
        fig.for_each_trace(lambda t: t.update(textfont_color='black',textfont_size=12))


        return fig, no_update

@app.callback(
    Output("nba_scatter_will_to_shoot", "figure"),
    Input("player_chosen_wts", "value")
)
def update_graph_card_will_to_shoot(players):
    if len(players) == 0:
        return no_update
    else:
        df_filtered = shotperf[shotperf["PLAYER_NAME"].isin(players)]

        fig = px.scatter(df_filtered, x='SHOTTREND_2P', y='SHOTTREND_3P', size='SHOTS_SUM',\
                         color='SHOTTREND_FT',color_continuous_scale=colors.sequential.Bluered,\
                         color_continuous_midpoint=0, text='PLAYER_NAME', \
                         labels={'SHOTTREND_2P': 'Player\'s 2 point shooting trend under pressure', \
                                 'SHOTTREND_3P': 'Player\'s 3 point shooting trend under pressure',\
                                 'SHOTTREND_FT': 'Player\'s free-throw shooting trend under pressure'})
        fig.add_hline(y=0, line_color='black')
        fig.add_vline(x=0, line_color='black')
        fig.update_layout(font=dict(size=10))
        fig.for_each_trace(lambda t: t.update(textfont_color='black',textfont_size=12 ))
        fig.update_traces(marker=dict(size=12,
                                      line=dict(width=1,
                                                color='black')),
                          selector=dict(mode='markers'))


        return fig

@app.callback(
    Output("nba_scatter_ast_to_trend", "figure"),
    Input("player_chosen_ast_to_trend", "value")
)
def update_graph_card_ast_to(players):
    if len(players) == 0:
        return no_update
    else:
        df_filtered = shotperf[shotperf["PLAYER_NAME"].isin(players)]
        #df_filtered = df_filtered[(df_filtered['AST_TREND'] > 0) & (df_filtered['TO_TREND'] > 0) & \
        #             (df_filtered['AST/TO_TREND'] > 0)]

        fig = px.scatter(df_filtered, x='AST_TREND', y='TO_TREND', size='AST_TO_SUM',\
                         color='AST/TO_TREND',color_continuous_scale=colors.sequential.Bluered,\
                         color_continuous_midpoint=0, text='PLAYER_NAME', \
                         labels={'AST_TREND': 'Assist trends under pressure', \
                                 'TO_TREND': 'Turnover trends under pressure',\
                                 'AST/TO_TREND': 'AST/TO trend under pressure'})
        fig.add_hline(y=0, line_color='black')
        fig.add_vline(x=0, line_color='black')
        fig.update_layout(font=dict(size=10))
        fig.for_each_trace(lambda t: t.update(textfont_color='black',textfont_size=12 ))
        fig.update_traces(marker=dict(size=12,
                                      line=dict(width=1,
                                                color='black')),
                          selector=dict(mode='markers'))


        return fig


@app.callback(
    Output("nba_scatter_pres_2", "figure"),
    Input("player_chosen_pres_2", "value")
)
def update_graph_card_pres_2(players):
    if len(players) == 0:
        return no_update
    else:
        df_filtered = shotperf[shotperf["PLAYER_NAME"].isin(players)]

        fig = px.scatter(df_filtered, x='PERFORMANCE_2P_DELTA_cat_1', y='PERFORMANCE_2P_DELTA_cat_2', \
                         size='SHOTS_SUM_PRES_2P',color='SHOTTREND_2P',color_continuous_scale=colors.sequential.Bluered,\
                         color_continuous_midpoint=0, text='PLAYER_NAME',\
                         labels={'PERFORMANCE_2P_DELTA_cat_1': 'PLayer\'s performance delta under pressure category 1', \
                                 'PERFORMANCE_2P_DELTA_cat_2': 'PLayer\'s performance delta under pressure category 2',\
                                 'SHOTTREND_2P': 'Player\'s 2 point shooting willingness under pressure'})
        fig.add_hline(y=0, line_color='black')
        fig.add_vline(x=0, line_color='black')
        fig.update_layout(font=dict(size=10),
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=0,
                              xanchor="right",
                              x=0
                          )
        )
        fig.for_each_trace(lambda t: t.update(textfont_color='black',textfont_size=10 ))
        fig.update_traces(marker=dict(size=12,
                                      line=dict(width=1,
                                                color='black')),
                          selector=dict(mode='markers'))

        return fig


@app.callback(
    Output("nba_scatter_pres_3", "figure"),
    Input("player_chosen_pres_3", "value")
)
def update_graph_card_pres_3(players):
    if len(players) == 0:
        return no_update
    else:
        df_filtered = shotperf[shotperf["PLAYER_NAME"].isin(players)]

        fig = px.scatter(df_filtered, x='PERFORMANCE_3P_DELTA_cat_1', y='PERFORMANCE_3P_DELTA_cat_2', \
                         size='SHOTS_SUM_PRES_3P',color='SHOTTREND_3P',color_continuous_scale=colors.sequential.Bluered,\
                         color_continuous_midpoint=0, text='PLAYER_NAME',\
                         labels={'PERFORMANCE_3P_DELTA_cat_1': 'Player\'s performance delta under pressure category 1', \
                                 'PERFORMANCE_3P_DELTA_cat_2': 'Player\'s performance delta under pressure category 2',\
                                 'SHOTTREND_3P': 'Player\'s 3 point shooting willingness under pressure'})
        fig.add_hline(y=0, line_color='black')
        fig.add_vline(x=0, line_color='black')
        fig.update_layout(font=dict(size=10),
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=0,
                              xanchor="right",
                              x=0
                          )
        )
        fig.for_each_trace(lambda t: t.update(textfont_color='black',textfont_size=10 ))
        fig.update_traces(marker=dict(size=12,
                                      line=dict(width=1,
                                                color='black')),
                          selector=dict(mode='markers'))

        return fig


@app.callback(
    Output("nba_scatter_pres_ft", "figure"),
    Input("player_chosen_pres_ft", "value")
)
def update_graph_card_pres_ft(players):
    if len(players) == 0:
        return no_update
    else:
        df_filtered = shotperf[shotperf["PLAYER_NAME"].isin(players)]

        fig = px.scatter(df_filtered, x='PERFORMANCE_FT_DELTA_cat_1', y='PERFORMANCE_FT_DELTA_cat_2', \
                         size='SHOTS_SUM_PRES_FT',color='SHOTTREND_FT',color_continuous_scale=colors.sequential.Bluered,\
                         color_continuous_midpoint=0, text='PLAYER_NAME',\
                         labels={'PERFORMANCE_FT_DELTA_cat_1': 'PLayer\'s performance delta under pressure category 1', \
                                 'PERFORMANCE_FT_DELTA_cat_2': 'PLayer\'s performance delta under pressure category 2',\
                                 'SHOTTREND_FT': 'Player\'s free-throw shooting willingness under pressure'})
        fig.add_hline(y=0, line_color='black')
        fig.add_vline(x=0, line_color='black')
        fig.update_layout(font=dict(size=10),
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=0,
                              xanchor="right",
                              x=0
                          )
        )
        fig.for_each_trace(lambda t: t.update(textfont_color='black',textfont_size=10 ))
        fig.update_traces(marker=dict(size=12,
                                      line=dict(width=1,
                                                color='black')),
                          selector=dict(mode='markers'))

        return fig


@app.callback(
    Output("nba_sc_pres_title","children"),
    Output("nba_shotchart_sc_pres", "figure"),
    Output("nba_sc_no_pres_title","children"),
    Output("nba_shotchart_sc_no_pres", "figure"),
    Output("nba_kde_pres_title","children"),
    Output("nba_shotchart_kde_pres", "src"),
    Output("nba_kde_no_pres_title", "children"),
    Output("nba_shotchart_kde_no_pres", "src"),
    Input("player_chosen_shotchart", "value")
)
def update_shotcharts(player):
    if len(player) == 0:
        return no_update,no_update,no_update,no_update,no_update,no_update,no_update,no_update
    else:
        ## filter data for player
        df_filtered = shotdata[shotdata['PLAYER_NAME']==player]
        ## sc_pres
        # title
        title_sc_pres = f"Shotchart of {player} under pressure"
        # add made shots
        fig_sc_pres = shot_chart_plotly(df_filtered[(df_filtered['high_pres'] == 1) & \
                                                    (df_filtered['SHOT_MADE_FLAG'] == 1)],\
                                          'LOC_X','LOC_Y', kind="scatter",name = "made")
        # add missed shots, with red color and x marker (also add title here)
        fig_sc_pres = shot_chart_plotly(df_filtered[(df_filtered['high_pres'] == 1) & \
                                            (df_filtered['SHOT_MADE_FLAG'] == 0)], \
                                        'LOC_X','LOC_Y',\
                                        kind="scatter",fig=fig_sc_pres,marker_symbol="x",
                                        name = "missed")
        ## sc_no_pres
        # title
        title_sc_no_pres = f"Shotchart of {player} under no pressure"
        # add made shots
        fig_sc_no_pres = shot_chart_plotly(df_filtered[(df_filtered['SHOT_MADE_FLAG'] == 1)] \
                                   , 'LOC_X', 'LOC_Y', kind='scatter',name="made")
        # add missed shots, with red color and x marker (also add title here)
        fig_sc_no_pres = shot_chart_plotly(df_filtered[(df_filtered['SHOT_MADE_FLAG'] == 0)] \
                                   , 'LOC_X', 'LOC_Y', kind='scatter', name="missed",\
                                           fig=fig_sc_no_pres,marker_symbol='x')

        cmap = plt.cm.gist_heat_r  # colormap for kde charts
        ## kde pres
        # title
        title_kde_pres = f"Shot selection heatmap of {player} under pressure"
        # figure
        fig_kde_pres, ax_kde_pres = plt.subplots()
        ax_kde_pres = shot_chart(df_filtered[(df_filtered['high_pres'] == 1)], 'LOC_X', 'LOC_Y',
                                 kind="kde",n_levels=30)#, cmap=cmap)
        fig_kde_pres = convert_seaborn_to_img(fig_kde_pres)

        ## kde_no_pres
        # title
        title_no_kde_pres = f"Shot selection heatmap of {player} under no pressure"
        # figure
        fig_kde_no_pres, ax_kde_no_pres = plt.subplots()
        ax_kde_no_pres = shot_chart(df_filtered[(df_filtered['high_pres'] == 0)], 'LOC_X', 'LOC_Y',
                                    kind="kde", n_levels=30)#, cmap=cmap)
        kde_no_pres = convert_seaborn_to_img(fig_kde_no_pres)

        return title_sc_pres,fig_sc_pres,title_sc_no_pres,fig_sc_no_pres,title_kde_pres,fig_kde_pres,title_no_kde_pres,kde_no_pres


@app.callback(
    Output("nba_scatter_custom", "figure"),
    Input("player_chosen_custom", "value"),
    Input("custom_x_axis", "value"),
    Input("custom_y_axis", "value"),
    Input("custom_color_axis", "value"),
    Input("custom_size_axis", "value")
)
def update_custom_grapgh(players, x_axes, y_axes, color, size):
    if len(players) == 0:
        return no_update
    else:
        df_filtered = shotperf[shotperf["PLAYER_NAME"].isin(players)]
        fig = px.scatter(df_filtered, x=x_axes, y=y_axes, \
                         size=size, color=color,
                         color_continuous_scale=colors.sequential.Bluered, \
                         color_continuous_midpoint=0, text='PLAYER_NAME', \
                         )
        fig.add_hline(y=0, line_color='black')
        fig.add_vline(x=0, line_color='black')
        fig.update_layout(font=dict(size=10),
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=0,
                              xanchor="right",
                              x=0
                          )
                          )
        fig.for_each_trace(lambda t: t.update(textfont_color='black', textfont_size=10))
        fig.update_traces(marker=dict(size=12,
                                      line=dict(width=1,
                                                color='black')),
                          selector=dict(mode='markers'))

        return fig


@app.callback(
    Output('player_chosen','value'),
    Input('all-players-bottom-target','n_clicks'), prevent_initial_call=True
)
def add_all_players_to_nba_card(click_n):
    if click_n:
        return shotperf['PLAYER_NAME'].unique()
    else:
        return no_update

@app.callback(
    Output('player_chosen_wts','value'),
    Input('all-players-bottom-target_wts','n_clicks'), prevent_initial_call=True
)
def add_all_players_to_nba_card(click_n):
    if click_n:
        return shotperf['PLAYER_NAME'].unique()
    else:
        return no_update

@app.callback(
    Output('player_chosen_ast_to_trend','value'),
    Input('all-players-bottom-target_ast_to_trend','n_clicks'), prevent_initial_call=True
)
def add_all_players_to_nba_card(click_n):
    if click_n:
        return shotperf['PLAYER_NAME'].unique()
    else:
        return no_update

@app.callback(
    Output('player_chosen_pres_2','value'),
    Input('all-players-bottom-target_pres_2','n_clicks'), prevent_initial_call=True
)
def add_all_players_to_nba_card(click_n):
    if click_n:
        return shotperf['PLAYER_NAME'].unique()
    else:
        return no_update

@app.callback(
    Output('player_chosen_pres_3','value'),
    Input('all-players-bottom-target_pres_3','n_clicks'), prevent_initial_call=True
)
def add_all_players_to_nba_card(click_n):
    if click_n:
        return shotperf['PLAYER_NAME'].unique()
    else:
        return no_update

@app.callback(
    Output('player_chosen_pres_ft','value'),
    Input('all-players-bottom-target_pres_ft','n_clicks'), prevent_initial_call=True
)
def add_all_players_to_nba_card(click_n):
    if click_n:
        return shotperf['PLAYER_NAME'].unique()
    else:
        return no_update

@app.callback(
    Output('player_chosen_custom','value'),
    Input('all-players-bottom-target_custom','n_clicks'), prevent_initial_call=True
)
def add_all_players_to_nba_card(click_n):
    if click_n:
        return shotperf['PLAYER_NAME'].unique()
    else:
        return no_update


if __name__ == "__main__":
    app.run_server()#debug=True)

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

path = 'data/'

emissions = pd.read_csv(path + "emissions_with_origin.csv")
productions = pd.read_csv(path + "productions.csv")
water = pd.read_csv(path + "water_use.csv")
global_emissions = pd.read_csv(path + "Global_Emissions.csv")
emissions_bar = pd.read_csv(path +'bar_plot_2.csv' )

df3 = pd.read_csv('data/productions.csv')
df3.columns = df3.columns.str.replace('Value', 'value')
df3 = df3.groupby(['Year', 'Origin'], as_index=False).sum()
df4 = df3.groupby(['Year'], as_index=False).sum()

top10 = emissions.sort_values("Total_emissions")[-8:]
top10_vegetal = emissions[emissions.Origin == 'Vegetal'].sort_values("Total_emissions")[-8:]
top8_animal = emissions[emissions.Origin == 'Animal'].sort_values("Total_emissions")[-8:]

top20 = emissions.sort_values("Total_emissions")[-8:]
top20_vegetal = emissions[emissions.Origin == 'Vegetal'].sort_values("Total_emissions")[-8:]
top20_animal = emissions[emissions.Origin == 'Animal'].sort_values("Total_emissions")[-8:]

radio_ani_veg = dbc.RadioItems(
    id='ani_veg',
    className='radio',
    options=[dict(label='Animal Products', value=0), dict(label='Vegan Products', value=1),
             dict(label='All Products', value=2)],
    value=2,
    inline=True
)

dict_ = {'Apples': 'Apples', 'Bananas': 'Bananas', 'Barley': 'Barley', 'Beet Sugar': 'Sugar beet',
         'Berries & Grapes': 'Berries & Grapes', 'Brassicas': 'Brassicas',
         'Cane Sugar': 'Sugar cane', 'Cassava': 'Cassava', 'Citrus Fruit': 'Citrus', 'Coffee': 'Coffee beans',
         'Groundnuts': 'Groundnuts', 'Maize': 'Maize', 'Nuts': 'Nuts',
         'Oatmeal': 'Oats', 'Olive Oil': 'Olives', 'Onions & Leeks': 'Onions & Leeks', 'Palm Oil': 'Oil palm fruit',
         'Peas': 'Peas', 'Potatoes': 'Potatoes', 'Rapeseed Oil': 'Rapeseed',
         'Rice': 'Rice', 'Root Vegetables': 'Roots and tubers', 'Soymilk': 'Soybeans',
         'Sunflower Oil': 'Sunflower seed', 'Tofu': 'Soybeans', 'Tomatoes': 'Tomatoes',
         'Wheat & Rye': 'Wheat & Rye', 'Dark Chocolate': 'Cocoa, beans', 'Milk': 'Milk', 'Eggs': 'Eggs',
         'Poultry Meat': 'Poultry Meat', 'Pig Meat': 'Pig Meat',
         'Seafood (farmed)': 'Seafood (farmed)', 'Cheese': 'Cheese', 'Lamb & Mutton': 'Lamb & Mutton',
         'Beef (beef herd)': 'Beef (beef herd)'}

options_veg = [dict(label=key, value=dict_[key]) for key in top20_vegetal['Food product'].tolist()[::-1] if
               key in dict_.keys()]
options_an = [dict(label=val, value=val) for val in top8_animal["Food product"].tolist()[::-1]]
options_total = [dict(label=key, value=dict_[key]) for key in top20['Food product'].tolist()[::-1] if
                 key in dict_.keys()]

bar_colors = ['#B22222', '#2E8B57']
bar_options = [top8_animal, top10_vegetal, top10]
drop_map = dcc.Dropdown(
    id='drop_map',
    clearable=False,
    searchable=False,
    style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#5CACEE'}  # בחירת מוצר גבולות
)

drop_continent = dcc.Dropdown(
    id='drop_continent',
    clearable=False,
    searchable=False,
    options=[{'label': 'World', 'value': 'world'},
             {'label': 'Europe', 'value': 'europe'},
             {'label': 'Asia', 'value': 'asia'},
             {'label': 'Africa', 'value': 'africa'},
             {'label': 'North america', 'value': 'north america'},
             {'label': 'South america', 'value': 'south america'}],
    value='world',
    style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#5CACEE'}
)

slider_map = daq.Slider(
    id='slider_map',
    handleLabel={"showCurrentValue": True, "label": "Year"},
    marks={str(i): str(i) for i in [1990, 1995, 2000, 2005, 2010, 2015, 2020]},
    min=1990,
    size=300,
    color='#4B9072'
)

fig_water = px.sunburst(water, path=['Origin', 'Category', 'Product'], values='Water Used', color='Category',
                        color_discrete_sequence=px.colors.sequential.haline_r).update_traces(
    hovertemplate='%{label}<br>' + 'Water Used: %{value} L')

fig_water = fig_water.update_layout({'margin': dict(t=0, l=0, r=0, b=10),
                                     'paper_bgcolor': '#F9F9F8',
                                     'font_color': '#363535'
                                     })

fig_gemissions = px.sunburst(global_emissions, path=['Emissions', 'Group', 'Subgroup'],
                             values='Percentage of food emissions',
                             color='Group', color_discrete_sequence=px.colors.sequential.Peach_r).update_traces(
    hovertemplate='%{label}<br>' + 'Global Emissions: %{value}%', textinfo="label + percent entry")

fig_gemissions = fig_gemissions.update_layout({'margin': dict(t=0, l=0, r=0, b=10),
                                               'paper_bgcolor': '#F9F9F8',
                                               'font_color': '#363535'})

fig2 = go.Figure(
    data=go.Scatter(x=df3['Year'], y=df3['value'])
)

fig3 = go.Figure(layout=dict(height=300, font_color='#363535', paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                             margin_pad=20))

# ------------------------------------------------------ APP ------------------------------------------------------

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([


        html.H1(children='Information Visualization Project'),

        html.Label(
            'Food products that have the biggest impact on environment, whose productions emit more greenhouse gases.',
            style={'color': 'rgb(242, 235, 233)'}),

            html.Img(src=app.get_asset_url('bgu.png'),
                 style={'position': 'relative', 'width': '5%', 'left': '-40px', 'top': '-118px'}),
    ], className='side_bar'),

    html.Div([
        html.Div([
            html.Div([
                html.Label("Choose the Product's Origin:"),
                html.Br(),
                html.Br(),
                radio_ani_veg
            ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px', }),

            html.Div([
                html.Div([

                    html.Div([
                        html.Label(id='title_bar'),
                        html.Br(),

                        html.Label('  (kg CO2 per kg of product)',style={'padding-bottom': '200px','font-size': '17px'}),
                        html.Br(),

                        html.Br(),html.Img(src=app.get_asset_url('len.png'),style={'width': '25%','left': '-40px', 'top': '-118px'}),

                        dcc.Graph(id='bar_fig'),
                        html.Div([
                            html.P(id='comment')
                        ], className='box_comment'),
                    ], className='box', style={'padding-bottom': '15px'}),

                    html.Div([

                        html.Img(src=app.get_asset_url('blue3.png'),
                                 style={'width': '100%', 'position': 'relative', 'opacity': '100%',
                                        'border-radius': '75'
                                                         'px','height':'350px'}),
                    ]),
                    html.Div([
                        html.Br(),
                        html.Label(id='title_line'),

                        dcc.Graph(id='fig1', figure=fig2)
                    ], className='box',
                        style={'width': '90%', 'position': 'relative', 'padding-top': '20px', 'padding-bottom': '20px',
                               'border-radius': '75px'}),

                ], style={'width': '40%'}),

                html.Div([
                    html.Div([
                        html.Label(id='choose_product', style={'margin': '10px', 'font-size': '20px'}),
                        drop_map,
                        ], className='box'),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Br(), html.Br(), html.Br(), html.Br(),
                                html.Div([

                                    html.Label(id='title_map', style={'font-size': '20px'}),

                                    html.Br(),
                                ], style={'width': '80%'}),
                                html.Div([

                                ], style={'width': '50%'}),
                                html.Div([
                                    drop_continent,
                                    html.Br(),
                                    html.Br(), html.Br(), html.Br(), html.Br()
                                ], style={'width': '50%'}),
                            ], className='row'),

                            dcc.Graph(id='map', style={'position': 'relative', 'top': '-50px'}),

                            html.Div([
                                slider_map
                            ], style={'margin-left': '30%', 'position': 'relative', 'top': '-38px'}),

                        ], className='box', style={'padding-bottom': '0px'}),
                    ]),
                    html.Div([dcc.Graph(id='graph2', figure=fig3),
                        html.Div([
                            html.Label('These represent greenhouse gas emissions per kg of food product across different stages in the lifecycle of food production.'),
                        ], className='box_comment')
                              ], className='box'),
                    html.Div([

                        html.Img(src=app.get_asset_url('farm2.png'),
                                 style={'width': '80%', 'position': 'relative', 'opacity': '90%',
                                        'border-radius': '75px', 'height': '190px','left':'80px'}),
                    ]),

                ], style={'width': '60%'}),
            ], className='row'),

            html.Div([
                html.Div([
                    html.P(['Ⓒ Final Information Visualization Project by', html.Br(),
                            html.A('Natalie Morad', href='https://www.linkedin.com/in/natalie-morad-44881620b',
                                   target='_blank'), ', ',
                            html.A('Bar Avraham',
                                   href='https://www.linkedin.com/in/bar-avraham-4475b1218/', target='_blank')],
                           style={'font-size': '17px'  ,'text-align': 'center'}),
                ], style={'width': '100%'}),

            ], className='side_bar', style={'display': 'flex'}),
        ]
            , className='main'),
    ]),
])


# ------------------------------------------------------ Callbacks ---------------------------------------------------

@app.callback(
    [
        Output('title_bar', 'children'),
        Output('bar_fig', 'figure'),
        Output('comment', 'children'),
        Output('drop_map', 'options'),
        Output('drop_map', 'value'),
        Output('choose_product', 'children')
    ],
    [
        Input('ani_veg', 'value')
    ],
)
def bar_chart(top10_select):
    ################## Top10 Plot ##################
    title = '1. Food products \n that cause the greatest emissions of CO2'
    df = bar_options[top10_select]

    if top10_select == 2:
        bar_fig = dict(type='bar',
                       y=df.Total_emissions,
                       x=df["Food product"],
                       orientation='v',
                       marker_color=['#B22222' if x == 'Animal' else '#2E8B57' for x in df.Origin])
        fig=go.Figure(data=bar_fig,
                  layout=dict(height=300, font_color='#363535', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                              margin_pad=20), layout_yaxis_range=[0, 60])

    else:

        bar_fig = dict(type='bar',
                       y=df.Total_emissions,
                       x=df["Food product"],
                       orientation='v',
                       marker_color=bar_colors[top10_select])
        fig=go.Figure(data=bar_fig,
                  layout=dict( height=300, font_color='#363535', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                              margin_pad=20), layout_yaxis_range=[0, 60])

    ################## Dropdown Bar ##################comments
    if top10_select == 0:
        options_return = options_an
        product_chosen = "2. Choose an animal product:"
        comment = ["Each kilogram of beef produces almost 60 kg of CO2!",
                   html.Br()]
    elif top10_select == 1:
        options_return = options_veg
        product_chosen = "2. Choose a vegan product:"
        comment = ["Dark chocolate is the vegan product with the most CO2 emissions with almost 20 kg of CO2.",
                   html.Br()]
    else:
        options_return = options_total
        product_chosen = "2. Choose an animal or vegan product:"
        comment = "Beef (top1 animal-based emitter) produces around 3 times more emissions than dark chocolate (top1 vegan-based emitter)."

    return title, \
           fig.update_layout(legend= {'itemsizing': 'constant'}),\
           comment, \
           options_return, \
           options_return[0]['value'], \
           product_chosen


@app.callback(
    [
        Output('slider_map', 'max'),
        Output('slider_map', 'value'),
    ],
    [
        Input('drop_map', 'value')
    ]
)
def update_slider(product):
    year = productions[productions['Item'] == product]['Year'].max()
    return year, year


@app.callback(
    [
        Output('title_map', 'children'),
        Output('map', 'figure')
    ],
    [
        Input('drop_map', 'value'),
        Input('slider_map', 'value'),
        Input('drop_continent', 'value')
    ],
    [State("drop_map", "options")]
)
def update_map(drop_map_value, year, continent, opt):
    ################## Emissions datset ##################

    the_label = [x['label'] for x in opt if x['value'] == drop_map_value]

    data_emissions = emissions[emissions["Food product"] == the_label[0]]

    ################## Choroplet Plot ##################

    prod1 = productions[(productions['Item'] == drop_map_value) & (productions['Year'] == year)]

    title = '  Production quantities of {}, by country and year'.format(prod1['Item'].unique()[0] )  # font_color = '#363535',
    data_slider = []
    data_each_yr = dict(type='choropleth',
                        locations=prod1['Area'],
                        locationmode='country names',
                        autocolorscale=False,
                        z=np.log(prod1['Value'].astype(float)),
                        zmin=0,
                        zmax=np.log(productions[productions['Item'] == drop_map_value]['Value'].max()),
                        # colorscale=["#ffe2bd", "#006837"],
                        colorscale=["#FFFF00", "#CD5C5C"],
                        marker_line_color='rgba(0,0,0,0)',
                        colorbar={'title': 'Tonnes (log)'},  # Tonnes in logscale
                        colorbar_lenmode='fraction',
                        colorbar_len=0.7,
                        colorbar_x=1,
                        colorbar_xanchor='left',
                        colorbar_y=0.5,
                        name='')
    data_slider.append(data_each_yr)

    layout = dict(geo=dict(scope=continent,
                           projection={'type': 'natural earth'},
                           bgcolor='rgba(0,0,0,0)'),
                  margin=dict(l=0,
                              r=0,
                              b=0,
                              t=0,
                              pad=0),
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')

    fig_choropleth = go.Figure(data=data_slider, layout=layout)
    fig_choropleth.update_geos(showcoastlines=False, showsubunits=True, showframe=True)

    return title, \
           fig_choropleth


@app.callback(
    [Output('title_line', 'children'),
     Output('fig1', 'figure')]
    ,
    Input('ani_veg', 'value')
)
def update_graph(dropdown_line):
    # font_color = '#363535',
    if dropdown_line == 0:
        prod1 = df3[(df3['Origin'] == 'Animal') & (df3['Year'] >= 1990)]

        title = '3. Production quantities of animal, by year'
        layout = go.Layout(
            dict(xaxis_title="Year", yaxis_title="Production quantities", height=300, font_color='#363535',
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                 margin_pad=20))

        fig = go.Figure(
            data=go.Scatter(x=prod1['Year'], y=prod1['value'], line_color='#B22222', fill='tozeroy', line_width=4
                            ), layout=layout
        )
        fig.update_layout(yaxis_range=[0, 10000000000])

    elif dropdown_line == 1:
        prod1 = df3.loc[df3['Origin'] == 'Vegetal']
        # print(prod1['Year'].unique())
        title = '3.Production quantities of vegetal, by year'
        layout = go.Layout(
            dict(xaxis_title="Year", yaxis_title="Production quantities", height=300, font_color='#363535',
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                 margin_pad=20))

        fig = go.Figure(
            data=go.Scatter(x=prod1['Year'], y=prod1['value'], line_color='#2E8B57', fill='tozeroy', line_width=4
                            ), layout=layout
        )
        fig.update_layout(yaxis_range=[0, 10000000000])

    else:
        title = '3.Production quantities of all productions, by year'
        prod1 = df4[( df3['Year'] >= 1990)]

        # prod1 = df4
        layout = go.Layout(
            dict(xaxis_title="Year", yaxis_title="Production quantities", height=300, font_color='#363535',
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                 margin_pad=20))

        fig = go.Figure(
            data=go.Scatter(x=prod1['Year'], y=prod1['value'], line_color='#5CACEE', fill='tozeroy', line_width=4
                            ), layout=layout
        )

    return title, \
           fig


@app.callback(
    Output('graph2', 'figure'),

    Input('drop_map', 'value')
    , Input('ani_veg', 'value')

)
def update_bar_chart(name, origin):
    if origin == 1:
        data = emissions_bar
        color=  '#2E8B57'
    elif origin == 0:
        data = emissions_bar
        color='#B22222'
    else:
        if emissions_bar.loc[emissions_bar['Food product'] == name].values.tolist()[0][-1]=='Vegetal':
            color = '#2E8B57'
        else:
            color = '#B22222'
        data = emissions_bar
    x = ['Land use change', 'Animal Feed', 'Farm', 'Processing', 'Transport', 'Packging', 'Retail']
    y = data.loc[data['Food product'] == name].values.tolist()
    data = [go.Bar(
        x=x,
        y=y[0],
        marker_color=color
    )]
    title = 'Emissions measured as kg of CO2 per kg of {}'.format(name)  # font_color = '#363535',

    fig = go.Figure(data=data, layout=dict(height=190, width=1000,font_color='#363535', paper_bgcolor='rgba(0,0,0,0)',
                                           plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                                           margin_pad=10,yaxis_range=[0, 40],title=title))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

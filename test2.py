import dash
from dash import dcc
from dash import html 
from dash.dependencies import Input,Output


app = dash.Dash()

app.layout = html.Div([html.Div("TITRE : premier élément",style={
    "color":"white",
    "text-align":"center",
    "background-color":"blue",
    "font-size":"34px",
}),html.Div("deuxième element")])

app.run_server()
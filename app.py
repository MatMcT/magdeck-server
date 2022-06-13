import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output
import pandas as pd
from magdeck import MagDeck

deck = MagDeck()


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Magnetic Rack Controller"


app.layout = dbc.Container(
    [
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Magnetic Deck controller", className="header-title"
                ),
                html.P(
                    children="Probe the plate to get the plate bottom position. Then use the engage/disengage buttons",
                    className="header-description",
                ),
            ],
            className="header row",
        ),
        dbc.Toast(
            "Connection failed. Check unit is turned on and connected",
            id="error-toast",
            header="Error",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        ),

        html.Div(
            children=[
                dbc.Input(id="probe-txt", placeholder="Plate not probed yet", type="text", className="me-md-2", disabled=True),
                dbc.FormText("Current plate position"),
            ],
            className="d-grid gap-2 d-md-flex justify-content-md-left input-row",
        ),

        html.Div(
            children=[
                # dbc.Button("Home Deck", color="primary", id="home-btn", className="me-mb-2"),
                dbc.Button("Probe Plate", color="primary", id="probe-btn", className="me-md-2"),
                dbc.Button("Engage", color="primary", id="engage-btn", className="me-md-2", disabled=True),
                dbc.Button("Disengage", color="primary", id="disengage-btn", className="me-md-2", disabled=True),
            ],
            className="d-grid gap-2 d-md-flex justify-content-md-left row",
        ),

       
    ]
)

# @app.callback(
#     Output("home-btn", "n_clicks"),[Input("home-btn", "n_clicks")]
# )
# def home(n):
#     if n:
#         deck.home()
    
@app.callback(
    [Output("probe-txt", "placeholder"),
     Output("engage-btn", "disabled"),
     Output("disengage-btn", "disabled"),
     Output("error-toast", "is_open")],
    [Input("probe-btn", "n_clicks")]
)
def probe(n):
    
    if n:
        # On press
        # update the current plate indicator if probed
        pos = deck.probe_plate() 
        if pos:
            return pos, False, False, False
        else:
            return "Plate not probed yet", True, True, True
    else:
        # On page load
        # Check if unit has previously been probed and update accordingly
        pos = deck.get_plate_position()
        if pos:
            return pos, False, False, False
        else:
            return "Plate not probed yet", True, True, False

            
@app.callback(
    Output("engage-btn", "n_clicks"),[Input("engage-btn", "n_clicks")]
)
def engage(n):
    if n:
        if deck.get_plate_position():
            deck.move_to_plate()

@app.callback(
    Output("disengage-btn", "n_clicks"),[Input("disengage-btn", "n_clicks")]
)
def disengage(n):
    if n:
        deck.move(0)

if __name__ == "__main__":
    HOST = 'localhost'
    app.run_server(host=HOST)
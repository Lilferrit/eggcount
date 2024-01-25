import dash_bootstrap_components as dbc

NAVBAR_MIN_HEIGHT = "4rem"

def get_navbar() -> dbc.Nav:
    return dbc.Nav(
        children = [
            dbc.NavItem(
                dbc.NavLink("Home")
            ),
            dbc.NavItem(
                dbc.NavLink("About")
            )
        ],
        class_name = "bg-dark",
        style = {
            "min-height": NAVBAR_MIN_HEIGHT
        }
    )
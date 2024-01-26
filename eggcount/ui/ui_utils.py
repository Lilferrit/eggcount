import dash_bootstrap_components as dbc

NAVBAR_MIN_HEIGHT = "4rem"

def get_navbar() -> dbc.Nav:
    return dbc.Nav(
        children = [
            dbc.NavItem(
                children = dbc.NavLink(
                    children = "Home",
                    href = "/",
                    class_name = "text-light"
                )
            ),
            dbc.NavItem(
                children = dbc.NavLink(
                    children = "Usage Guide",
                    href = "/guide",
                    class_name = "text-light"
                )
            ),
            dbc.NavItem(
                children = dbc.NavLink(
                    children = "About",
                    href = "/about",
                    class_name = "text-light"
                )
            )
        ],
        class_name = "bg-dark d-flex flex-row justify-content-start align-items-center",
        style = {
            "min-height": NAVBAR_MIN_HEIGHT
        }
    )
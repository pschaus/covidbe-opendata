import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
from dash.dependencies import Input, Output, State
from flask import request, g
from flask_babel import Babel, lazy_gettext

from pages.cases import cases_menu
from pages.deaths import deaths_menu
from pages.international import international_menu
from pages.hospitals import hospitals_menu

FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(__name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, FA],
    external_scripts=["https://cdn.plot.ly/plotly-locale-fr-latest.js", "https://cdn.plot.ly/plotly-locale-nl-latest.js", "https://cdn.plot.ly/plotly-locale-de-latest.js"],
    # these meta_tags ensure content is scaled correctly on different devices
    # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)
app.config['suppress_callback_exceptions'] = True
server = app.server

# Hook Flask-Babel to the app
babel = Babel(app.server)


@babel.localeselector
def get_locale():
    g.locale = "fr"
    if not g.get('locale', None):
        translations = [str(translation) for translation in babel.list_translations()]
        g.locale = request.accept_languages.best_match(translations)
    return g.locale


menus = [cases_menu, deaths_menu, hospitals_menu, international_menu]
menu_links = {}
for menu_idx, menu in enumerate(menus):
    for x in menu.children:
        menu_links[x] = {"id": f"menu_{len(menu_links)}", "href": menu.base_link+x.link}


def generate_sidebar():
    # we use the Row and Col components to construct the sidebar header
    # it consists of a title, and a toggle, the latter is hidden on large screens
    sidebar_header = dbc.Row(
        [
            dbc.Col(html.H2("Covidata.be", className="display-6")),
            dbc.Col(
                [
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "borderColor": "rgba(0,0,0,.1)",
                        },
                        id="navbar-toggle",
                    ),
                    html.Button(
                        # use the Bootstrap navbar-toggler classes to style
                        html.Span(className="navbar-toggler-icon"),
                        className="navbar-toggler",
                        # the navbar-toggler classes don't set color
                        style={
                            "color": "rgba(0,0,0,.5)",
                            "borderColor": "rgba(0,0,0,.1)",
                        },
                        id="sidebar-toggle",
                    ),
                ],
                # the column containing the toggle will be only as wide as the
                # toggle, resulting in the toggle being right aligned
                width="auto",
                # vertically align the toggle in the center
                align="center",
            ),
        ]
    )

    menus_components = []
    for menu_idx, menu in enumerate(menus):
        this_menu_links = [
            dbc.NavLink(
                [html.I(className="fas fa-arrow-right mr-3"), str(x.link_name)],
                id=menu_links[x]["id"], href=menu_links[x]["href"]
            )
            for x in menu.children
        ]

        menus_components += [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        dbc.Col(dcc.Link(str(menu.name), href=menu.base_link+menu.children[0].link)),
                        dbc.Col(
                            html.I(className="fas fa-chevron-right mr-3"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                id=f"submenu-{menu_idx}",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                this_menu_links,
                id=f"submenu-{menu_idx}-collapse",
            ),
        ]

    return [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "Select any link below to learn more about the virus and how Belgium handles it.",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(menus_components, vertical=True),
            id="collapse",
        ),
    ]
    return sidebar

def gen_layout():
    print(f"REGENERATE LAYOUT {get_locale()}")
    return html.Div([
        dcc.Location(id="url"),
        html.Div(generate_sidebar(), id="sidebar"),
        dcc.Loading(children=html.Div(id="page-content"))
    ])

layout_lang_cache = {}
def serve_layout():
    if flask.has_request_context():
        key = str(get_locale())
        print(f"SERVE {get_locale()}")
        if key not in layout_lang_cache:
            layout_lang_cache[key] = gen_layout()
        return layout_lang_cache[key]
    return html.Div([dcc.Location(id="url")])


app.layout = serve_layout

for link_comp in menu_links.values():
    def gen_f(link):
        return lambda x: x == link or ((x == "/" or x == "/index") and link == "/cases/overview")
    app.callback(
        Output(link_comp["id"], "active"),
        [Input("url", "pathname")]
    )(gen_f(link_comp["href"]))


# this function applies the "open" class to rotate the chevron
def set_navitem_class(is_open):
    if is_open:
        return "open"
    return ""


for i in range(len(menus)):
    def toggle_collapse(menu):
        return lambda x: x.startswith(menu.base_link) or ((x == "/" or x == "/index") and menu.base_link == "/cases")

    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input("url", "pathname")]
    )(toggle_collapse(menus[i]))

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)

page_generators = {menu.base_link+page.link: page.display_fn for menu in menus for page in menu.children}
page_cache = {}


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        pathname = "/cases/overview"

    if pathname in page_generators:
        if (pathname, str(get_locale())) not in page_cache:
            page_cache[pathname, str(get_locale())] = page_generators[pathname]()
        return page_cache[pathname, str(get_locale())]

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for menu in menus:
    for page in menu.children:
        page.callback_fn(app)

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)

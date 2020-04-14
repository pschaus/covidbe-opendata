import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import flask_babel
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
from flask import request, g, abort, redirect
from flask_babel import Babel, lazy_gettext, gettext

from graphs import registered_plots
from graphs.cases_per_municipality import map_communes_per_inhabitant
from pages import ThreadSafeCache, lang_cache, get_translation
from pages.cases import cases_menu
from pages.deaths import deaths_menu
from pages.index import index_menu
from pages.international import international_menu
from pages.hospitals import hospitals_menu

FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, FA],
                external_scripts=[
                    "https://cdn.plot.ly/plotly-locale-fr-latest.js",
                    "https://cdn.plot.ly/plotly-locale-nl-latest.js",
                    "https://cdn.plot.ly/plotly-locale-de-latest.js",
                    "https://platform.twitter.com/widgets.js",
                    "https://www.googletagmanager.com/gtag/js?id=UA-131327483-1",
                    "https://http://www.covidata.be/assets/gtag.js",
                ],
                # these meta_tags ensure content is scaled correctly on different devices
                # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                    {"name": "google-site-verification", "content": "gQNHNoCstG07kDFbPFAdPj4lSyiZrzqzfUqMZ3XZF8w"}
                ],
)
app.title = "Covidata.be"
app.config['suppress_callback_exceptions'] = True
server = app.server

# Hook Flask-Babel to the app
babel = Babel(app.server)


@babel.localeselector
def get_locale():
    g.locale = request.cookies.get("lang")
    if not g.get('locale', None):
        translations = ["en", "fr", "nl"]
        g.locale = request.accept_languages.best_match(translations)
    return g.locale


menus = [index_menu, cases_menu, deaths_menu, hospitals_menu, international_menu]
menu_links = {}
for menu_idx, menu in enumerate(menus):
    for x in menu.children:
        menu_links[x] = {"id": f"menu_{len(menu_links)}", "href": menu.base_link + x.link}


def generate_sidebar():
    # we use the Row and Col components to construct the sidebar header
    # it consists of a title, and a toggle, the latter is hidden on large screens
    sidebar_header = dbc.Row(
        [
            dbc.Col(html.A([html.H2([html.Img(src='/assets/covidata.png', style={"height": "70px", "margin-right": "5px"}), "Covidata.be"], id="sidebar-title", className="display-6")], href="http://www.covidata.be/", style={"color":"black","text-decoration": "none"})),
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

        if not menu.fake_menu:
            menus_components += [
                html.Li(
                    # use Row and Col components to position the chevrons
                    dbc.Row(
                        [
                            dbc.Col(dcc.Link(str(menu.name), href=menu.base_link + menu.children[0].link)),
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
        else:
            menus_components += this_menu_links

    menus_components.append(html.Li(
        dbc.Row(
            [
                dbc.Col(gettext("Language"), className="navbar-text"),
                dbc.Col(dbc.Button("EN", color="link", id="en-lang", disabled=str(get_locale()) == "en")),
                dbc.Col(dbc.Button("FR", color="link", id="fr-lang", disabled=str(get_locale()) == "fr")),
                dbc.Col(dbc.Button("NL", color="link", id="nl-lang", disabled=str(get_locale()) == "nl"))
            ],
            className="my-1",
        ),
        id="language-switcher"
    ))
    return [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                #html.Hr(),
                html.P(
                    get_translation(
                        en="Select any link below to learn more about the virus and how Belgium handles it.",
                        fr="Cliquez sur les liens ci-dessous pour en apprendre plus sur le virus et sur la manière dont la Belgique gère cette crise."
                    ),
                    className="lead",
                ),
            ],
            className="blurb"
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            [
                dbc.Nav(menus_components, vertical=True)
            ],
            id="collapse",
        ),
        html.Div(
            [
                html.A("Tweets by Covidatabe", className="twitter-timeline", href="https://twitter.com/Covidatabe?ref_src=twsrc%5Etfw")
            ],
            id="twitterdiv",
            className="blurb"
        )
    ]
    return sidebar


@lang_cache
def gen_layout():
    # print(f"REGENERATE LAYOUT {get_locale()}")
    return html.Div([
        dcc.Store(id="memory", data={"lang": str(get_locale())}),
        dcc.Location(id="url"),
        html.Div(generate_sidebar(), id="sidebar"),
        dcc.Loading(children=html.Div(id="page-content"))
    ])


def serve_layout():
    if flask.has_request_context():
        return gen_layout()
    return html.Div([dcc.Location(id="url")])


app.layout = serve_layout

for link_comp in menu_links.values():
    def gen_f(link):
        return lambda x: x == link or (x == "/" and link == "/index")


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
        return lambda x, _ignore: x.startswith(menu.base_link)


    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input("url", "pathname"), Input("sidebar", "children")]
    )(toggle_collapse(menus[i]))

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)

page_objects = {menu.base_link + page.link: (menu, page) for menu in menus for page in menu.children}
page_cache = ThreadSafeCache()


@app.callback(Output("sidebar", "children"),
              [Input("memory", "data")])
def update_sidebar_lang(ignore):
    return generate_sidebar()


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname"), Input("memory", "data")])
def render_page_content(pathname, lang_data):
    if pathname == "/":
        pathname = "/index"

    if pathname in page_objects:
        return page_cache.get((pathname, str(get_locale())), page_objects[pathname][1].display_fn)

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


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


@app.callback(Output('memory', 'data'),
              [Input('{}-lang'.format(lang), 'n_clicks') for lang in ["fr", "en"]],
              [State('memory', 'data')])
def on_click(*args):
    current = args[-1]
    ctx = dash.callback_context
    if not ctx.triggered or all(x is None for x in args[:-1]):
        raise PreventUpdate

    lang = ctx.triggered[0]['prop_id'].split('.')[0].split("-")[0]

    if current.get("lang") == lang:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    dash.callback_context.response.set_cookie('lang', lang)
    g.locale = lang
    flask_babel.refresh()
    return {"lang": lang}


app.clientside_callback(
    ClientsideFunction('twitter_upd', 'twitter_upd'),
    Output("twitterdiv", "upd"),
    [Input("url", "pathname"), Input("memory", "data"), Input("sidebar", "children")]
)


@app.server.route("/embed/html/<which>")
def plot_embed_html(which):
    if which not in registered_plots:
        abort(404)
    return redirect(registered_plots[which].get_html_link())


# @app.server.route("/embed/image/<which>")
# def plot_embed_image(which):
#     if which not in registered_plots:
#         abort(404)
#     return registered_plots[which].get_image_link()


def memory_summary():
    # Only import Pympler when we need it. We don't want it to
    # affect our process if we never call memory_summary.
    from pympler import summary, muppy
    mem_summary = summary.summarize(muppy.get_objects())
    rows = summary.format_(mem_summary)
    return '\n'.join(rows)

original_interpolate_index = app.interpolate_index
def layout(metas="", title="", css="", config="", scripts="", app_entry="", favicon="", renderer=""):
    try:
        pathname = flask.request.path
        menu, page = page_objects[pathname]
        title += " - " + page.title

        if page.plot is not None:
            link_html = page.plot.get_html_link()
            desc = gettext("Click here to open the interactive visualization")
            link_image = page.plot.get_image_link()
            metas += f"""
            <meta name="twitter:card" content="player"/>
            <meta name="twitter:site" content="@covidatabe"/>
            <meta name="twitter:title" content="Covidata.be - {page.title}"/>
            <meta name="twitter:player" content="{link_html}"/>
            <meta name="twitter:player:width" content="600"/>
            <meta name="twitter:player:height" content="500"/>
            <meta name="twitter:description" content="{desc}"/>
            <meta name="twitter:image" content="{link_image}"/>
            <meta property="og:url" content="https://www.covidata.be/{pathname}"/>
            <meta property="og:type" content="article"/>
            <meta property="og:title" content="{page.title}"/>
            <meta property="og:description" content="{desc}"/>
            <meta property="og:image" content="{link_image}"/>
            """
    except:
        pass  # ignore
    return original_interpolate_index(metas, title, css, config, scripts, app_entry, favicon, renderer)
app.interpolate_index = layout

if __name__ == "__main__":
    @app.server.route("/memory")
    def memory_check():
        print(memory_summary())
        return "see logs"

    app.run_server(port=8888, debug=True)

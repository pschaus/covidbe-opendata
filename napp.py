
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
from flask_caching import Cache


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
cache = Cache(app.server, config={
    'CACHE_TYPE': ('filesystem' if __name__ != "__main__" else 'null'),
    'CACHE_DIR': 'cache-directory'
})
server = app.server





def gen_layout2():
    # print(f"REGENERATE LAYOUT {get_locale()}")
    return html.Div([
    dcc.Markdown("""
            ## Français

            Chers followers/visiteurs,

            Le site ne sera plus maintenu jusqu'au 9 aout 
            
            Guillaume et Pierre
            
            ## English
            
            Dear followers/visitors,

            The website will not be maintained till the 9th of August

            Guillaume and Pierre
            """),
    ])


def serve_layout():
    if flask.has_request_context():
        return gen_layout2()
    return html.Div([dcc.Location(id="url")])


app.layout = serve_layout




if __name__ == "__main__":
    app.run_server(port=8050, debug=False)


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

            Nous avons pris la décision d’arrêter la maintenance de Covidata.be ainsi que les commentaires/analyses des chiffres belges du Covid via twitter.
            
            Nous avions commencé à créer covidata.be au départ pour mettre à disposition nos compétences d’analyse des données au service des citoyens, ensuite par curiosité sur le sujet, mais surtout, pour l’aspect collaboratif, open-science et open-data.
            
            Notre décision d’arrêter est en grande partie influencée par la désillusion de ces deux derniers points: open-science et open-data. 
            
            Il y a en Belgique un manque de transparence sur les données collectées sur le covid rendant très difficiles certaines analyses objectives.
            
            Malgré nos nombreuses alertes sur ce point, le fossé est grandissant entre les données collectées par sciensano et les données réellement mises à disposition des citoyens et de la communauté scientifique.
            
            Si nous constatons un changement et que des données importantes sont mises à disposition, nous reviendrons, promis !
            
            En attendant, nous vous souhaitons à toutes et tous une bonne vaccination et une bonne santé pour 2021!

            Guillaume et Pierre
            
            ## English
            
            Dear followers/visitors,

            We have made the decision to stop the maintenance of Covidata.be as well as the comments of the Belgian numbers via twitter.
            
            We started to create covidata.be initially to make our data analysis skills available to citizens, then to learn more on the subject, but above all, for the collaborative, open-science and open-data aspect.
            
            Our decision to quit is largely influenced by the disillusionment of these last two points: open-science and open-data.
            
            In Belgium, there is a lack of transparency on the data collected related to covid, making certain objective analyzes very difficult.
            
            Despite our numerous warnings on this point, the gap is growing between the data collected by sciensano and the data actually made available to citizens and the scientific community.
            
            If we see a change and important data becomes available, we will come back, we promise!
            
            In the meantime, we wish you all a good vaccination and good health for 2021!

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

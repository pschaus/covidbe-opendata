from napp import app #important: we need this to start the translation mechanism. A bit hacky.
from flask import g
import flask_babel
from graphs import registered_plots
from graphs.cases_per_municipality import map_communes_per_inhabitant

output = "static/embed/{name}_{lang}.html"

with app.server.app_context():
    for lang in ["en", "fr"]:
        g.locale = lang
        flask_babel.refresh()
        for name in registered_plots:
            try:
                gr = registered_plots[name]()
                gr.write_html(output.format(name=name,lang=lang), include_plotlyjs="cdn", include_mathjax="cdn")
                print(name, lang, "done")
            except:
                print("Cannot export", name)
                pass
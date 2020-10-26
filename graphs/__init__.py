import pandas as pd
import os.path
import subprocess

from flask_babel import get_locale

registered_plots = {}

if os.path.exists("static/csv/last_plots.csv"):
    __plots = pd.read_csv("static/csv/last_plots.csv").set_index("name")
else:
    __plots = pd.DataFrame(columns=["name", "link_html", "link_image"]).set_index("name")

try:
    GIT_COMMIT_HASH = subprocess.check_output(["git", "ls-remote", "https://github.com/pschaus/covidbe-opendata.git", "HEAD"]).strip().decode("utf8").split("\t")[0]
except:
    GIT_COMMIT_HASH = "ERROR"

def register_plot_for_embedding(name):
    def inside(f):
        f.name = name
        f.get_html_link = lambda: __plots.loc[name].link_html
        f.get_image_link = lambda: __plots.loc[name].link_image
        def add_button(*args, **kwargs):
            g = f(*args, **kwargs)
            lang = str(get_locale())
            try:
                g.__dict__["embeddable"] = f"https://www.covidata.be/embed/static_html/{GIT_COMMIT_HASH}/{name}_{lang}"
            except:
                print(name, "is embeddable but is not a plotly figure")
                pass
            return g
        registered_plots[name] = add_button
        return add_button
    return inside


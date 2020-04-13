import pandas as pd
import os.path

registered_plots = {}

if os.path.exists("static/csv/last_plots.csv"):
    __plots = pd.read_csv("static/csv/last_plots.csv").set_index("name")
else:
    __plots = pd.DataFrame(columns=["name", "link_html", "link_image"]).set_index("name")

def register_plot_for_embedding(name):
    def inside(f):
        f.name = name
        f.get_html_link = lambda: __plots.loc[name].link_html
        f.get_image_link = lambda: __plots.loc[name].link_image
        registered_plots[name] = f
        return f
    return inside
from typing import List
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import gettext, get_locale


class AppLink:
    def __init__(self, link_name: str, link: str, display_fn, callback_fn=(lambda app: None)):
        self.link_name = link_name
        self.link = link
        self.display_fn = display_fn
        self.callback_fn = callback_fn


class AppMenu:
    def __init__(self, name: str, base_link: str, children: List[AppLink]):
        self.name = name
        self.base_link = base_link
        self.children = children


def model_warning(*elems):
    return [
        html.Div([dcc.Markdown(gettext(
            "**WARNING**: We enter in the realm of models and estimates. Everything below is **wrong**, but **may** give an idea of the reality."))],
                 className="model-warning"),
        html.Div([html.Div([], className="model-warning-content-left")] + list(elems), className="model-warning-content")
    ]


def get_translation(**kwargs):
    key = str(get_locale())
    if key in kwargs:
        return kwargs[key]
    # fallback to "en" if available
    if "en" in kwargs:
        return kwargs["en"]
    return list(kwargs.keys())[0]

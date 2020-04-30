import threading
from typing import List
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import gettext, get_locale

from utils import ThreadSafeCache


class AppLink:
    def __init__(self, title: str, link_name: str, link: str, display_fn, plot=None, callback_fn=(lambda app: None), invisible=False):
        self.title = title
        self.link_name = link_name
        self.link = link
        self.display_fn = display_fn
        self.plot = plot
        self.callback_fn = callback_fn
        self.invisible = invisible


class AppMenu:
    def __init__(self, name: str, base_link: str, children: List[AppLink], fake_menu=False):
        self.name = name
        self.base_link = base_link
        self.children = children
        self.fake_menu = fake_menu


def custom_warning_box(content):
    return html.Div(html.Div(content, className="model-warning-inner"), className="model-warning")


def model_warning(*elems):
    return [
        custom_warning_box(dcc.Markdown(gettext(
            "**WARNING**: We enter in the realm of models and estimates. Everything below is **wrong**, "
            "but **may** give an idea of the reality."
        ))),
        html.Div([html.Div([], className="model-warning-content-left")] + list(elems),
                 className="model-warning-content")
    ]


def get_translation(**kwargs):
    key = str(get_locale())
    if key in kwargs:
        return kwargs[key]
    # fallback to "en" if available
    if "en" in kwargs:
        return kwargs["en"]
    return list(kwargs.keys())[0]


def lang_cache(f):
    cache = ThreadSafeCache()
    return lambda: cache.get(str(get_locale()), f)



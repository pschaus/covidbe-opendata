from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.lockdown.traffic import display_traffic
from pages.lockdown.mobility_report import display_mobility
from pages.lockdown.brussels import display_brussels
from pages.lockdown.tomtom import display_tomtom
from pages.lockdown.facebook import display_facebook, callback_fb
from pages.lockdown.facebook_eu import callback_fb_countries_eu, display_facebook_eu
from pages.lockdown.facebook_lux import callback_fb_countries,callback_fb_lux, display_facebook_lux

def call_back_fb_eu(app):
    callback_fb_countries_eu(app)

def call_back_fb_lux(app):
    facebook_lux.callback_fb_countries(app)
    facebook_lux.callback_fb_lux(app)

lockdown_menu = AppMenu(lazy_gettext("Lockdown Impact"), "/lockdown", [
    AppLink(lazy_gettext("Mobility Reports"), lazy_gettext("Mobility Report"), "/mobility-reports", display_mobility),
    AppLink(lazy_gettext("Google-Map Traffic"), lazy_gettext("Google Map Internet Traffic EU"), "/google-map", display_traffic),
])


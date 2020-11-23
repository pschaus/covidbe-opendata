from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.lockdown.traffic import display_traffic
from pages.lockdown.mobility_report import display_mobility
from pages.lockdown.brussels import display_brussels
from pages.lockdown.tomtom import display_tomtom
from pages.lockdown.facebook import display_facebook, callback_fb
from pages.lockdown.facebook_lux import display_facebook_lux, callback_fb_lux

lockdown_menu = AppMenu(lazy_gettext("Lockdown Impact"), "/lockdown", [
    AppLink(lazy_gettext("Mobility Reports"), lazy_gettext("Mobility Report"), "/mobility-reports", display_mobility),
    AppLink(lazy_gettext("Google-Map Traffic"), lazy_gettext("Google Map Internet Traffic EU"), "/google-map", display_traffic),
    AppLink(lazy_gettext("TomTom Traffic Data"), lazy_gettext("TomTom Traffic Data"), "/tomtom", display_tomtom),
    AppLink(lazy_gettext("Brussels"), lazy_gettext("Brussels"), "/brussels", display_brussels),
    AppLink(lazy_gettext("Facebook"), lazy_gettext("Facebook"), "/facebook", display_facebook, callback_fn=callback_fb),
    AppLink(lazy_gettext("Facebook-lux"), lazy_gettext("Facebook-lux"), "/facebook_lux", display_facebook_lux, callback_fn=callback_fb_lux,invisible=True),

    ])


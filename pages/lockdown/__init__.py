from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.lockdown.traffic import display_traffic
from pages.lockdown.mobility_report import display_mobility


lockdown_menu = AppMenu(lazy_gettext("Lockdown Impact"), "/lockdown", [
    AppLink(lazy_gettext("Google-Map Traffic"), lazy_gettext("Google Map Internet Traffic EU"), "/mobility", display_traffic),
    AppLink(lazy_gettext("Google Mobility Report"), lazy_gettext("Google Mobility Report EU"), "/google-mobility", display_mobility),
])
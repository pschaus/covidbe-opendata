from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.lockdown.mobility import display_mobility


lockdown_menu = AppMenu(lazy_gettext("Lockdown Impact"), "/lockdown", [
    AppLink(lazy_gettext("Mobility"), lazy_gettext("Mobility"), "/mobility", display_mobility),
])
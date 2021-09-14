from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.lockdown.mobility_report import display_mobility


lockdown_menu = AppMenu(lazy_gettext("Lockdown Impact"), "/lockdown", [
    AppLink(lazy_gettext("Mobility Reports"), lazy_gettext("Mobility Report"), "/mobility-reports", display_mobility),])


from flask_babel import lazy_gettext

from pages import AppMenu, AppLink

from pages.deaths.overmortality import display_overmortality
from pages.deaths.age_groups import display_age_groups
deaths_menu = AppMenu(lazy_gettext("Deaths"), "/deaths", [
    AppLink(lazy_gettext("Overmortality"), "/overmortality", display_overmortality),
    AppLink(lazy_gettext("Age Groups"), "/age_groups", display_age_groups)
])

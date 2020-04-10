from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.cases.overview import overview_link
from pages.cases.provinces import display_provinces
from pages.cases.age_groups import display_age_groups

cases_menu = AppMenu(lazy_gettext("Cases"), "/cases", [
    overview_link,
    AppLink(lazy_gettext("Provinces"), "/provinces", display_provinces),
    AppLink(lazy_gettext("Age Groups"), "/age_groups", display_age_groups)
])
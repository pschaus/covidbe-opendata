from flask_babel import lazy_gettext

from pages import AppMenu, AppLink

from pages.hospitals.hospitals_be import display_hospitals
from pages.hospitals.hospitals_prov import display_hospitals_prov

hospitals_menu = AppMenu(lazy_gettext("Hospitalization"), "/hospitals", [
    AppLink(lazy_gettext("Belgium"), lazy_gettext("Belgium"), "/hospitals_be", display_hospitals),
    AppLink(lazy_gettext("Provinces"), lazy_gettext("Provinces"), "/hospitals_prov", display_hospitals_prov),
])

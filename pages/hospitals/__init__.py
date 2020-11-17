from flask_babel import lazy_gettext

from pages import AppMenu, AppLink

from pages.hospitals.hospitals_be import display_hospitals
from pages.hospitals.hospitals_prov import display_hospitals_prov
from pages.hospitals.hospitals_region import display_hospitals_region

hospitals_menu = AppMenu(lazy_gettext("Hospitalization"), "/hospitals", [
    AppLink(lazy_gettext("Belgium"), lazy_gettext("Belgium"), "/hospitals_be", display_hospitals),
    AppLink(lazy_gettext("Provinces"), lazy_gettext("Provinces"), "/hospitals_prov", display_hospitals_prov),
    AppLink(lazy_gettext("Regions"), lazy_gettext("Region"), "/hospitals_regions", display_hospitals_region),

])

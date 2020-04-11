from pages import AppMenu, AppLink

from pages.hospitals.hospitals_be import display_hospitals
from pages.hospitals.hospitals_prov import display_hospitals_prov

hospitals_menu = AppMenu("Hospitals", "/hospitals", [
    AppLink("Hospitals Belgium", "/hospitals_be", display_hospitals),
    AppLink("Hospitals Provinces", "/hospitals_prov", display_hospitals_prov),
])

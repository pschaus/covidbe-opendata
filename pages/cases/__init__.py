from pages import AppMenu, AppLink
from pages.cases.overview import overview_link
from pages.cases.provinces import display_provinces

cases_menu = AppMenu("Cases", "/cases", [
    overview_link,
    AppLink("Provinces", "/provinces", display_provinces)
])
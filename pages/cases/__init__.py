from pages import AppMenu, AppLink
from pages.cases.overview import overview_link
from pages.cases.b import display_b

cases_menu = AppMenu("Cases", "/cases", [
    overview_link,
    AppLink("B", "/b", display_b)
])
from pages import AppMenu, AppLink
from pages.cases.overview import overview_link
from pages.cases.provinces import display_provinces
from pages.cases.age_groups import display_age_groups

cases_menu = AppMenu("Cases", "/cases", [
    overview_link,
    AppLink("Provinces", "/provinces", display_provinces),
    AppLink("Age Groups", "/age_groups", display_age_groups)
])
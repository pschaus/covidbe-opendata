from pages import AppMenu, AppLink
from pages.cases.overview import overview_link
from pages.cases.provinces import display_provinces
from pages.cases.age_groups import display_age_groups
from pages.cases.testing import display_testing

cases_menu = AppMenu("Cases", "/cases", [
    overview_link,
    AppLink("Provinces", "/provinces", display_provinces),
    AppLink("Age Groups", "/age_groups", display_age_groups),
    AppLink("Testing", "/testing", display_testing),
])
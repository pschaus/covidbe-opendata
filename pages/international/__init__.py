from pages import AppMenu, AppLink
from pages.international.evolution_per_country import display_a,callback_a
from pages.international.cases_per_million import display_cases_per_million, callback_cases_per_million
from pages.international.deaths_per_million import display_deaths_per_million, callback_deaths_per_million

international_menu = AppMenu("International", "/international", [
    AppLink("Evolution per country", "/evolution_per_country", display_a, callback_a),
    AppLink("Cases per million", "/cases_per_million", display_cases_per_million, callback_cases_per_million),
    AppLink("Deaths per million", "/deaths_per_million", display_deaths_per_million, callback_deaths_per_million),
])
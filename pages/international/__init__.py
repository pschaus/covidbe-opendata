from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.international.euromomo import display_euromomo
from pages.international.evolution_per_country import display_a,callback_a
from pages.international.cases_per_million import display_cases_per_million
from pages.international.deaths_per_million import display_deaths_per_million, callback_deaths_per_million
from pages.international.hospitalisations import display_hospi_international, callback_display_hospi_international

international_menu = AppMenu("International", "/international", [
    #AppLink("EUROMOMO", "EUROMOMO", "/euromomo", display_euromomo),
    AppLink(lazy_gettext("Evolution per country"), lazy_gettext("Evolution per country"), "/evolution_per_country", display_a, callback_fn=callback_a,invisible=True),
    AppLink(lazy_gettext("Cases per million"), lazy_gettext("Cases per million"), "/cases_per_million", display_cases_per_million),
    AppLink(lazy_gettext("Deaths per million"), lazy_gettext("Deaths per million"), "/deaths_per_million", display_deaths_per_million, callback_fn=callback_deaths_per_million,invisible=True),
    AppLink(lazy_gettext("Hospitalizations EU"), lazy_gettext("Hospitalizations EU"), "/hospi_per_100k",
            display_hospi_international, callback_fn=callback_display_hospi_international),

])
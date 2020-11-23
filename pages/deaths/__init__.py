from flask_babel import lazy_gettext

from graphs.obituary import rolling_ratio_plot
from graphs.overmortality import overmortality_estimates_repartition_bar
from pages import AppMenu, AppLink

from pages.deaths.overmortality import display_overmortality
from pages.deaths.age_groups import display_age_groups
from pages.deaths.obituary import display_obituary
from pages.deaths.covid_deaths import display_covid_death
from pages.deaths.admin_region import display_arrondissements

from pages import get_translation


deaths_menu = AppMenu(lazy_gettext("Deaths"), "/deaths", [
    AppLink(get_translation(fr="Décès COVID / Groupes d'ages", en="COVID Deaths / Age group"),
            lazy_gettext("Covid Deaths"),
            "/covid", display_covid_death),
    AppLink(get_translation(fr="Décès totaux / Groupes d'ages", en="Overal Deaths / Age group"), lazy_gettext("All Deaths"), "/all", display_age_groups),
    AppLink(get_translation(fr= "Evolution Nécrologiques", en = "Obituary evolution"), get_translation(fr= "Nécrologie", en = "Obituary"), "/obituary", display_obituary,
            plot=rolling_ratio_plot),
    AppLink(get_translation(fr="Décès / Arrondissements", en="Deaths / Admin Region"),
            get_translation(fr="Arrondissements", en="Admin Region"), "/admin_region", display_arrondissements),
    AppLink(get_translation(fr="Surmortalité", en="Overmortality"), get_translation(fr="Surmortalité", en="Overmortality"),
        "/overmortality", display_overmortality,
        plot=overmortality_estimates_repartition_bar),

])



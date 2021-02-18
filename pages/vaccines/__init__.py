from flask_babel import lazy_gettext


from graphs.overmortality import overmortality_estimates_repartition_bar
from pages import AppMenu, AppLink

from pages.deaths.overmortality import display_overmortality
from pages.deaths.age_groups import display_age_groups
from pages.deaths.obituary import display_obituary
from pages.vaccines.vaccines import display_vaccines


from pages import get_translation


vaccines_menu = AppMenu(lazy_gettext("Vaccines"), "/vaccines", [
    AppLink(get_translation(fr="Vaccins", en="Vaccines"),
            lazy_gettext("Vaccines"),
            "/vaccines", display_vaccines),

])



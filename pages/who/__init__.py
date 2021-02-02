from flask_babel import lazy_gettext


from graphs.overmortality import overmortality_estimates_repartition_bar
from pages import AppMenu, AppLink

from pages.deaths.overmortality import display_overmortality
from pages.deaths.age_groups import display_age_groups
from pages.deaths.obituary import display_obituary
from pages.who.who import display_who


from pages import get_translation


who_menu = AppMenu(lazy_gettext("WHO Indicators"), "/who", [
    AppLink(get_translation(fr="Indicateurs OMS", en="WHO Indicators"),
            lazy_gettext("WHO Indicators"),
            "/who", display_who),

])



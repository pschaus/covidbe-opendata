from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.cases.municipalities import municipalities_link
from pages.cases.provinces import display_provinces
from pages.cases.age_groups import display_age_groups
from pages.cases.testing import display_testing
from pages.cases.Re import display_Re

cases_menu = AppMenu(lazy_gettext("Cases"), "/cases", [
    municipalities_link,
    AppLink(lazy_gettext("Cases per province"), lazy_gettext("Per province"), "/provinces", display_provinces),
    AppLink(lazy_gettext("Cases per age groups"), lazy_gettext("Age Groups"), "/age_groups", display_age_groups),
    AppLink(lazy_gettext("Testing"), lazy_gettext("Testing"), "/testing", display_testing),
    #AppLink(lazy_gettext("Re"), lazy_gettext("Re"), "/Re", display_Re)
])
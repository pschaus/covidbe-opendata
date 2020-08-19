from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.cases.cases_correction import display_cases_correction
from pages.cases.municipalities import municipalities_link
from pages.cases.admin_region import display_admin
from pages.cases.provinces import display_provinces
from pages.cases.age_groups import display_age_groups
from pages.cases.testing import display_testing
from pages.cases.Re import display_Re, callback_Re


from pages import get_translation

cases_menu = AppMenu(lazy_gettext("Cases"), "/cases", [
    municipalities_link,
    AppLink(get_translation(en="Cases per age-group",fr="Cas par agroupe d'age",lazy=True), get_translation(en="Age-group",fr="Groupes d'age",lazy=True), "/age_groups", display_age_groups),
    AppLink(lazy_gettext("Testing"), lazy_gettext("Testing"), "/testing", display_testing),
    AppLink(get_translation(en="Cases per admin region", fr="Cas par arrondissement",lazy=True),
            get_translation(en="Admin Region", fr="Arrondissement",lazy=True), "/admin_region", display_admin),
    AppLink(lazy_gettext("Epidemic Indicators"), lazy_gettext("Epidemic Indicators"), "/Re", display_Re, callback_fn=callback_Re),
    AppLink(get_translation(en="Corrected 1st wave",fr="Correction 1ière vague", lazy=True),
            get_translation(en="Corrected 1st wave",fr="Correction 1ière vague", lazy=True),
            "/first_wave", display_cases_correction)
])

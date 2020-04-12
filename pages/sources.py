import dash_core_components as dcc
import dash_html_components as html
from flask_babel import gettext, get_locale, lazy_gettext
import dash_bootstrap_components as dbc


class SourceProvider:
    def __init__(self, name, link, desc=None):
        self.name = name
        self.link = link
        self.desc = desc


def display_source_providers(*providers: SourceProvider):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4([
                        html.I(className="fas fa-link"), " ", gettext("Sources")], className="card-title"),
                    html.H6(gettext("The following data sources were used to produce this page:"),
                            className="card-subtitle")
                ]
            ),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(
                        str(p.name) + ("" if not p.desc else f" ({p.desc})"),
                        href=p.link,
                        action=True) for p in providers
                ] +
                [
                    dbc.ListGroupItem(gettext("The processed data, along with the software used to process it, is available on GitHub."),
                                      href="https://github.com/pschaus/covidbe-opendata",
                                      action=True, color="primary")
                ],
                flush=True,
            )
        ],
        className="my-3"
    )


source_sciensano = SourceProvider("Sciensano - Covid19", "https://epistat.wiv-isp.be/covid/",
                                  lazy_gettext("Official Belgian data"))
source_map_communes = SourceProvider(lazy_gettext("FPS Finance"),
                                     "https://finances.belgium.be/fr/particuliers/habitation/cadastre/plan-cadastral/lambert-2008/2019",
                                     lazy_gettext("Administrative limits"))
source_map_provinces = SourceProvider("STATBEL",
                                      "https://statbel.fgov.be/fr/open-data/secteurs-statistiques",
                                      lazy_gettext("Administrative limits"))
source_death_causes = SourceProvider("STATBEL",
                                     "https://statbel.fgov.be/en/themes/population/mortality-life-expectancy-and-causes-death/causes-death#figures",
                                     lazy_gettext("Causes of death"))
source_inmemoriam = SourceProvider("inmemoriam", "https://www.inmemoriam.be")
source_necro_sudpress = SourceProvider(lazy_gettext("Sudpresse obituary"), "http://necro.sudpresse.be/")
source_hopkins = SourceProvider(lazy_gettext("Johns Hopkins CSSE & others"),
                                "https://github.com/CSSEGISandData/COVID-19",
                                lazy_gettext("See link for full list of sources"))

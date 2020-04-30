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

source_google_traffic = SourceProvider("Google Traffic Data", "https://transparencyreport.google.com/traffic/overview and https://github.com/Jigsaw-Code/net-analysis/tree/master/netanalysis/traffic",
                                  lazy_gettext("Google Traffic Data"))

source_google_mobility = SourceProvider("Google Mobility Report", "https://www.google.com/covid19/mobility/",
                                  lazy_gettext("Google Mobility Report"))

source_apple_mobility = SourceProvider("Apple Mobility Trends Report", "https://www.apple.com/covid19/mobility",
                                  lazy_gettext("Apple Mobility Report"))

source_map_communes = SourceProvider(lazy_gettext("FPS Finance"),
                                     "https://finances.belgium.be/fr/particuliers/habitation/cadastre/plan-cadastral/lambert-2008/2019",
                                     lazy_gettext("Administrative limits"))
source_map_provinces = SourceProvider("STATBEL",
                                      "https://statbel.fgov.be/fr/open-data/secteurs-statistiques",
                                      lazy_gettext("Administrative limits"))
source_death_causes = SourceProvider("STATBEL",
                                     "https://statbel.fgov.be/en/themes/population/mortality-life-expectancy-and-causes-death/causes-death#figures",
                                     lazy_gettext("Causes of death"))

source_brussels_mobility = SourceProvider("Brussels Mobility",
                                     "https://mobilite-mobiliteit.brussels/fr",
                                     lazy_gettext("Brussels Mobility"))
source_pop = SourceProvider("STATBEL",
                            "https://statbel.fgov.be/fr/themes/population/structure-de-la-population#panel-12",
                            lazy_gettext("Population per municipality"))
source_inmemoriam = SourceProvider("inmemoriam", "https://www.inmemoriam.be")
source_necro_sudpress = SourceProvider(lazy_gettext("Sudpresse obituary"), "http://necro.sudpresse.be/")
source_hopkins = SourceProvider(lazy_gettext("Johns Hopkins CSSE & others"),
                                "https://github.com/CSSEGISandData/COVID-19",
                                lazy_gettext("See link for full list of sources"))

source_SI_modelRe = SourceProvider(lazy_gettext("Theory versus Data: How to Calculate R0?, Breban et al."),
                        "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0000282&type=printable",
                        lazy_gettext("See link for details on the assumptions"))

source_euromomo = SourceProvider("EUROMOMO", "https://www.euromomo.eu")

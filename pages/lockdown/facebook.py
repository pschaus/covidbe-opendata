import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.facebook import population_proportion, population_evolution, movement, staying_put
from pages.sources import display_source_providers, source_facebook
from pages import get_translation

def display_facebook():
    return [
        html.P(
            get_translation(
                fr="""
                Toutes les données présentées dans les visualisations ci-dessous concernent uniquement les utilisateurs de Facebook ayant activé leur localisation.
                """,
                en="""
                All data visualized below only concerns Facebook users who activate their localization.
                """)),
        html.H3(
            get_translation(
                fr="Changement du nombre de tuiles visitées quotidiennement par rapport à la normale",
                en="Change in the daily number of tiles visited wrt normality")),
        html.Span(
            get_translation(
                fr="Une ",
                en="A ")),
        html.A(get_translation(fr="tuile", en="tile"), href="https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system", target="_blank"),
        html.Span(
            get_translation(
                fr="""
                est zone géographique de 600x600m. L'indicateur représenté sur le graphe présente pour chaque jour le changement dans la mobilité des utilisateurs par rapport à la normale.
                Plus précisément, c'est le nombre moyen de tuiles différentes visitées sur une journée divisé par cette valeur en temps normal.
                Les valeurs caractérisant la normalité ont été calculées sur les 45 jours précédant le début du graphe et pour chacun des jours de la semaine.
                """,
                en="""
                is a 600x600m geographical area. The metric shown on the graph indicates the daily evolution of the mobility to a normal period.
                More precisely, it is the average number of unique tiles visited during a day divided by that same value computed for a normal period.
                Values considered as normal were computed over the 45 days before the start of this graph and for each separate weekday.
                """)),
        dbc.Row([
            dbc.Col(dcc.Graph(id='movement',
                              figure=movement(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(
            get_translation(
                fr="Fraction des utilisateurs restant dans la même tuile toute la journée",
                en="Ratio of users staying in one tile for the whole day")),
        html.Span(
            get_translation(
                fr="Comme pour le graphe précédent, on considère des zones géographiques de 600x600m (",
                en="As for the previous graph, we consider 600x600m geographical areas (")),
        html.A(get_translation(fr="tuiles", en="tiles"), href="https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system", target="_blank"),
        html.Span(
            get_translation(
                fr=""").
                Cet indicateur donne une idée de la proportion de la population restant à (ou très proche de) son domicile toute la journée.
                Par exemple, si je rends visite à mes grand-parents qui habitent le village voisin à quelques kilomètres de chez moi,
                je vais traverser plusieurs tuiles sur la journée et ainsi faire partie des utilisateurs n'étant pas restés fixes pendant toute la journée.
                """,
                en=""").
                This metric gives insights about the fraction of the population who stays at home (or close to it) during the whole day.
                For instance, if I visit my grandparents in a village distant by a few kilometers, I will cross several tiles and thus
                will not belong to the users who stayed put for the whole day.
                """)),
        dbc.Row([
            dbc.Col(dcc.Graph(id='staying-put',
                              figure=staying_put(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(
            get_translation(
                fr="Lien de proportionnalité entre le nombre d'utilisateurs et la population réelle",
                en="Proportionality between the number of users and the population")),
        html.P(
            get_translation(
                fr="""
                Comparaison du nombre d'utilisateurs de Facebook observés en moyenne chaque jour de la semaine (calculé sur 45 jours avant le 14 avril 2020) et de la population de chaque arrondissement.
                On observe une relation linéaire respectée dans tous les arrondissements.
                Les arrondissements de Soignies et La Louvière ne figurent pas sur cette visualisation car les données fournies par Facebook ne tiennent pas compte de la division de Soignies de janvier 2019.
                """,
                en="""
                Comparison of the average number of Facebook users by weekday (computed over 45 days before April 14th 2020) with the population of each administrative unit.
                We observe a linear relation for all administrative units.
                Soignies and La Louvière are not shown on the visualization as Facebook data does not account for the split of Soignies in January 2019.
                """)),
        # html.H3(
        #     get_translation(
        #         fr="Changement de la densité d'utilisateurs par rapport à la normale",
        #         en="Change in the density of users wrt normality")),
        # html.P(
        #     get_translation(
        #         fr="""
        #         Les valeurs caractérisant la normalité ont été calculées sur les 90 jours précédant le début du graphe et pour chaque jour de la semaine.
        #         """,
        #         en="""
        #         Values considered as normal were computed over the 90 days before the start of this graph and for each weekday.
        #         """)),
        # dbc.Row([
        #     dbc.Col(dcc.Graph(id='population-evolution',
        #                       figure=population_evolution(),
        #                       config=dict(locale=str(get_locale())))),
        # ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='population-proportion',
                              figure=population_proportion(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_facebook)
        ]

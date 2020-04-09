from pages import AppMenu, AppLink
from pages.deaths.a import display_a
from pages.deaths.overmortality import display_overmortality

deaths_menu = AppMenu("Deaths", "/deaths", [
    AppLink("Overmortality", "/overmortality", display_overmortality),
    AppLink("A", "/a", display_a),
])
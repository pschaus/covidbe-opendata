from pages import AppMenu, AppLink
from pages.deaths.a import display_a

deaths_menu = AppMenu("Deaths", "/deaths", [
    AppLink("A", "/a", display_a),
])
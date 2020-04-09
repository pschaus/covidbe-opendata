from pages import AppMenu, AppLink
from pages.deaths.a import display_a
from pages.deaths.age_groups import display_age_groups


deaths_menu = AppMenu("Deaths", "/deaths", [
    AppLink("Age Groups", "/age_groups", display_age_groups),
    AppLink("A", "/a", display_a),
])
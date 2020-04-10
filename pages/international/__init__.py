from pages import AppMenu, AppLink
from pages.international.a import display_a,callback_a

international_menu = AppMenu("International", "/international", [
    AppLink("A", "/a", display_a, callback_a)
])
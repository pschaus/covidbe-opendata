from pages import AppMenu, AppLink

from pages.hospitals.hospitals import display_hospitals
hospitals_menu = AppMenu("Hospitals", "/hospitals", [
    AppLink("Hospitals", "/hospitals", display_hospitals),
])

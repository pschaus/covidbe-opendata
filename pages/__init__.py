from typing import List


class AppLink:
    def __init__(self, link_name: str, link: str, display_fn, callback_fn=(lambda app: None)):
        self.link_name = link_name
        self.link = link
        self.display_fn = display_fn
        self.callback_fn = callback_fn


class AppMenu:
    def __init__(self, name: str, base_link: str, children: List[AppLink]):
        self.name = name
        self.base_link = base_link
        self.children = children

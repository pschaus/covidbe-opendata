from functools import lru_cache
from flask_babel import get_locale


def translated_graph(f):
    @lru_cache(maxsize=None)
    def uf(lang):
        return f()
    return lambda: uf(str(get_locale()))
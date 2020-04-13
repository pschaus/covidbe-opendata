import threading


class ThreadSafeCache:
    class __ErrorMarker:
        def __init__(self, exception):
            self.exception = exception

    def __init__(self):
        self.lock = threading.Lock()
        self.cache = {}

    def get(self, key, creator):
        is_creating = False
        with self.lock:
            if key not in self.cache or isinstance(self.cache[key], self.__ErrorMarker):
                self.cache[key] = threading.Event()
                is_creating = True

        obj = self.cache[key]

        if is_creating:
            try:
                newobj = creator()
            except Exception as e:
                newobj = self.__ErrorMarker(e)
            self.cache[key] = newobj
            obj.set()
            obj = newobj

        while isinstance(obj, threading.Event):
            obj.wait()
            obj = self.cache[key]

        if isinstance(obj, self.__ErrorMarker):
            raise obj.exception

        return obj

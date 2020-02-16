import flask
import icetracker


class WSGI(flask.Flask):
    __instance = None
    __inited = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is True:
            return

        super().__init__("Flask iceTracker App")
        self.url_route()

        self.__class__.__inited = True

    def start(self, host: str, port: int, debug=False, thread=True):
        self.run(host=host, port=port, debug=debug, threaded=thread)

    def url_route(self):
        self.add_url_rule('/', 'static_site', self.data, methods=['GET'])

    @staticmethod
    def data():
        return icetracker.get_status(icetracker.Config().get_process_list())

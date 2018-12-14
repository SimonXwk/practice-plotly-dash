from functools import wraps


class FunctionMap(object):
    def __init__(self):
        self.func_map_set = set()
        self.app = None

    def init_app(self, app):
        self.app = app

    def add_rule(self, f, func_path, endpoint_url_dic):
        self.func_map_set.add(
            tuple(
                (rule, endpoint, f, func_path)
                for endpoint in endpoint_url_dic
                for rule in endpoint_url_dic[endpoint]
            )
        )
        print(f' _ [URL MAP] -> {self.func_map_set}')

    def register(self, endpoint_url_dic=None):
        def decorator(f):
            # This Part will run whenever its decorated function's module/package is imported (and wil only be executed once)
            # The function meta data will be exposed at this level
            # func_path = '.'.join((f.__module__.rsplit('.', 1)[-1], f.__name__))
            func_path = '.'.join((f.__module__, f.__name__))
            dic = endpoint_url_dic
            if not isinstance(dic, dict):
                try:
                    dic = dict(dic)
                except TypeError:
                    dic = {}
            self.add_rule(f, func_path, dic)

            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Do Nothing
                return f(*args, **kwargs)
            return decorated_function
        return decorator


fm = FunctionMap()

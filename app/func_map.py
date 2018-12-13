from functools import wraps

class FunctionMap(object):
    def __init__(self):
        self.func_map = {}

    def init_app(self, app):
        self.app = app

    def register(self, url_rules=None):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                rules = url_rules

                func_path = '.'.join((f.__module__.rsplit('.', 1)[-1], f.__name__))
                print(func_path, rules)
                
                
                if rules is None:
                    rules = []
                
                for url_rule in rules:
                    self.func_map[url_rule] = f
                return f(*args, **kwargs)
            return decorated_function
        return decorator


fm = FunctionMap()

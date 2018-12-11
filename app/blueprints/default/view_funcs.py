from app.helper import apply_template


@apply_template('index', title="Home")
def root_view_handler():
	# import inspect
	# import_name_module = __name__
	# import_string_function = inspect.getframeinfo(inspect.currentframe()).function
	# import_name = '.'.join((import_name_module, import_string_function))
	# print(' -> ', import_name)
	return None

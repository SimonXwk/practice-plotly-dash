from flask import render_template, request
from werkzeug.utils import import_string, cached_property
from functools import wraps
import plotly.offline as pyo


def apply_template(template=None, title=None, template_path_absolute=False, template_format='html', require_login=False):
	""" Function that accepts arguments passed to decorator and creates the Actual Decorator
	:param template: The Name of the template that will be used in flask.render_template(template)
	:param title: The Name of page title, passed to flask.render_template() as a parameter
	:param template_path_absolute: set to True when the template provided in its full path, no further process needed in this function
	:param template_format: default to .html if not provided, the template string will be checked if ends with template_format string
	:param require_login: whether login is required to have access to this view
	:return: Decorator function
	"""
	""" When using 'a decorator with arguments @something(your own args)', the process is as follows:
	1. 'templatified(your arguments)' is called (only once when using @... to create a decorator) and is expected to return the actual decorator function 'decorator'
	2. 'decorator(f)' is called and expected to return 'decorated_function(*args, **kwargs)' as the decorated function'myCallingFunc'
	3. 'decorated_function(*args, **kwargs)' is assign to the calling function 'myCallingFunc = decorated_function(myCallingFunc) '
	4. When calling 'myCallingFunc', 'decorated_function' will be executed
	step 1 is what defers the Decorator with argument from Decorator without argument
	this is equivalent to 
	"""

	def decorator(f):
		"""
		Actual Decorator that will decorate the decorated function
		:param f: function to be decorated
		:return: new decorated function
		"""

		@wraps(f)
		def decorated_function(*args, **kwargs):
			""" Process the template variable and construct the template_name for flask.render_template(template_name)
			Replace '.' in request.endpoint with '/'
			Case 1: No template provided, use the /endpoint.html
			Case 2: template provided as absolute path to root, template.html instead
			Case 3: template provided as a name only, use the /endpoint(take out last part) + template.html
			"""
			template_name, page_title = template, title

			# If template was not provided, use the endpoint path instead
			if template_name is None or str(template_name).strip() == '':
				template_name = request.endpoint.replace('.', '/')
			# If template was not given by its full path, then append the sub-folder name in front of it (which should be created using its blueprint's name)
			elif not template_path_absolute:
				template_name = '/'.join((request.blueprint, template_name)) if request.blueprint else template_name
			
			# If template does not end with the template_format provided, append it
			if template_name[-len(template_format):] != template_format:
				template_name = '.'.join((template_name, template_format))

			# By default add a title parameter to flask.render_template() function using dictionary unpacking
			if page_title is None:
				page_title = request.endpoint.replace('_', ' ').title()
				if not (request.blueprint is None):
					page_title = page_title.rsplit('.', 1)[1]
			default_context = {'title': page_title}  # Page title block in global jinja template block

			# Run the wrapped function, which should return a dictionary of Parameters
			context = f(*args, **kwargs)

			if not isinstance(context, dict):
				try:
					context = dict(context )
				except TypeError:
					# todo : Find a better way to deal with this scenario
					# print(f'!!! View Function not returning dict convertible object : [ {dic.__class__.__name__} ] returned by view function [ {f.__name__} ]  will be set to dict()')
					context = {}

			# Merge two dic, default dic will be overwritten if same key appears in the dictionary returned by the function
			context = {**default_context, **context}

			# Render the template
			return render_template(template_name, **context)

		if require_login:
			pass

		return decorated_function

	return decorator


# At rest class object could be used (called) when it's used
class LazyLoad(object):
	def __init__(self, import_name):
		self.__module__, self.__name__ = import_name.rsplit('.', 1)
		self.import_name = import_name
		self.fall_back_func = lambda: f'"{self.import_name}" is not callable object hence can not be used as view_func'

	@cached_property
	def imported_object(self):
		obj = import_string(self.import_name)
		print(f' . Lazy Loaded <{ self.import_name }> - {type(obj)}')
		return obj

	def __call__(self, *args, **kwargs):
		if hasattr(self.imported_object, '__call__'):
			return self.imported_object(*args, **kwargs)
		else:
			# TODO Add this to customized 500 error page
			return self.fall_back_func()


def request_arg(arg_name, default_value, type_func=str, test_func=None):
	arg = request.args.get(arg_name)
	if arg is None:
		return default_value

	if type_func != str:
		try:
			arg = type_func(arg)
		except (TypeError, ValueError):
			return default_value

	#  short-circuit if test_func is None
	if test_func == None or test_func(arg):
		return type_func(arg)
	return default_value
	


def plot_div_to_example_html(f):
	@apply_template('example', title="Plotly Demo")
	@wraps(f)
	def decorated_function(*args, **kwargs):
		figure = f(*args, **kwargs)
		plot_string = pyo.plot(figure, output_type='div')
		return dict(plot=plot_string)
	return decorated_function

from functools import wraps
from flask import render_template, request


def templatified(template=None, title=None, template_path_absolute=False, template_format='html', require_login=False):
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
			default_dic = {'title': page_title}  # Page title block in global jinja template block

			# Run the wrapped function, which should return a dictionary of Parameters
			dic = f(*args, **kwargs)

			if not isinstance(dic, dict):
				try:
					dic = dict(dic)
				except TypeError:
					# todo : Find a better way to deal with this scenario
					# print(f'!!! View Function not returning dict convertible object : [ {dic.__class__.__name__} ] returned by view function [ {f.__name__} ]  will be set to dict()')
					dic = {}

			# Merge two dic, default dic will be overwritten if same key appears in the dictionary returned by the function
			dic = {**default_dic, **dic}

			# Render the template
			return render_template(template_name, **dic)

		if require_login:
			pass

		return decorated_function

	return decorator

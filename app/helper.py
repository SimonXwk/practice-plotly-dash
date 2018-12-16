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
class LazyLoader(object):
	def __init__(self, import_name):
		self.__module__, self.__name__ = import_name.rsplit('.', 1)
		self.import_name = import_name
		self.fall_back_func = lambda: f'"{self.import_name}" is not callable object hence can not be used as view_func'

	@cached_property
	def imported_object(self):
		obj = import_string(self.import_name)
		print(f' . Lazy Loaded <{ self.import_name }> - {type(obj)}')
		if hasattr(obj, '__call__'):
			return obj
		# TODO Add this to customized 500 error page
		return self.fall_back_func

	def __call__(self, *args, **kwargs):
		return self.imported_object(*args, **kwargs)


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
	if test_func is None or test_func(arg):
		return type_func(arg)
	return default_value
	

def single_plot_to_html_div(f):
	@apply_template('example', title="Example")
	@wraps(f)
	def decorated_function(*args, **kwargs):
		figure = f(*args, **kwargs)
		config = {
			# no interactivity, for export or image generation
			'staticPlot': False,
			# base URL for the 'Edit in Chart Studio' (aka sendDataToCloud) mode bar button and the showLink/sendData on-graph link
			'plotlyServerURL': 'https://plot.ly',
			# change the title and axis titles
			'editable': True,
			'edits': {
				'annotationPosition': False,
				# just for annotations with arrows, change the length  and direction of the arrow
				'annotationTail': False,
				'annotationText': False,
				'axisTitleText': True,
				'colorbarPosition': False,
				'colorbarTitleText': False,
				'legendPosition': False,
				# edit the trace name fields from the legend
				'legendText': False,
				'shapePosition': False,
				# the global `layout.title`
				'titleText': True
			},

			# responsive: determines whether to change the layout size when window is resized. In v2, this option will be removed and will always be true.
			'responsive': True,
			# set the length of the undo/redo queue
			'queueLength': 0,

			# DO autosize once regardless of layout.autosize (use default width or height values otherwise)
			'autosizable': True,
			# if we DO autosize, do we fill the container or the screen?
			'fillFrame': False,
			# if we DO autosize, set the frame margins in percents of plot size
			'frameMargins': 0,

			# mousewheel or two-finger scroll zooms the plot
			'scrollZoom': False,
			# double click interaction (false, 'reset', 'autosize' or 'reset+autosize')
			'doubleClick': 'reset+autosize',
			# new users see some hints about interactivity
			'showTips': False,
			# enable axis pan/zoom drag handles
			'showAxisDragHandles': True,
			# enable direct range entry at the pan/zoom drag points (drag handles must be enabled above)
			'showAxisRangeEntryBoxes': True,

			# Add a text link to open this plot in plotly? This link shows up in the bottom right corner of the plo
			# This works identically to the newer ModeBar button controlled by `showSendToCloud` unless `sendData: false` is used.
			'showLink': False,
			# If we show a text link (`showLink: true`), does it contain data or just
			# a reference to a plotly cloud file? This option should only be used on
			# plot.ly or another plotly server, and is not supported by the newer ModeBar button `showSendToCloud`
			'sendData': True,
			# Should we include a ModeBar button, labeled "Edit in Chart Studio",
			'showSendToCloud': False,
			# text appearing in the sendData link
			'linkText': 'Online Export',

			# display the mode bar (true, false, or 'hover')
			'displayModeBar': 'hover',
			# remove/add mode bar button by name https://github.com/plotly/plotly.js/blob/master/src/components/modebar/buttons.js
			# toImage, sendDataToCloud, zoom2d, pan2d, select2d, lasso2d, zoomIn2d, autoScale2d, resetScale2d, hoverClosestCartesian, hoverCompareCartesian
			# zoom3d, pan3d, orbitRotation, tableRotation, resetCameraDefault3d, resetCameraLastSave3d, hoverClosest3d
			# zoomInGeo, zoomOutGeo, resetGeo, hoverClosestGeo
			# hoverClosestGl2d, hoverClosestPie, toggleHover, resetViews , toggleSpikelines, resetViewMapbox,
			'modeBarButtonsToRemove': [],
			'modeBarButtonsToAdd': [],
			'displaylogo': False,  # add the plotly logo on the end of the mode bar
			# fully custom mode bar buttons as nested array,
			# where the outer arrays represents button groups,
			# and the inner arrays have buttons config objects or names of default buttons
			# see ../components/modebar/buttons.js
			'modeBarButtons': False,
			# statically override options for toImage modebar button
			# allowed keys are format, filename, width, height, scale
			# see ../components/modebar/buttons.js
			'toImageButtonOptions': {},

			# watermark the images with the company's logo
			'watermark': False,
			# increase the pixel ratio for Gl plot images
			'plotGlPixelRatio': 2,
			# 'transparent' sets the background `layout.paper_color`,
			# 'opaque' blends bg color with white ensuring an opaque background
			# or any other custom function of gd
			'setBackground': 'transparent',

			# URL to topojson files used in geo charts
			'topojsonURL': 'https://cdn.plot.ly/',
			# If using an Mapbox Atlas server, set this option to ''
			'mapboxAccessToken': None,
			# 0: no logs | 1: warnings and errors, but not informational messages | 2: verbose logs
			'logging': 1,
			# Set global transform to be applied to all traces with no specification needed
			'globalTransforms': [],
			# Should be a string like 'en' or 'en-US'
			'locale': 'en-US',
			'locales': {}
		}
		plot_string = pyo.plot(figure, output_type='div', config=config)
		return dict(plot=plot_string)
	return decorated_function

import os
import webapp2
import jinja2
import urllib

from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import ndb

from slimmer import html_slimmer

from jinja2htmlcompress import SelectiveHTMLCompress

env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape', 'jinja2htmlcompress.HTMLCompress', 'jinja2htmlcompress.SelectiveHTMLCompress'],
	autoescape = True)

titles = [
        "Topsoil",
	"Oh My Giraffe",
        "Bring Your Own Book",
]

projects = [
	"work/topsoil",
	"work/oh-my-giraffe",
	"work/bring-your-own-book",
]

def get_fragment(resource):

	path = os.path.join(os.path.dirname(__file__), "static/fragments/%s.html" % resource)
	if os.path.isfile(path):
		fragment = file(path, "r").read().decode("utf8")
		markup = html_slimmer(fragment)
		return markup

def render_document(resource, template):

	values = {}
	resource = "work" if not resource else resource
	parts = resource.split("/")
	section = parts[0]

	title = None if resource == "work" else resource
	try:
		title = title if not parts[1] else parts[1]
		title = " ".join(title.split("-"))
	except IndexError:
		pass

	values["css"] = "static/css/main.css"
	values["js"] = "templates/javascript.html"
	values["title"] = title
	values["resource"] = resource.split("/")
	values["name"] = section

	fragment = get_fragment(resource)
	values["fragment"] = fragment
	try:
		index = projects.index(resource)
		if index is not None:

			values["project"] = True
			values["title"] = titles[index]

			pill = {}
			pill["progress"] = str((index + 1) / float(len(projects)) * 100)
			pill["index"] = index + 1
			pill["length"] = len(projects)

			prev_index = index - 1
			if prev_index >= 0:
				pill["prev"] = projects[prev_index]

			next_index = index + 1
			if next_index < len(projects):
				pill["next"] = projects[next_index]

			values["pill"] = pill

	except ValueError:
		pass

	markup = template.render(values)
	return markup

class FragmentHandler(webapp2.RequestHandler):
	def get(self, resource):
		template = env.get_template("templates/fragment.html")
		markup = render_document(resource, template)
		self.response.out.write(markup)

class ResourceHandler(webapp2.RequestHandler):
	def get(self, resource):
		if resource == "work":
			self.redirect("/")
		template = env.get_template("templates/base.html")
		markup = render_document(resource, template)
		self.response.out.write(markup)

application = webapp2.WSGIApplication([
	(r'/fragment/([^\s]*)', FragmentHandler),
	(r'/([^\s]*)', ResourceHandler),
], debug = True)

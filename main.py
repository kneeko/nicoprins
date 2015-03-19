import os
import webapp2
import jinja2
import urllib

from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import ndb

from jinja2htmlcompress import SelectiveHTMLCompress

env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape', 'jinja2htmlcompress.HTMLCompress', 'jinja2htmlcompress.SelectiveHTMLCompress'],
	autoescape = True)

projects = [
	"work/oh-my-giraffe",
	"work/radio-hyrule",
	"work/theo-prins",
	"work/pt-art-and-frame",
	"work/brainstorm",
	"work/by-hand-and-eye",
]

def get_fragment(section):
	path = os.path.join(os.path.dirname(__file__), "static/fragments/%s.html" % section)
	exists = os.path.isfile(path) 
	if exists:
		fragment = file(path, "r").read().decode("utf8")
		return fragment

class FragmentHandler(webapp2.RequestHandler):
	def get(self, resource):

		if not resource:
			resource = "work"
	
		template = env.get_template("templates/fragment.html")
		values = {}

		parts = resource.split("/")
		section = parts[0]

		fragment = get_fragment(resource)
		if fragment:
			values["resource"] = resource.split("/")
			values["name"] = section
			values["fragment"] = fragment

			try:
				index = projects.index(resource)
				if index is not None:
					values["project"] = True
					pill = {}
					pill["progress"] = str((index + 1) / float(len(projects)) * 100) + "%"
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
				print("showing other")

			markup = template.render(values)
			self.response.out.write(markup)

class ResourceHandler(webapp2.RequestHandler):
	def get(self, resource):

		if resource == "work":
			self.redirect("/")
		elif not resource:
			resource = "work"

		title = None if resource == "work" else resource
	
		template = env.get_template("templates/base.html")
		values = {}

		parts = resource.split("/")
		section = parts[0]

		try:
			title = title if not parts[1] else parts[1]
			title = " ".join(title.split("-"))
		except IndexError:
			print("ya")

		fragment = get_fragment(resource)
		if not fragment:
			self.redirect("/")
		else:
			values["resource"] = resource.split("/")
			values["name"] = section
			values["fragment"] = fragment
			values["css"] = "static/css/main.css"
			values["js"] = "templates/javascript.html"
			values["title"] = title
			try:
				index = projects.index(resource)
				if index is not None:
					values["project"] = True
					pill = {}
					pill["progress"] = str((index + 1) / float(len(projects)) * 100) + "%"
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
				print("showing other")

			markup = template.render(values)
			self.response.out.write(markup)

application = webapp2.WSGIApplication([
	(r'/fragment/([^\s]*)', FragmentHandler),
	(r'/([^\s]*)', ResourceHandler),
], debug = True)
#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")
    def post(self):
        convert_from = self.request.get("Convert_from")
        convert_to = self.request.get("Convert_to")
        original_amount = float(self.request.get("number"))

        conversions = {
                "mm": {"mm": 1.0, "cm": 1.0/10.0, "m": 1.0/1000.0, "km": 1.0/1000000.0},
                "cm": {"mm": 10.0, "cm": 1.0, "m": 1.0/100.0, "km": 1.0/100000.0},
                "m":  {"mm": 1000.0, "cm": 100.0, "m": 1.0, "km": 1.0/1000.0},
                "km": {"mm": 100000.0, "cm": 10000.0, "m": 1000.0, "km": 1.0},
              }

        convert = conversions[convert_from][convert_to]
        x= original_amount*convert

        view_vars = {
           "x":x,
            "convertedfrom": convert_from,
            "convertedto": convert_to,
            "original": original_amount,
       }
        return self.render_template("converted.html", view_vars)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)

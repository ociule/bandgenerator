#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from band import Band
import os


import webapp2
# @TODO this will not work anymore!
from google.appengine.ext.webapp import template
from google.appengine.ext import db


# Set the debug level
_DEBUG = True


class BaseRequestHandler(webapp2.RequestHandler):
  """Base request handler extends webapp.Request handler

     It defines the generate method, which renders a Django template
     in response to a web request
  """

  def generate(self, template_name, template_values={}):
    """Generate takes renders and HTML template along with values
       passed to that template

       Args:
         template_name: A string that represents the name of the HTML template
         template_values: A dictionary that associates objects with a string
           assigned to that object to call in the HTML template.  The defualt
           is an empty dictionary.
    """

    print 111
    latest_bands = db.GqlQuery("SELECT * FROM Band ORDER BY created DESC LIMIT 3")
    latest_fixed = []
    for band in latest_bands:
        band.fix_encoding()
        latest_fixed.append(band)
    values = {'latest_bands': latest_fixed}
    template_values.update(values)
    
    # Construct the path to the template
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, 'templates', template_name)

    # Respond to the request by rendering the template
    self.response.out.write(template.render(path, template_values, debug=_DEBUG))

class MainHandler(BaseRequestHandler):

  def get(self):
    band = Band()
    band.randomize()
    band.put()
    band.fix_encoding()
    self.generate('index.html', template_values={'page_title': 'Band Generator - Generate a band!',
                                                'band' : band,
                                                })

class ViewHandler(BaseRequestHandler):

  def get(self, band_id):
    try:
      band_id = int(band_id)
    except ValueError:
      self.generate('index.html', template_values={'page_title': '404 - Band Generator - Generate a band!',
                                                  'band' : {'name': '404'},
                                                  })
      return

    band = Band.get_by_id(band_id)
    band.fix_encoding()
    band_name = band.name if band and band.name else ""
    self.generate('index.html', template_values={'page_title': band_name + 'Band Generator - Generate a band!',
                                                'band' : band,
                                                'disqus': True,
                                                })


class AboutHandler(BaseRequestHandler):

  def get(self):
    self.generate('about.html', template_values={'page_title': 'About - Band Generator - Generate a band!',
                                                'disqus': True,
                                                })
_URLS = [('/',              MainHandler),
         ('/about/?',        AboutHandler),
         ('/band/',         MainHandler),
         ('/band/([^/]+)',  ViewHandler)]

app = webapp2.WSGIApplication(_URLS,
                                debug=_DEBUG)

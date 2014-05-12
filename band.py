#!/usr/bin/python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
from google.appengine.ext import db


class Band(db.Model):
  """Band model
  """
  created = db.DateTimeProperty(auto_now_add=True)
  debut_album_cover_path = db.StringProperty()
  debut_album_cover_link = db.StringProperty()
  name = db.StringProperty()
  debut_album_name = db.StringProperty()

  def randomize(self):
    """Generate random band.
       Band name : Wikipedia Special:Random
       Debut album name : Wikiquote Special:Random
       Debut album cover : Flickr, "last seven day page", choose the 3rd pic
    """
    self.name = Band.getRandomWikipediaPageTitle()
    self.debut_album_name = Band.getRandomWikiquotePageTitle()
    self.debut_album_cover_path, self.debut_album_cover_link = Band.getRandomFlickrPhotoPath()
    
  @staticmethod
  def getRandomWikiMediaPageTitle(
    random_url = "http://en.wikipedia.org/wiki/Special:Random",
    end_title_token = "- Wikipedia, the free",
    ):
    retries = 0
    max_retries = 5
    while retries < max_retries:
      random_page = urlfetch.fetch(random_url, payload=None, method=urlfetch.GET, headers={}, allow_truncated=True, follow_redirects=True)
      content = unicode(random_page.content.decode("latin-1"))
      ix_title_start = content.find("<title>")
      ix_title_end = content.find("</title>")
    
      if ix_title_start > -1 and ix_title_end > -1 and ix_title_start < ix_title_end:
        title = content[ix_title_start+7:ix_title_end]
        ix_title_end = title.find(end_title_token)
        if ix_title_end > -1:
          title = title[0:ix_title_end]
          return title
      retries += 1
      
  @staticmethod
  def getRandomWikipediaPageTitle():
    return Band.getRandomWikiMediaPageTitle(
      random_url = "http://en.wikipedia.org/wiki/Special:Random",
        end_title_token = "- Wikipedia, the free")

  @staticmethod
  def getRandomWikiquotePageTitle():
    return Band.getRandomWikiMediaPageTitle(random_url = "http://en.wikiquote.org/wiki/Special:Random",
      end_title_token = "- Wikiquote")

  @staticmethod
  def getRandomFlickrPhotoPath():
    random_url = "https://www.flickr.com/explore/interesting/7days/"
    first_image_start = "\"https://farm"
    first_image_end   = ".jpg\" "

    first_link_start  = "href=\"/photos/"
    first_link_end    = "\" "

    retries = 0
    max_retries = 5
    while retries < max_retries:
      random_page = urlfetch.fetch(random_url, payload=None, method=urlfetch.GET, headers={}, allow_truncated=True, follow_redirects=True)
      print random_page.content[:100]
      content = unicode(random_page.content.decode("latin_1"))
      
      ix_first_image_start = content.find(first_image_start)

      if ix_first_image_start > -1:        
        path = content[ix_first_image_start+11:]

        ix_first_link_start = path.find(first_link_start)
        if ix_first_link_start > -1:

          link = path[ix_first_link_start+6:]
          ix_first_link_end = link.find(first_link_end)
          if ix_first_link_end > -1:
            link = link[0:ix_first_link_end]

            ix_first_image_start = path.find(first_image_start)
            if ix_first_image_start > -1:
              path = path[ix_first_image_start+1:]
              ix_title_end = path.find(first_image_end)
              path = path[0:ix_title_end+4]
              return path, link
      retries += 1
      
  def fix_encoding(self):
    self.name = self.name.encode('latin-1')
    self.debut_album_name = self.debut_album_name.encode('latin-1')

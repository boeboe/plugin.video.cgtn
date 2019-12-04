# pylint: disable=bare-except
"""Module with generic configuration for the CGTN Kodi plugin """
import os
import json
import xbmc

class Config(object):
    """Class with all the configuration constants"""

    def __init__(self):
        pass

    try:
        import xbmcaddon
        addon = xbmcaddon.Addon()
        path = addon.getAddonInfo('path')
        addon = None
    except:
        xbmc.log("Retrospect: using os.getcwd()", xbmc.LOGDEBUG)
        path = os.getcwd()
        pathDetection = "os.getcwd()"

    if isinstance(path, bytes):
        path = path.decode('utf-8')

    rootDir = path.replace(";", "").rstrip(os.sep)
    dataDir = os.path.join(rootDir, "resources", "data")
    mediaDir = os.path.join(rootDir, "resources", "media")
    fanart = os.path.join(rootDir, "resources", "fanart.jpg")

class Categories(object):

    CATEGORIES = json.loads("""{
        "livestreams": {
            "name": "Livestreams",
            "poster": "poster_cgtn_live.png"
        },
        "channels": {
            "name": "Channels",
            "poster": "poster_cgtn_channels.png"
        },
        "news": {
            "name": "News",
            "poster": "poster_cgtn_news.png"
        }
    }""")

    @classmethod
    def get_categories(cls):
        return cls.CATEGORIES.iterkeys()

    @classmethod
    def get_name(cls, category):
        return cls.CATEGORIES[category]['name']

    @classmethod
    def get_poster(cls, category):
        return cls.CATEGORIES[category]['poster']

    @classmethod
    def get_thumb(cls, category):
        return cls.CATEGORIES[category]['thumb']

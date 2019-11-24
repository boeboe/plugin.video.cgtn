
import os
import xbmc

class CGTNConfig:
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

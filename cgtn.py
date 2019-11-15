# -*- coding: utf-8 -*-
# Module: default
# Author: Boeboe
# Created on: 14.11.2019
# License: CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0

import sys
import os
from urllib import urlencode
from urlparse import parse_qsl
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import json

from resources.lib.cgtnconfig import Config

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

with open(os.path.join(Config.dataDir, "menu.json")) as json_menu:
    VIDEOS = json.load(json_menu)

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    return VIDEOS.iterkeys()


def get_videos(category):
    return VIDEOS[category]


def list_categories():
    xbmcplugin.setPluginCategory(_handle, 'CGTN News')
    xbmcplugin.setContent(_handle, 'videos')

    categories = get_categories()
    for category in categories:
        list_item = xbmcgui.ListItem(label=category, iconImage='DefaultFolder.png')
        list_item.setInfo('video', {'title': category,
                                    'genre': category,
                                    'mediatype': 'video'})
        thumb = os.path.join(Config.mediaDir, "thumb_cgtn_live.png")
        poster = os.path.join(Config.mediaDir, "poster_cgtn_live.png")
        fanart = Config.fanart
        list_item.setArt({'thumb': thumb,
                          'icon': thumb,
                          'poster': poster,
                          'fanart': fanart})

        # plugin://plugin.video.cgtn/?action=listing&category=Livestream
        url = get_url(action='listing', category=category)
        xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=list_item, isFolder=True)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    xbmcplugin.setPluginCategory(_handle, category)
    xbmcplugin.setContent(_handle, 'videos')

    videos = get_videos(category)
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['name'])
        list_item.setInfo('video', {'title': video['name'],
                                    'genre': video['genre'],
                                    'mediatype': 'video'})
        thumb = os.path.join(Config.mediaDir, video['thumb'])
        poster = os.path.join(Config.mediaDir, video['poster'])
        fanart = Config.fanart
        list_item.setArt({'thumb': thumb,
                          'icon': thumb,
                          'poster': poster,
                          'fanart': fanart})
        list_item.setProperty('IsPlayable', 'true')

        # plugin://plugin.video.cgtn/?action=play&video=httpx://example.com/dummy.m3u8
        url = get_url(action='play', video=video['video'])
        xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=list_item, isFolder=False)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(handle=_handle, succeeded=True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))

    # Valid routing cases:
    #  - Initial call from Kodi: 
    #       plugin://plugin.video.cgtn
    #  - When user goes into a category: 
    #       plugin://plugin.video.cgtn?action=listing&category=Livestream
    #  - When user plays an item
    #       plugin://plugin.video.cgtn?action=play&video=httpx://example.com/dummy.m3u8
    if params:
        if params['action'] == 'listing':
            list_videos(params['category'])     
        elif params['action'] == 'play':
            play_video(params['video'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
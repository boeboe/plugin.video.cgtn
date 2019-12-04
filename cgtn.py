"""Main entry for this Kodi plugin """
# -*- coding: utf-8 -*-
# Module: default
# Author: Boeboe
# Created on: 14.11.2019
# License: CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0

import os
import sys
from urllib import urlencode
from urlparse import parse_qsl

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.channel import Channel, ChannelParser

from config import Config, Categories

PLUGIN_URL = sys.argv[0]
PLUGIN_HANDLE = int(sys.argv[1])

def log(message):
    xbmc.log("============== {}".format(message), level=xbmc.LOGNOTICE)

def get_url(**kwargs):
    """Get a valid Kodi URL with encoded parameters """
    return '{0}?{1}'.format(PLUGIN_URL, urlencode(kwargs))

def list_categories():
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'CGTN Addon')
    xbmcplugin.setContent(PLUGIN_HANDLE, 'videos')
    for cat in Categories.get_categories():
        list_item = xbmcgui.ListItem(label=Categories.get_name(cat), iconImage='DefaultFolder.png')
        list_item.setInfo('video', {'title': Categories.get_name(cat),
                                    'genre': Categories.get_name(cat),
                                    'mediatype': 'video'})

        poster = os.path.join(Config.mediaDir, Categories.get_poster(cat))
        list_item.setArt({'poster': poster, 'fanart': Config.fanart})

        # plugin://plugin.video.cgtn/?action=listing&category=livestream|channels|news
        url = get_url(action='listing', category=cat)
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=True)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def list_livestreams():
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'Livestreams')
    xbmcplugin.setContent(PLUGIN_HANDLE, 'videos')

    parser = ChannelParser()
    for channel in Channel.get_all():
        video = parser.parse_current_live(channel)
        list_item = xbmcgui.ListItem(label=channel["name"])
        list_item.setInfo('video', {'title': channel["name"],
                                    'genre': "Livestream",
                                    'plot': video.title,
                                    'mediatype': 'movie'})
        poster_file = "poster_cgtn_{}.png".format(channel["prefix"])
        poster = os.path.join(Config.mediaDir, poster_file)
        list_item.setArt({'poster': poster, 'fanart': Config.fanart})
        list_item.setProperty('IsPlayable', 'true')

        # plugin://plugin.video.cgtn/?action=play&video=httpx://example.com/dummy.m3u8
        url = get_url(action='play', video=video.video_url)
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=False)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def router(paramstring):
    params = dict(parse_qsl(paramstring))

    if params:
        if params['action'] == 'listing' and params['category'] == 'livestreams':
            list_livestreams()
    else:
        list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])

"""Main entry for this Kodi plugin """
# -*- coding: utf-8 -*-
# Module: default
# Author: Boeboe
# Created on: 14.11.2019
# License: CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0

import os
import sys
import time
from urllib import urlencode
from urlparse import parse_qsl

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.channel import Channel, ChannelParser
from resources.lib.other.section import SectionSP, SectionFR, SectionAR, SectionRU, SectionParser
from resources.lib.english.newscategory import NewsCategory, NewsCategoryParser
from resources.lib.english.news import NewsParser

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
    for video in parser.parse_all_current_live():
        duration = (int(video.end_date) - int(video.start_date))/1000
        premiered = time.strftime('%Y-%m-%d', time.localtime(int(video.start_date)/1000))
        channel = Channel.get_by_id(video.channel_id)
        list_item = xbmcgui.ListItem(label=channel['name'])
        list_item.setInfo('video', {'title': channel['name'],
                                    'genre': 'Livestream',
                                    'duration': duration,
                                    'premiered': premiered,
                                    'plotoutline': video.title,
                                    'plot': video.title,
                                    'mediatype': 'movie'})
        poster_file = "poster_cgtn_{}.png".format(channel['prefix'])
        poster = os.path.join(Config.mediaDir, poster_file)
        list_item.setArt({'poster': poster, 'fanart': Config.fanart})
        list_item.setProperty('IsPlayable', 'true')

        # plugin://plugin.video.cgtn/?action=play&video=httpx://example.com/dummy.m3u8
        url = get_url(action='play', video=video.video_url)
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=False)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def list_channels():
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'Channels')
    xbmcplugin.setContent(PLUGIN_HANDLE, 'videos')
    for channel in Channel.get_all():
        list_item = xbmcgui.ListItem(label=channel['name'], iconImage='DefaultFolder.png')
        list_item.setInfo('video', {'title': channel['name'],
                                    'genre': channel['name'],
                                    'mediatype': 'video'})

        poster_file = "poster_cgtn_{}.png".format(channel['prefix'])
        poster = os.path.join(Config.mediaDir, poster_file)
        list_item.setArt({'poster': poster, 'fanart': Config.fanart})

        # plugin://plugin.video.cgtn/?action=listing&channel=en|sp|fr|ar|ru|do
        url = get_url(action='listing', channel=channel['key'])
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=True)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def list_channel_videos(channel_key):
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'Channel Videos')
    xbmcplugin.setContent(PLUGIN_HANDLE, 'videos')

    channel = Channel.get_by_key(channel_key)
    parser = ChannelParser()
    videos = parser.parse_history_from_now(channel, hours=12)
    for video in videos:
        duration = (int(video.end_date) - int(video.start_date))/1000
        premiered = time.strftime('%Y-%m-%d', time.localtime(int(video.start_date)/1000))
        list_item = xbmcgui.ListItem(label=video.title)
        list_item.setInfo('video', {'title': video.title,
                                    'genre': 'Channel Program',
                                    'duration': duration,
                                    'premiered': premiered,
                                    'plotoutline': video.title,
                                    'plot': video.title,
                                    'mediatype': 'movie'})
        poster_file = "poster_cgtn_{}.png".format(channel['prefix'])
        poster = os.path.join(Config.mediaDir, poster_file)
        list_item.setArt({'poster': poster, 'fanart': Config.fanart})
        list_item.setProperty('IsPlayable', 'true')

        # plugin://plugin.video.cgtn/?action=play&video=httpx://example.com/dummy.m3u8
        url = get_url(action='play', video=video.video_url)
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=False)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def list_news_channels():
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'News')
    xbmcplugin.setContent(PLUGIN_HANDLE, 'videos')
    for channel in Channel.get_all()[:-1]:
        list_item = xbmcgui.ListItem(label=channel['name'], iconImage='DefaultFolder.png')
        list_item.setInfo('video', {'title': channel['name'],
                                    'genre': channel['name'],
                                    'mediatype': 'video'})

        poster_file = "poster_cgtn_{}.png".format(channel['prefix'])
        poster = os.path.join(Config.mediaDir, poster_file)
        list_item.setArt({'poster': poster, 'fanart': Config.fanart})

        # plugin://plugin.video.cgtn/?action=listing&newschannel=en|sp|fr|ar|ru
        url = get_url(action='listing', newschannel=channel['key'])
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=True)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def list_newssections_other(channel_key):
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'News Sections')
    xbmcplugin.setContent(PLUGIN_HANDLE, 'videos')

    sections = []

    if channel_key == "sp":
        sections = SectionSP.get_all()
    elif channel_key == "fr":
        sections = SectionFR.get_all()
    elif channel_key == "ar":
        sections = SectionAR.get_all()
    elif channel_key == "ru":
        sections = SectionRU.get_all()

    for section in sections:
        list_item = xbmcgui.ListItem(label=section['name'], iconImage='DefaultFolder.png')
        list_item.setInfo('video', {'title': section['name'],
                                    'genre': section['name_en'],
                                    'mediatype': 'video'})

        poster_file = "poster_cgtn_{}.png".format(Channel.get_by_key(channel_key)['prefix'])
        poster = os.path.join(Config.mediaDir, poster_file)
        list_item.setArt({'poster': poster, 'fanart': Config.fanart})

        # plugin://plugin.video.cgtn/?action=listing&newschannel=en|sp|fr|ar|ru
        url = get_url(action='listing', newschannel=channel_key, section=section['id'])
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=True)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def list_newssection_videos_other(channel_key, section_id):
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'News Section Videos')
    xbmcplugin.setContent(PLUGIN_HANDLE, 'videos')

    videos = []
    parser = SectionParser()

    if channel_key == "sp":
        videos = parser.parse_section_sp(section_id)
        genre = SectionSP.get_by_id(section_id)["name_en"]
    elif channel_key == "fr":
        videos = parser.parse_section_fr(section_id)
        genre = SectionFR.get_by_id(section_id)["name_en"]
    elif channel_key == "ar":
        videos = parser.parse_section_ar(section_id)
        genre = SectionAR.get_by_id(section_id)["name_en"]
    elif channel_key == "ru":
        videos = parser.parse_section_ru(section_id)
        genre = SectionRU.get_by_id(section_id)["name_en"]

    for video in videos:
        list_item = xbmcgui.ListItem(label=video.title)
        premiered = time.strftime('%Y-%m-%d', time.localtime(video.publish_date/1000))
        list_item.setInfo('video', {'title': video.title,
                                    'genre': genre,
                                    'director': video.editor,
                                    'premiered': premiered,
                                    'plotoutline': video.title,
                                    'plot': video.details,
                                    'mediatype': 'movie'})
        list_item.setArt({'poster': video.img_url, 'fanart': Config.fanart})
        list_item.setProperty('IsPlayable', 'true')

        # plugin://plugin.video.cgtn/?action=play&video=httpx://example.com/dummy.m3u8
        url = get_url(action='play', video=video.video_url)
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=False)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def list_newscategories_en(channel_key):
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'News Categories')
    xbmcplugin.setContent(PLUGIN_HANDLE, 'videos')

    parser = NewsCategoryParser
    categories = parser.parse_categories()

    for category in categories:
        list_item = xbmcgui.ListItem(label=category.name, iconImage='DefaultFolder.png')
        list_item.setInfo('video', {'title': category.name,
                                    'genre': category.name,
                                    'mediatype': 'video'})

        poster_file = "poster_cgtn_{}.png".format(Channel.get_by_key(channel_key)['prefix'])
        poster = os.path.join(Config.mediaDir, poster_file)
        list_item.setArt({'poster': poster, 'fanart': Config.fanart})

        # plugin://plugin.video.cgtn/?action=listing&newschannel=en&
        #   newscategory=https://www.cgtn.com/nature&hassubs=True
        url = get_url(action='listing', newschannel=channel_key, newscategory=category.url,
                      hassubs=category.has_subcatagories)
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=True)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def list_newscategory_videos_en(channel_key, category_url, has_subcatagories):
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'News Category Videos')
    xbmcplugin.setContent(PLUGIN_HANDLE, 'videos')

    if has_subcatagories:
        parser = NewsCategoryParser
        sub_categories = parser.parse_sub_categories(category_url)

        for sub_category in sub_categories:
            list_item = xbmcgui.ListItem(label=sub_category.name, iconImage='DefaultFolder.png')
            list_item.setInfo('video', {'title': sub_category.name,
                                        'genre': sub_category.name,
                                        'mediatype': 'video'})

            poster_file = "poster_cgtn_{}.png".format(Channel.get_by_key(channel_key)['prefix'])
            poster = os.path.join(Config.mediaDir, poster_file)
            list_item.setArt({'poster': poster, 'fanart': Config.fanart})

            # plugin://plugin.video.cgtn/?action=listing&newschannel=en&
            #   newscategory=https://www.cgtn.com/nature/animal.html&hassubs=False
            url = get_url(action='listing', newschannel=channel_key, newscategory=sub_category.url, hassubs=False)
            xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=True)

    videos = []
    parser = NewsParser()
    videos = parser.parse_videos(category_url)

    for video in videos:
        premiered = time.strftime('%Y-%m-%d', time.localtime(int(video.publish_date)/1000))
        genre = category_url.split("/")[-1].split(".")[0].split("?")[0].strip().capitalize()
        list_item = xbmcgui.ListItem(label=video.title)
        list_item.setInfo('video', {'title': video.title,
                                    'genre': genre,
                                    'premiered': premiered,
                                    'plotoutline': video.title,
                                    'plot': video.title,
                                    'mediatype': 'movie'})
        list_item.setArt({'poster': video.img_url, 'fanart': Config.fanart})
        list_item.setProperty('IsPlayable', 'true')

        # plugin://plugin.video.cgtn/?action=play&video=httpx://example.com/dummy.m3u8
        url = get_url(action='play', video=video.video_url)
        xbmcplugin.addDirectoryItem(handle=PLUGIN_HANDLE, url=url, listitem=list_item, isFolder=False)

    xbmcplugin.addSortMethod(PLUGIN_HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(handle=PLUGIN_HANDLE, succeeded=True, listitem=play_item)

def router(paramstring):
    params = dict(parse_qsl(paramstring))

    if params:
        if params['action'] == 'listing':
            if 'category' in params:
                if params['category'] == 'livestreams':
                    list_livestreams()
                elif params['category'] == 'channels':
                    list_channels()
                elif params['category'] == 'news':
                    list_news_channels()
            elif 'channel' in params:
                list_channel_videos(params['channel'])
            elif 'newschannel' in params:
                if params['newschannel'] in ["sp", "fr", "ar", "ru"]:
                    if 'section' in params:
                        list_newssection_videos_other(params['newschannel'], params['section'])
                    else:
                        list_newssections_other(params['newschannel'])
                elif params['newschannel'] == "en":
                    if 'newscategory' in params:
                        list_newscategory_videos_en(params['newschannel'], params['newscategory'], params['hassubs'])
                    else:
                        list_newscategories_en(params['newschannel'])
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])

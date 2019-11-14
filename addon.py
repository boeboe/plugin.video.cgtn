import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

lifestream_list = [("https://news.cgtn.com/resource/live/english/cgtn-news.m3u8", 'English'),
        ("https://news.cgtn.com/resource/live/french/cgtn-f.m3u8", 'French'),
        ("https://news.cgtn.com/resource/live/espanol/cgtn-e.m3u8", 'Spanish'),
        ("https://news.cgtn.com/resource/live/arabic/cgtn-a.m3u8", 'Arabic'),
        ("https://news.cgtn.com/resource/live/russian/cgtn-r.m3u8", 'Russian'),
        ("https://news.cgtn.com/resource/live/document/cgtn-doc.m3u8", "Documentary")]

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'folder', 'foldername': 'Livestream'})
    li = xbmcgui.ListItem('Livestream', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'Videos'})
    li = xbmcgui.ListItem('Videos', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    foldername = args['foldername'][0]

    if foldername == 'Livestream':
        for lifestream_url, lifestream_name in lifestream_list:
            li = xbmcgui.ListItem(lifestream_name, iconImage='DefaultVideo.png')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=lifestream_url, listitem=li)
    
    xbmcplugin.endOfDirectory(addon_handle)

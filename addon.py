import sys
import time
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import requests

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

lifestream_list = [('https://news.cgtn.com/resource/live/english/cgtn-news.m3u8', 'English', '1'),
        ('https://news.cgtn.com/resource/live/french/cgtn-f.m3u8', 'French', '3'),
        ('https://news.cgtn.com/resource/live/espanol/cgtn-e.m3u8', 'Spanish', '2'),
        ('https://news.cgtn.com/resource/live/arabic/cgtn-a.m3u8', 'Arabic', '4'),
        ('https://news.cgtn.com/resource/live/russian/cgtn-r.m3u8', 'Russian', '5'),
        ('https://news.cgtn.com/resource/live/document/cgtn-doc.m3u8', "Documentary", '6')]

channel_program_url = 'https://api.cgtn.com/website/api/live/channel/epg/list?'

xbmcplugin.setContent(addon_handle, 'videos')

current_milli_time = lambda: int(round(time.time() * 1000))

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def get_day_start_epoch():
    start_str = time.strftime( "%m/%d/%Y" ) + " 00:00:00"
    return int( time.mktime( time.strptime( start_str, "%m/%d/%Y %H:%M:%S" ) ) ) * 1000

def get_day_end_epoch():
    end_str = time.strftime( "%m/%d/%Y ") + " 23:59:59"
    return int( time.mktime( time.strptime( end_str, "%m/%d/%Y %H:%M:%S" ) ) ) * 1000

def get_schedule(channel_id):
    begin_day = get_day_start_epoch()
    end_day = get_day_end_epoch()
    schedule = ""
    r = requests.get('https://api.cgtn.com/website/api/live/channel/epg/list?channelId={}&startTime={}&endTime={}'.format(channel_id, begin_day, end_day))
    if r.status_code == 200:
        res = r.json()
        for item in res['data']:
            begin = item['startTime']
            begin_hm = time.strftime('%H:%M', time.gmtime(float(item['startTime'])/1000))
            end = item['endTime']
            end_hm = time.strftime('%H:%M', time.gmtime(float(item['endTime'])/1000))
            name = item['name'].lower().capitalize()
            if int(begin) < int(current_milli_time()) < int(end):
                schedule = schedule + '[B]' + begin_hm + ' - ' + end_hm + ' : ' + name + ' [running][/B]\n'
            else:
                schedule = schedule + begin_hm + ' - ' + end_hm + ' : ' + name + '\n'
    return schedule

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'folder', 'foldername': 'Livestream'})
    li = xbmcgui.ListItem('Livestream', iconImage='DefaultFolder.png')

    info = {
        'plot': 'This is livestream program of today',
    }
    li.setInfo('video', info)

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'Videos'})
    li = xbmcgui.ListItem('Videos', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    foldername = args['foldername'][0]

    if foldername == 'Livestream':
        for lifestream_url, lifestream_name, channel_index in lifestream_list:
            li = xbmcgui.ListItem(lifestream_name, iconImage='DefaultVideo.png')

            info = {
                'plot': get_schedule(channel_index)
            }
            li.setInfo('video', info)

            xbmcplugin.addDirectoryItem(handle=addon_handle, url=lifestream_url, listitem=li)
    
    xbmcplugin.endOfDirectory(addon_handle)

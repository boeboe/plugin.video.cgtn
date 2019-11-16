from resources.lib.cgtnschedule import ScheduleParser

sp = ScheduleParser("https://api.cgtn.com/website/api/live/channel/epg/list?channelId=1")
print(sp.get_current_play())

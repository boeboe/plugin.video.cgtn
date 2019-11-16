import os
import requests
import time

class ScheduleParser:
    """Class to parse the TV schedule"""

    def __init__(self, url):
        self.url = url
        pass

    def get_now_time(self):
        return int(round(time.time() * 1000))
 
    def get_day_start_epoch(self):
        start_str = time.strftime( "%m/%d/%Y" ) + " 00:00:00"
        return int( time.mktime( time.strptime( start_str, "%m/%d/%Y %H:%M:%S" ) ) ) * 1000

    def get_day_end_epoch(self):
        end_str = time.strftime( "%m/%d/%Y ") + " 23:59:59"
        return int( time.mktime( time.strptime( end_str, "%m/%d/%Y %H:%M:%S" ) ) ) * 1000
    
    def get_hour_minutes(self, timestring):
        return time.strftime('%H:%M', time.localtime(float(timestring)/1000))

    def get_schedule_json(self, start, end):
        try:
            r = requests.get('{}&startTime={}&endTime={}'.format(self.url, start, end))
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
            return None
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
            return None
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
            return None
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else", err)
            return None
        
        return r.json()

    def parse_schedule(self, json):
        output = ""
        for item in reversed(json['data']):
            begin = item['startTime']
            begin_hm = self.get_hour_minutes(item['startTime'])
            end = item['endTime']
            end_hm = self.get_hour_minutes(item['endTime'])
            name = item['name'].lower().capitalize()

            if int(begin) < self.get_now_time() < int(end):
                output = output + '[B]' + begin_hm + ' - ' + end_hm + ' : ' + name + ' [running][/B]\n'
            elif int(end) < self.get_now_time():
                # Do not include finished programs
                continue
            elif int(begin) > self.get_now_time():
                output = output + begin_hm + ' - ' + end_hm + ' : ' + name + '\n'
            
        return output

    def parse_current_play(self, json):
        output = ""
        for item in reversed(json['data']):
            begin = item['startTime']
            end = item['endTime']
            name = item['name'].lower().capitalize()

            if int(begin) < self.get_now_time() < int(end):
                return name     

    def get_schedule(self):        
        begin_day = self.get_day_start_epoch()
        end_day = self.get_day_end_epoch()

        schedule_json = self.get_schedule_json(begin_day, end_day)

        if schedule_json:
            return self.parse_schedule(schedule_json)
        else:
            return ""

    def get_current_play(self):
        begin_day = self.get_day_start_epoch()
        end_day = self.get_day_end_epoch()

        schedule_json = self.get_schedule_json(begin_day, end_day)

        if schedule_json:
            return self.parse_current_play(schedule_json)
        else:
            return ""

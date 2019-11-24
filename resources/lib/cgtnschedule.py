import os
import requests
import time

class CGTNScheduleParser:
    """Class to parse the CGTN livestream schedule"""

    def __init__(self, url):
        self.url = url
        self.schedule = None
        pass
 
    def get_day_start_epoch(self):
        start_str = time.strftime( "%m/%d/%Y" ) + " 00:00:00"
        return int( time.mktime( time.strptime( start_str, "%m/%d/%Y %H:%M:%S" ) ) ) * 1000

    def get_day_end_epoch(self):
        end_str = time.strftime( "%m/%d/%Y ") + " 23:59:59"
        return int( time.mktime( time.strptime( end_str, "%m/%d/%Y %H:%M:%S" ) ) ) * 1000

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
        schedule = []
        for item in reversed(json['data']):
            schedule_item = CGTNLiveScheduleItem(item['name'].lower().capitalize(),
                                                 item['startTime'], item['endTime'])
            schedule.append(schedule_item)            
        return schedule

    def get_schedule(self):        
        begin_day = self.get_day_start_epoch()
        end_day = self.get_day_end_epoch()

        schedule_json = self.get_schedule_json(begin_day, end_day)

        if schedule_json:
            self.schedule = self.parse_schedule(schedule_json)
        else:
            print("Failed to parse schedule")
            self.schedule = []
        
        return self.schedule

    def get_play_item(self):
        for item in self.schedule:
            if item.get_status() == CGTNLiveScheduleState.RUNNING:
                return item
        
        print("Failed to get current playing item")
        return None

    def get_future_items(self):
        future_items = []
        for item in self.schedule:
            if item.get_status == CGTNLiveScheduleState.SCHEDULED:
                future_items.append(item)
        
        return future_items


class CGTNLiveScheduleItem:
    """Class to store a single live scheduled item"""

    def __init__(self, program, start, end):
        self.program = program
        self.start = start
        self.end = end
        self.status = self.get_status()
        pass

    def get_hour_minutes(self, timestring):
        return time.strftime('%H:%M', time.localtime(float(timestring)/1000))

    def get_now_time(self):
        return int(round(time.time() * 1000))    

    def get_start_hm(self):
        return self.get_hour_minutes(self.start)

    def get_end_hm(self):
        return self.get_hour_minutes(self.end)
    
    def get_status(self):
        if int(self.start) < self.get_now_time() < int(self.end):
            return CGTNLiveScheduleState.RUNNING
        elif int(self.end) < self.get_now_time():
            return CGTNLiveScheduleState.FINISHED
        elif int(self.start) > self.get_now_time():
            return CGTNLiveScheduleState.SCHEDULED   

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class CGTNLiveScheduleState():
    """Class to represent the status of live scheduled item"""

    FINISHED = "FINISHED"
    RUNNING = "RUNNING"
    SCHEDULED = "SCHEDULED"
